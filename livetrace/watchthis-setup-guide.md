# WatchThis - Chrome Session Monitoring for JobNimbus

A Claude Code command that monitors Chrome sessions to investigate and diagnose JobNimbus issues with automatic code analysis.

## What It Does

**WatchThis** captures your browser activity and automatically:
- Fetches latest code from all repositories
- Records all JobNimbus page navigation
- Logs API calls with request/response data
- Captures POST body data (including form submissions)
- Compares observed behavior to JobNimbus codebase
- Identifies root causes and provides code fix recommendations

## Prerequisites

- **Chrome browser** installed
- **Python 3** with pip (pre-installed on macOS)
- **Claude Code CLI** installed and configured
- Access to JobNimbus codebase at `/Documents/GitHub/`

## Installation

### Step 1: Install Python Dependencies

```bash
pip3 install websocket-client requests
```

### Step 2: Create Scripts Directory

```bash
mkdir -p ~/.claude/scripts
```

### Step 3: Create Monitoring Script

Save this as `~/.claude/scripts/chrome-console-monitor-all-tabs.py`:

```python
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
    try:
        response = requests.get(f'http://localhost:{DEBUG_PORT}/json')
        tabs = response.json()
        pages = [t for t in tabs if t.get('type') in ['page', 'popup', 'webview'] and 'webSocketDebuggerUrl' in t]
        return pages
    except Exception as e:
        return []

def handle_message(ws, message, page_id, page_title):
    try:
        data = json.loads(message)

        if data.get('method') == 'Page.frameNavigated':
            frame = data.get('params', {}).get('frame', {})
            url = frame.get('url', '')
            if 'jobnimbus.com' in url and not url.startswith('https://static.'):
                log(f"[{page_title[:30]}] [NAVIGATION] {url}")

        elif data.get('method') == 'Page.lifecycleEvent':
            params = data.get('params', {})
            event_name = params.get('name', '')
            if event_name in ['DOMContentLoaded', 'load']:
                log(f"[{page_title[:30]}] [PAGE LIFECYCLE] {event_name}")

        elif data.get('method') == 'Network.requestWillBeSent':
            request = data.get('params', {}).get('request', {})
            request_id = data.get('params', {}).get('requestId', '')
            url = request.get('url', '')
            method = request.get('method', 'GET')
            if 'jobnimbus.com' in url and not any(x in url for x in ['static.jobnimbus.com', '.js', '.css', '.png', '.jpg', '.svg', '.woff']):
                log(f"[{page_title[:30]}] [API {method}] {url}")
                if method == 'POST':
                    if request.get('postData'):
                        post_data = request.get('postData', '')[:500]
                        log(f"  POST Data: {post_data}")
                    elif request_id:
                        try:
                            ws.send(json.dumps({
                                "id": 999 + hash(request_id) % 1000,
                                "method": "Network.getRequestPostData",
                                "params": {"requestId": request_id}
                            }))
                        except:
                            pass

        elif data.get('id') and data.get('id') >= 999 and data.get('result', {}).get('postData'):
            post_data = data.get('result', {}).get('postData', '')[:500]
            log(f"  POST Data: {post_data}")

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

        elif data.get('method') == 'Log.entryAdded':
            entry = data.get('params', {}).get('entry', {})
            level = entry.get('level', 'info')
            text = entry.get('text', '')
            url = entry.get('url', '')
            line_number = entry.get('lineNumber', '')
            log(f"[{page_title[:30]}] [LOG.{level.upper()}] {text}")
            if url:
                log(f"  Source: {url}:{line_number}")

        elif data.get('method') == 'Network.loadingFailed':
            params = data.get('params', {})
            if not params.get('canceled', False):
                error_text = params.get('errorText', 'Unknown error')
                log(f"[{page_title[:30]}] [NETWORK FAILED] {error_text}")

        elif data.get('method') == 'Network.responseReceived':
            response = data.get('params', {}).get('response', {})
            status = response.get('status', 200)
            url = response.get('url', 'unknown')
            if 'jobnimbus.com' in url and not any(x in url for x in ['static.jobnimbus.com', '.js', '.css', '.png', '.jpg', '.svg', '.woff']):
                log(f"[{page_title[:30]}] [RESPONSE {status}] {url}")
            elif status >= 400:
                log(f"[{page_title[:30]}] [HTTP {status}] {url}")

    except Exception as e:
        pass

def monitor_page(page):
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
    monitored_pages = set()
    last_page_count = 0

    while True:
        try:
            pages = get_all_pages()
            current_count = len(pages)

            if current_count != last_page_count:
                log(f"Detected {current_count} page(s)")
                last_page_count = current_count

            for page in pages:
                page_id = page.get('id')
                if page_id not in monitored_pages:
                    monitored_pages.add(page_id)
                    thread = threading.Thread(target=monitor_page, args=(page,), daemon=True)
                    thread.start()

            time.sleep(0.5)

        except Exception as e:
            log(f"Error in discovery loop: {e}")
            time.sleep(2)

def main():
    with open(LOG_FILE, 'w') as f:
        f.write(f"Chrome Console Monitor (All Tabs) Started - {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

    try:
        log("Starting multi-tab console monitor...")
        log("Discovering pages...")

        discovery_thread = threading.Thread(target=discover_and_monitor, daemon=True)
        discovery_thread.start()

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
```

