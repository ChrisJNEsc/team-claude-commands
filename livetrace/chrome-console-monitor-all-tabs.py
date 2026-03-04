#!/usr/bin/env python3

import json
import requests
import websocket
import threading
import time
import sys
from datetime import datetime
from urllib.parse import urlparse

LOG_FILE = '/tmp/chrome-live-console.log'
DEBUG_PORT = 9222

active_connections = {}
connection_lock = threading.Lock()
# Track request URLs by requestId so we can label response bodies
pending_requests = {}
# ID range for response body requests (separate from POST data range)
RESPONSE_BODY_ID_BASE = 50000

# --- Constants ---

STATIC_EXTENSIONS = [
    '.js', '.css', '.png', '.jpg', '.jpeg', '.svg', '.woff', '.woff2',
    '.ttf', '.eot', '.gif', '.ico', '.map', '.webp',
]

SKIP_URL_PREFIXES = ['data:', 'chrome-extension://']

DOMAIN_TAGS = {
    'JN': ['jobnimbus.com'],
    'SQ': ['sumoquote.com'],
    'SUPPLIER': ['abcsupply.com', 'beacon', 'srs', 'supplier'],
    'MEASURE': ['eagleview', 'hover.to', 'hoverapi', 'hover.com'],
    'FINANCE': ['wisetack', 'financing'],
}

ESTIMATE_FLOW_PATTERNS = {
    'ESTIMATE': ['/estimate', '/report/', '/estimates'],
    'LAYOUT': ['/layouts', '/layout'],
    'SIGNING': ['/signing', '/reviewQuote', '/signQuote', '/publicreviewhub', '/manuallySign', '/inperson'],
    'TEMPLATE': ['/template', '/gettemplate'],
    'MEASUREMENT': ['/measurement', '/thirdPartyMeasurement', '/measurementprovider'],
    'FINANCING': ['/financing', '/wisetack', '/payment-link', '/monthly-payment'],
    'MATERIAL': ['/material', '/suppliers', '/products', '/branches'],
    'PROPOSAL': ['/proposals'],
    'SIGNATURE': ['/possiblesigners', '/signingurl', '/dsigndocument', '/digitalsignature'],
    'PDF': ['/pdf', '/download', '/regenerateQuote'],
    'TAX': ['/tax'],
}

BODY_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}


def get_domain_tag(url):
    """Categorize a URL by domain."""
    url_lower = url.lower()
    for tag, patterns in DOMAIN_TAGS.items():
        if any(p in url_lower for p in patterns):
            return tag
    return 'EXT'


def get_flow_tag(url):
    """Return an estimate flow tag if the URL matches known patterns, or empty string."""
    url_lower = url.lower()
    for tag, patterns in ESTIMATE_FLOW_PATTERNS.items():
        if any(p in url_lower for p in patterns):
            return tag
    return ''


def should_skip_url(url):
    """Return True if the URL is a static asset or should be skipped."""
    if any(url.startswith(prefix) for prefix in SKIP_URL_PREFIXES):
        return True
    if 'static.jobnimbus.com' in url:
        return True
    url_lower = url.lower()
    # Check path portion only (ignore query params)
    path = url_lower.split('?')[0]
    return any(path.endswith(ext) for ext in STATIC_EXTENSIONS)


def log(message):
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(log_line)
    print(log_line.strip())

def get_all_pages():
    """Get all page targets from Chrome (including popups and new windows)"""
    try:
        response = requests.get(f'http://localhost:{DEBUG_PORT}/json')
        tabs = response.json()
        # Include page, popup, and other window types
        pages = [t for t in tabs if t.get('type') in ['page', 'popup', 'webview'] and 'webSocketDebuggerUrl' in t]
        return pages
    except Exception as e:
        # Silently fail to avoid spam
        return []

