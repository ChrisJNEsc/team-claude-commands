#!/usr/bin/env python3

import json
import requests
import websocket
import threading
import time
import sys
from datetime import datetime

LOG_FILE = '/tmp/chrome-live-console.log'
DEBUG_PORT = 9222

active_connections = {}
connection_lock = threading.Lock()

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

        # Page navigation events
        if data.get('method') == 'Page.frameNavigated':
            frame = data.get('params', {}).get('frame', {})
            url = frame.get('url', '')
            # Only log JobNimbus navigation
            if 'jobnimbus.com' in url and not url.startswith('https://static.'):
                log(f"[{page_title[:30]}] [NAVIGATION] {url}")

        # Document lifecycle events
        elif data.get('method') == 'Page.lifecycleEvent':
            params = data.get('params', {})
            event_name = params.get('name', '')
            if event_name in ['DOMContentLoaded', 'load']:
                log(f"[{page_title[:30]}] [PAGE LIFECYCLE] {event_name}")

        # Network requests - log all JobNimbus API calls
        elif data.get('method') == 'Network.requestWillBeSent':
            request = data.get('params', {}).get('request', {})
            request_id = data.get('params', {}).get('requestId', '')
            url = request.get('url', '')
            method = request.get('method', 'GET')
            # Only log JobNimbus API calls and page loads
            if 'jobnimbus.com' in url and not any(x in url for x in ['static.jobnimbus.com', '.js', '.css', '.png', '.jpg', '.svg', '.woff']):
                log(f"[{page_title[:30]}] [API {method}] {url}")
                # For POST requests, try to get the body data
                if method == 'POST':
                    # First try inline postData
                    if request.get('postData'):
                        post_data = request.get('postData', '')[:500]  # First 500 chars
                        log(f"  POST Data: {post_data}")
                    # If not available inline, request it via CDP
                    elif request_id:
                        try:
                            ws.send(json.dumps({
                                "id": 999 + hash(request_id) % 1000,
                                "method": "Network.getRequestPostData",
                                "params": {"requestId": request_id}
                            }))
                        except:
                            pass  # Ignore if we can't send the request

        # Handle responses to Network.getRequestPostData
        elif data.get('id') and data.get('id') >= 999 and data.get('result', {}).get('postData'):
            post_data = data.get('result', {}).get('postData', '')[:500]  # First 500 chars
            log(f"  POST Data: {post_data}")

        # Console API messages
        elif data.get('method') == 'Runtime.consoleAPICalled':
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
        elif data.get('method') == 'Runtime.exceptionThrown':
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
        elif data.get('method') == 'Log.entryAdded':
            entry = data.get('params', {}).get('entry', {})
            level = entry.get('level', 'info')
            text = entry.get('text', '')
            url = entry.get('url', '')
            line_number = entry.get('lineNumber', '')

            log(f"[{page_title[:30]}] [LOG.{level.upper()}] {text}")
            if url:
                log(f"  Source: {url}:{line_number}")

        # Network failures
        elif data.get('method') == 'Network.loadingFailed':
            params = data.get('params', {})
            if not params.get('canceled', False):
                error_text = params.get('errorText', 'Unknown error')
                log(f"[{page_title[:30]}] [NETWORK FAILED] {error_text}")

        # Network responses
        elif data.get('method') == 'Network.responseReceived':
            response = data.get('params', {}).get('response', {})
            status = response.get('status', 200)
            url = response.get('url', 'unknown')
            # Log all JobNimbus API responses
            if 'jobnimbus.com' in url and not any(x in url for x in ['static.jobnimbus.com', '.js', '.css', '.png', '.jpg', '.svg', '.woff']):
                log(f"[{page_title[:30]}] [RESPONSE {status}] {url}")
            # Also log non-JobNimbus errors
            elif status >= 400:
                log(f"[{page_title[:30]}] [HTTP {status}] {url}")

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
            log(f"[{page_title[:30]}] Monitoring enabled (Console, Runtime, Log, Network, Page)")

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
    # Initialize log file
    with open(LOG_FILE, 'w') as f:
        f.write(f"Chrome Console Monitor (All Tabs) Started - {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

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