### Step 4: Create Launcher Script

Save this as `~/.claude/scripts/monitor-chrome.sh`:

```bash
#!/bin/bash

URL="${1:-https://auth.jobnimbus.com/admin/login}"
LOG_FILE="/tmp/chrome-live-console.log"
MONITOR_PID_FILE="/tmp/chrome-monitor.pid"

echo "🔍 Chrome Console Monitor"
echo "================================"

echo "1. Checking debug port availability..."
if lsof -Pi :9222 -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "   ✗ Port 9222 already in use (another debugging session active)"
  echo "   Close other debugging Chrome instances or stop previous watchthis session"
  exit 1
fi
echo "   ✓ Port 9222 available"

echo "2. Launching Chrome with remote debugging..."
TEMP_PROFILE="/tmp/chrome-debug-profile-$$"
mkdir -p "$TEMP_PROFILE"

/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \
  --user-data-dir="$TEMP_PROFILE" \
  --no-first-run \
  --no-default-browser-check \
  --disable-sync \
  "$URL" > /dev/null 2>&1 &

CHROME_PID=$!
echo "   Chrome PID: $CHROME_PID"

echo "3. Waiting for Chrome to initialize..."
sleep 5

echo "4. Verifying debug port..."
if curl -s http://localhost:9222/json > /dev/null 2>&1; then
  echo "   ✓ Debug port is open"
else
  echo "   ✗ Failed to open debug port"
  exit 1
fi

echo "5. Starting console monitor..."
python3 ~/.claude/scripts/chrome-console-monitor-all-tabs.py > /tmp/monitor-output.log 2>&1 &
MONITOR_PID=$!
echo $MONITOR_PID > "$MONITOR_PID_FILE"
echo "   Monitor PID: $MONITOR_PID"

echo "6. Monitoring active"
echo "================================"
echo ""
echo "✓ Ready - perform your actions in Chrome"
echo ""
```

### Step 5: Create Repository Fetch Script

Save this as `~/.claude/scripts/fetch-all-repos.sh`:

```bash
#!/bin/bash

GITHUB_DIR="/Users/garrett.young/Documents/GitHub"

echo "📦 Fetching latest code from all repositories..."
echo "================================"

for dir in "$GITHUB_DIR"/*; do
  if [ -d "$dir/.git" ]; then
    repo_name=$(basename "$dir")
    echo "Fetching: $repo_name"
    (cd "$dir" && git fetch origin 2>&1 | grep -v "^$") || echo "  ⚠ Failed to fetch"
  fi
done

echo "================================"
echo "✓ Repository fetch complete"
echo ""
```

### Step 6: Make Scripts Executable