def handle_message(ws, message, page_id, page_title):
    """Handle messages from a specific page"""
    try:
        data = json.loads(message)
        method = data.get('method', '')

        # Page navigation events
        if method == 'Page.frameNavigated':
            frame = data.get('params', {}).get('frame', {})
            url = frame.get('url', '')
            if url and not url.startswith('data:') and not url.startswith('chrome-extension://'):
                tag = get_domain_tag(url)
                log(f"[{page_title[:30]}] [NAVIGATION] [{tag}] {url}")

        # Document lifecycle events
        elif method == 'Page.lifecycleEvent':
            params = data.get('params', {})
            event_name = params.get('name', '')
            if event_name in ['DOMContentLoaded', 'load']:
                log(f"[{page_title[:30]}] [PAGE LIFECYCLE] {event_name}")

        # Network requests - log ALL API calls (filtered for static assets)
        elif method == 'Network.requestWillBeSent':
            request = data.get('params', {}).get('request', {})
            request_id = data.get('params', {}).get('requestId', '')
            url = request.get('url', '')
            req_method = request.get('method', 'GET')

            if not should_skip_url(url):
                domain_tag = get_domain_tag(url)
                flow_tag = get_flow_tag(url)
                flow_str = f" [{flow_tag}]" if flow_tag else ''

                # Track request for response body labeling and timing
                if request_id:
                    pending_requests[request_id] = {
                        'url': url,
                        'method': req_method,
                        'start_time': time.monotonic(),
                    }

                log(f"[{page_title[:30]}] [API {req_method}] [{domain_tag}]{flow_str} {url}")

                # Capture request bodies for POST, PUT, PATCH, DELETE
                if req_method in BODY_METHODS:
                    if request.get('postData'):
                        post_data = request.get('postData', '')
                        log(f"  Request Body: {post_data}")
                    elif request_id:
                        try:
                            ws.send(json.dumps({
                                "id": 999 + hash(request_id) % 1000,
                                "method": "Network.getRequestPostData",
                                "params": {"requestId": request_id}
                            }))
                        except:
                            pass

        # Handle responses to Network.getRequestPostData
        elif data.get('id') and 999 <= data.get('id', 0) < RESPONSE_BODY_ID_BASE and data.get('result', {}).get('postData'):
            post_data = data.get('result', {}).get('postData', '')
            log(f"  Request Body: {post_data}")

        # Handle responses to Network.getResponseBody
        elif data.get('id') and data.get('id', 0) >= RESPONSE_BODY_ID_BASE and 'result' in data:
            result = data.get('result', {})
            body = result.get('body', '')
            base64_encoded = result.get('base64Encoded', False)
            if body and not base64_encoded:
                # Look up original request URL from the stashed info
                msg_id = data.get('id', 0)
                req_hash = msg_id - RESPONSE_BODY_ID_BASE
                # Find matching request by hash
                source_label = ''
                for rid, info in list(pending_requests.items()):
                    if hash(rid) % 10000 == req_hash:
                        source_label = f" for [{info['method']} {info['url']}]"
                        break
                log(f"  Response Body{source_label}: {body}")

        # Network loading finished - request response body for tracked API calls
        elif method == 'Network.loadingFinished':
            request_id = data.get('params', {}).get('requestId', '')
            if request_id in pending_requests:
                try:
                    ws.send(json.dumps({
                        "id": RESPONSE_BODY_ID_BASE + hash(request_id) % 10000,
                        "method": "Network.getResponseBody",
                        "params": {"requestId": request_id}
                    }))
                except:
                    pass
                # Don't delete yet - we need the info for response body labeling
                # It will be cleaned up after the response body arrives or on timeout

        # Network responses - with timing
        elif method == 'Network.responseReceived':
            response = data.get('params', {}).get('response', {})
            status = response.get('status', 200)
            url = response.get('url', 'unknown')
            request_id = data.get('params', {}).get('requestId', '')

            if not should_skip_url(url):
                domain_tag = get_domain_tag(url)
                flow_tag = get_flow_tag(url)
                flow_str = f" [{flow_tag}]" if flow_tag else ''

                # Calculate timing
                timing_str = ''
                if request_id and request_id in pending_requests:
                    start_time = pending_requests[request_id].get('start_time')
                    if start_time:
                        duration_ms = int((time.monotonic() - start_time) * 1000)
                        timing_str = f" [{duration_ms}ms]"

                log(f"[{page_title[:30]}] [RESPONSE {status}] [{domain_tag}]{flow_str}{timing_str} {url}")

        # WebSocket events
        elif method == 'Network.webSocketCreated':
            params = data.get('params', {})
            url = params.get('url', '')
            log(f"[{page_title[:30]}] [WEBSOCKET OPENED] {url}")

        elif method == 'Network.webSocketFrameReceived':
            params = data.get('params', {})
            payload = params.get('response', {}).get('payloadData', '')
            if payload:
                log(f"[{page_title[:30]}] [WEBSOCKET RECV] {payload}")

        elif method == 'Network.webSocketFrameSent':
            params = data.get('params', {})
            payload = params.get('response', {}).get('payloadData', '')
            if payload:
                log(f"[{page_title[:30]}] [WEBSOCKET SENT] {payload}")

        elif method == 'Network.webSocketClosed':
            params = data.get('params', {})
            log(f"[{page_title[:30]}] [WEBSOCKET CLOSED]")

        # Console API messages
        elif method == 'Runtime.consoleAPICalled':
            params = data.get('params', {})
            msg_type = params.get('type', 'log')
            args = params.get('args', [])

            log_args = []
            for arg in args:
                if 'value' in arg:
                    log_args.append(str(arg['value']))
                elif 'description' in arg:
                    log_args.append(arg['description'])
                else:
                    log_args.append(json.dumps(arg))

            log(f"[{page_title[:30]}] [CONSOLE.{msg_type.upper()}] {' '.join(log_args)}")

            if 'stackTrace' in params and params['stackTrace'].get('callFrames'):
                frame = params['stackTrace']['callFrames'][0]
                log(f"  Stack: {frame.get('url', 'unknown')}:{frame.get('lineNumber', '?')}")

        # Runtime exceptions
        elif method == 'Runtime.exceptionThrown':
            details = data.get('params', {}).get('exceptionDetails', {})
            log(f"[{page_title[:30]}] [ERROR] {details.get('text', 'Unknown error')}")

            if 'exception' in details:
                exc = details['exception']
                desc = exc.get('description', json.dumps(exc))
                log(f"  {desc}")

            if 'stackTrace' in details and details['stackTrace'].get('callFrames'):
                for frame in details['stackTrace']['callFrames']:
                    func_name = frame.get('functionName', '(anonymous)')
                    url = frame.get('url', 'unknown')
                    line = frame.get('lineNumber', '?')
                    col = frame.get('columnNumber', '?')
                    log(f"    at {func_name} ({url}:{line}:{col})")

        # Log entries
        elif method == 'Log.entryAdded':
            entry = data.get('params', {}).get('entry', {})
            level = entry.get('level', 'info')
            text = entry.get('text', '')
            url = entry.get('url', '')
            line_number = entry.get('lineNumber', '')

            log(f"[{page_title[:30]}] [LOG.{level.upper()}] {text}")
            if url:
                log(f"  Source: {url}:{line_number}")

        # Network failures
        elif method == 'Network.loadingFailed':
            params = data.get('params', {})
            request_id = params.get('requestId', '')
            if not params.get('canceled', False):
                error_text = params.get('errorText', 'Unknown error')
                log(f"[{page_title[:30]}] [NETWORK FAILED] {error_text}")
            # Clean up pending request on failure
            if request_id in pending_requests:
                del pending_requests[request_id]

        # Auto-attached target (iframe, worker) - enable network monitoring on it
        elif method == 'Target.attachedToTarget':
            session_id = data.get('params', {}).get('sessionId', '')
            target_info = data.get('params', {}).get('targetInfo', {})
            target_url = target_info.get('url', '')
            target_type = target_info.get('type', '')
            if session_id:
                try:
                    # Enable Network and Runtime on the attached target via its session
                    for domain_id, domain in [(10, "Network.enable"), (11, "Runtime.enable"), (12, "Console.enable")]:
                        ws.send(json.dumps({
                            "id": domain_id,
                            "sessionId": session_id,
                            "method": domain
                        }))
                    log(f"[{page_title[:30]}] [IFRAME ATTACHED] {target_type}: {target_url[:80]}")
                except:
                    pass

    except Exception as e:
        pass  # Ignore parse errors

