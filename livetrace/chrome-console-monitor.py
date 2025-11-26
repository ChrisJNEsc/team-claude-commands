#!/usr/bin/env python3

import json
import requests
import websocket
import sys
from datetime import datetime

LOG_FILE = '/tmp/chrome-live-console.log'
DEBUG_PORT = 9222

def log(message):
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(log_line)
    print(log_line.strip())

def get_websocket_debugger_url():
    try:
        response = requests.get(f'http://localhost:{DEBUG_PORT}/json')
        tabs = response.json()
        tab = next((t for t in tabs if t.get('type') == 'page'), tabs[0] if tabs else None)
        if tab and 'webSocketDebuggerUrl' in tab:
            return tab['webSocketDebuggerUrl']
        raise Exception('No debugger URL found')
    except Exception as e:
        raise Exception(f'Failed to get debugger URL: {e}')

def on_message(ws, message):
    try:
        data = json.loads(message)

        # Console API messages (console.log, console.error, etc.)
        if data.get('method') == 'Runtime.consoleAPICalled':
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

            log(f"[CONSOLE.{msg_type.upper()}] {' '.join(log_args)}")

            if 'stackTrace' in params and params['stackTrace'].get('callFrames'):
                frame = params['stackTrace']['callFrames'][0]
                log(f"  Stack: {frame.get('url', 'unknown')}:{frame.get('lineNumber', '?')}")

        # Runtime exceptions (uncaught errors)
        elif data.get('method') == 'Runtime.exceptionThrown':
            details = data.get('params', {}).get('exceptionDetails', {})
            log(f"[ERROR] {details.get('text', 'Unknown error')}")

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

            log(f"[LOG.{level.upper()}] {text}")
            if url:
                log(f"  Source: {url}:{line_number}")

        # Network request failures
        elif data.get('method') == 'Network.loadingFailed':
            params = data.get('params', {})
            if not params.get('canceled', False):
                error_text = params.get('errorText', 'Unknown error')
                request_id = params.get('requestId', 'unknown')
                log(f"[NETWORK FAILED] {error_text} (Request ID: {request_id})")

        # Network responses with errors
        elif data.get('method') == 'Network.responseReceived':
            response = data.get('params', {}).get('response', {})
            status = response.get('status', 200)
            if status >= 400:
                url = response.get('url', 'unknown')
                log(f"[HTTP {status}] {url}")

    except Exception as e:
        # Ignore parse errors
        pass

def on_error(ws, error):
    log(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    log("Connection closed. Monitoring stopped.")

def on_open(ws):
    log("Connected to Chrome DevTools")

    # Enable Console domain
    ws.send(json.dumps({"id": 1, "method": "Console.enable"}))

    # Enable Runtime domain for console messages
    ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))

    # Enable Log domain
    ws.send(json.dumps({"id": 3, "method": "Log.enable"}))

    # Enable Network domain for network logs
    ws.send(json.dumps({"id": 4, "method": "Network.enable"}))

    log("Console monitoring enabled. Waiting for messages...\n")

def main():
    # Initialize log file
    with open(LOG_FILE, 'w') as f:
        f.write(f"Chrome Console Monitor Started - {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

    try:
        log("Connecting to Chrome DevTools Protocol...")
        ws_url = get_websocket_debugger_url()
        log(f"WebSocket URL: {ws_url}")

        ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        ws.run_forever()

    except Exception as e:
        log(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