```bash
chmod +x ~/.claude/scripts/monitor-chrome.sh
chmod +x ~/.claude/scripts/chrome-console-monitor-all-tabs.py
chmod +x ~/.claude/scripts/fetch-all-repos.sh
```

### Step 7: Create Claude Command

Save this as `~/.claude/commands/watchthis.md`:

```markdown
# Watch This - Chrome Session Monitoring

Start Chrome with enhanced monitoring to investigate JobNimbus issues.

## Your Task:

1. **Ask the user**: "Describe the issue you want to investigate:"
   - Wait for their description
   - Store this context for analysis

2. **Fetch latest code** by running:
   ```bash
   ~/.claude/scripts/fetch-all-repos.sh
   ```

3. **Start monitoring** by running:
   ```bash
   ~/.claude/scripts/monitor-chrome.sh
   ```

4. **Wait silently** for the user to perform actions in Chrome

5. **When user says "done"**, automatically:
   - Analyze captured logs (`/tmp/chrome-live-console.log`)
   - Extract navigation paths, API calls, POST data, and responses
   - Search for errors or unexpected behavior related to the described issue
   - Compare observed behavior to JobNimbus codebase (`~/Documents/GitHub`)
   - Identify root causes

6. **Deliver** in this exact format:

   **PART 1: Bug Report Form** (at the top)
   ```
   Description: [Brief description of the issue]
   Date & Time Issue Occurred: [Extract from logs if available, otherwise leave blank]
   Company JN ID: [Extract from session logs if available, otherwise leave blank]
   User JN ID: [Extract from session logs if available, otherwise leave blank]
   Affected Record: [Extract record type/ID from logs if available, otherwise leave blank]


   Replicable in Customer's Account? [Yes/No based on testing, or leave blank if unknown]
   Replicable in Test Account? [Leave blank]
   Test Account Replicated in: [Leave blank]
   Record Replicated with: [Leave blank]


   Prerequisites:
   [List specific prerequisites needed to reproduce, or leave blank if none identified]


   Steps to Replicate:
   [Clear, numbered steps starting with "Login to JobNimbus on..."]


   Expected Result: [What should happen]
   Actual Result: [What actually happened]


   Steps to View:
   [Steps to view the issue, starting with "Login to JobNimbus on..."]


   Screenshots: [Leave blank]
   User Recording/Zoom Meeting: [Leave blank]


   Specific Troubleshooting:
   [List troubleshooting steps attempted or recommended, or leave blank if none]


   Additional Information:
   [Any relevant context from logs or session, or leave blank if none]
   ```

   **PART 2: Technical Analysis** (below the form)
   - Root cause analysis (referencing the original issue description)
   - Full code change recommendations (before/after code)
   - File paths and line numbers
   - Code explanation with full details

## Important:
- No prompts or confirmations during monitoring (only initial issue description)
- After user says "done", read all necessary files without asking for approval
- Automatically stop monitoring when analysis begins
- Focus on JobNimbus-related API calls and behavior
- Compare frontend behavior (logs) to backend code (C#)
- Keep the issue description in context throughout analysis
```

### Step 8: Configure Auto-Approval for File Reads

**Important**: This prevents prompts when analyzing code after you say "done".

Edit or create `~/.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Read(/Users/garrett.young/Documents/GitHub/**)"
    ],
    "deny": [],
    "ask": []
  }
}
```

**Note**: Replace `/Users/garrett.young/Documents/GitHub` with your actual GitHub directory path.

### Step 9: Configure Default Behavior (Optional)

Create `~/.claude/CLAUDE.md` to set defaults:

```markdown
### Code Search Default Path
When searching code, default to searching in `~/Documents/GitHub` unless a different path is explicitly specified.

### JobNimbus Help Center
When questions arise about JobNimbus features, search the JobNimbus Help Center at https://support.jobnimbus.com/
```

## Usage

### Start an Investigation

1. Open Claude Code in your terminal
2. Type: `/watchthis`
3. Describe the issue you want to investigate
4. Perform the actions in Chrome that reproduce the issue
5. When done, type: `done`
6. Claude automatically analyzes and provides:
   - **Bug Report Form** - Structured report with all key details
   - **Technical Analysis** - Root cause and code fix recommendations