def monitor_page(page):
    """Monitor a single page/tab"""
    page_id = page.get('id')
    page_url = page.get('url', 'unknown')
    page_title = page.get('title', 'Untitled')
    ws_url = page.get('webSocketDebuggerUrl')

    try:
        log(f"Connecting to page: {page_title} ({page_url[:50]}...)")

        def on_message(ws, message):
            handle_message(ws, message, page_id, page_title)

        def on_error(ws, error):
            log(f"[{page_title[:30]}] WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            with connection_lock:
                if page_id in active_connections:
                    del active_connections[page_id]
            log(f"[{page_title[:30]}] Connection closed")

        def on_open(ws):
            # Enable Console, Runtime, Log, Network, and Page domains
            ws.send(json.dumps({"id": 1, "method": "Console.enable"}))
            ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
            ws.send(json.dumps({"id": 3, "method": "Log.enable"}))
            ws.send(json.dumps({"id": 4, "method": "Network.enable"}))
            ws.send(json.dumps({"id": 5, "method": "Page.enable"}))
            # Auto-attach to iframes/workers so we capture their network requests too
            ws.send(json.dumps({"id": 6, "method": "Target.setAutoAttach", "params": {
                "autoAttach": True,
                "waitForDebuggerOnStart": False,
                "flatten": True
            }}))
            log(f"[{page_title[:30]}] Monitoring enabled (Console, Runtime, Log, Network, Page, WebSocket, Iframes)")

        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        with connection_lock:
            active_connections[page_id] = ws

        ws.run_forever()

    except Exception as e:
        log(f"Error monitoring page {page_title}: {e}")

def discover_and_monitor():
    """Continuously discover new pages and start monitoring them"""
    monitored_pages = set()
    last_page_count = 0

    while True:
        try:
            pages = get_all_pages()
            current_count = len(pages)

            # Log when page count changes
            if current_count != last_page_count:
                log(f"Detected {current_count} page(s)")
                last_page_count = current_count

            for page in pages:
                page_id = page.get('id')
                if page_id not in monitored_pages:
                    monitored_pages.add(page_id)
                    # Start monitoring in a new thread
                    thread = threading.Thread(target=monitor_page, args=(page,), daemon=True)
                    thread.start()

            time.sleep(0.5)  # Check for new pages every 0.5 seconds (faster discovery)

        except Exception as e:
            log(f"Error in discovery loop: {e}")
            time.sleep(2)

def main():
    # Initialize log file with session metadata
    with open(LOG_FILE, 'w') as f:
        f.write(f"Chrome Console Monitor (All Tabs) Started - {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")
        f.write("=== LIVETRACE SESSION ===\n")
        f.write("Capture: ALL domains (tagged by category)\n")
        f.write("Bodies: Full request/response bodies (POST/PUT/PATCH/DELETE)\n")
        f.write("WebSocket: SignalR and WS frames captured\n")
        f.write("Timing: Request duration in ms\n")
        f.write("Tags: JN, SQ, SUPPLIER, MEASURE, FINANCE, ESTIMATE, LAYOUT, SIGNING, TEMPLATE, MEASUREMENT, FINANCING, MATERIAL, PROPOSAL, SIGNATURE, PDF, TAX, EXT\n")
        f.write("========================\n\n")

    try:
        log("Starting multi-tab console monitor...")
        log("Discovering pages...")

        # Start discovery thread
        discovery_thread = threading.Thread(target=discover_and_monitor, daemon=True)
        discovery_thread.start()

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log("Monitoring stopped by user")
        sys.exit(0)
    except Exception as e:
        log(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