### Example Session

```
You: /watchthis

Claude: Describe the issue you want to investigate:

You: @mention notifications not sending for users with periods in their names

Claude: ✓ Monitoring active. Perform your testing and reply "done" when finished.

[You perform testing in Chrome...]

You: done

Claude: ## Analysis Complete

Description: @mention email notifications not sending for users with periods in their names
Date & Time Issue Occurred: 2025-11-20 14:32:00
Company JN ID:
User JN ID:
Affected Record: Note created on job


Replicable in Customer's Account? Yes
Replicable in Test Account?
Test Account Replicated in:
Record Replicated with:


Prerequisites:
- Account with active users
- At least one user with periods in their name (e.g., "A.J. Smith")
- Permission to create notes on jobs


Steps to Replicate:
1. Login to admin tool at https://auth.jobnimbus.com/admin/login
2. Impersonate a customer account
3. Navigate to any job page
4. Create a new note with @mention for user with periods in name (e.g., @AjJabari for user "A.J. Jabari")
5. Observe: @mention does not match, no notification sent


Expected Result: User "A.J. Jabari" should be mentioned when typing @AjJabari and receive email notification
Actual Result: @mention matching fails, user is not mentioned, no notification sent


Steps to View:
1. Login to admin tool at https://auth.jobnimbus.com/admin/login
2. Impersonate the customer account used in testing
3. Navigate to the job where note was created
4. Check note content - @mention will appear as plain text instead of highlighted mention
5. Check user's email - no notification received


Screenshots:
User Recording/Zoom Meeting:


Specific Troubleshooting:
- Tested with user "Lolli Young" (@LolliYoung) - worked successfully
- Tested with user "A.J. Jabari" (@AjJabari) - failed
- Issue specific to names containing periods


Additional Information:
Created note with text: "@LolliYoung @AjJabari Testing one mo time"
@LolliYoung matched successfully, @AjJabari failed


---

## Technical Analysis

### Root Cause
TitleCaseString() in UtilityManager.cs:682 strips periods, converting "A.J." to "AJ" then to "AJJabari".
Frontend sends "@AjJabari" but backend expects "@AJJabari" (case-sensitive match).

### Code Fixes

[Fix #1: UtilityManager.cs:682]
Remove period stripping from TitleCaseString()...

[Fix #2: EmailManager.cs:932]
Add case-insensitive matching for @mentions...
```

## What Gets Captured

- **Navigation**: Every JobNimbus page you visit
- **API Calls**: All requests with full URLs
- **POST Data**: Form submissions and request bodies
- **Responses**: HTTP status codes for all requests
- **Console Logs**: JavaScript errors and log messages
- **Network Failures**: Failed requests and timeouts

## Troubleshooting

### "Command not found: python3"
Install Python 3:
```bash
brew install python3
```

### "Module not found: websocket"
Install dependencies:
```bash
pip3 install websocket-client requests
```

### "Port 9222 already in use"
Another debugging session is active. Close the previous `/watchthis` Chrome window or restart the monitoring session.

### "Debug port is not open"
Chrome failed to enable debugging. Wait a few seconds and try running `/watchthis` again.

### Chrome doesn't open to the right page
The script uses a temporary profile. You'll need to login manually each time.

## Notes

- **Your existing Chrome windows stay open** - only opens a new debugging window
- Chrome uses a **temporary profile** (no saved logins/extensions)
- Monitoring captures **only the new debugging window**, not your regular Chrome
- Logs are stored at `/tmp/chrome-live-console.log`
- Previous logs are overwritten on each run
- If you get "Port 9222 already in use", close the previous `/watchthis` session first

## Privacy & Security

- All monitoring happens **locally on your machine**
- Logs contain **sensitive data** (tokens, credentials, POST bodies)
- Log files are stored in `/tmp/` (cleared on reboot)
- **Never share log files** without sanitizing sensitive data

## Support

For issues or questions, contact the team member who shared this guide.
