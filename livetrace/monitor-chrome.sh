#!/bin/bash

# Chrome Console Monitor Launcher
# This script launches Chrome with remote debugging and starts the console monitor

URL="${1:-https://auth.jobnimbus.com/admin/login}"
LOG_FILE="/tmp/chrome-live-console.log"
MONITOR_PID_FILE="/tmp/chrome-monitor.pid"

echo "🔍 Chrome Console Monitor"
echo "================================"

# Step 1: Clean up any existing debugging sessions automatically
echo "1. Cleaning up existing debug sessions..."

# Kill any existing Chrome processes with remote debugging
if pgrep -f "Chrome.*remote-debugging-port" > /dev/null 2>&1; then
  echo "   Found existing Chrome debug session, terminating..."
  pkill -f "Chrome.*remote-debugging-port" 2>/dev/null
  sleep 2
fi

# Kill any processes using port 9222
if lsof -ti:9222 > /dev/null 2>&1; then
  PORT_PIDS=$(lsof -ti:9222)
  RISKY=false
  for PID in $PORT_PIDS; do
    CMDLINE=$(ps -p "$PID" -o args= 2>/dev/null || true)
    if echo "$CMDLINE" | grep -q "chrome-debug-profile"; then
      : # Safe - this is a previous livetrace debug instance
    elif [ -n "$CMDLINE" ]; then
      RISKY=true
    fi
  done

  if [ "$RISKY" = true ]; then
    echo ""
    echo "   ⚠️  Port 9222 is in use by a process that may be tied to your regular Chrome session."
    echo "   Killing it could close existing tabs."
    echo ""
    read -p "   Proceed with cleanup? (y/n): " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
      echo "   Aborted. Close Chrome or free port 9222 manually, then retry."
      exit 1
    fi
  fi

  echo "   Freeing port 9222..."
  lsof -ti:9222 | xargs kill -9 2>/dev/null
  sleep 1
fi

# Kill any existing monitor processes
if [ -f "$MONITOR_PID_FILE" ]; then
  OLD_PID=$(cat "$MONITOR_PID_FILE" 2>/dev/null)
  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "   Stopping previous monitor process..."
    kill "$OLD_PID" 2>/dev/null
  fi
  rm -f "$MONITOR_PID_FILE"
fi

# Clean up old temp profiles
rm -rf /tmp/chrome-debug-profile-* 2>/dev/null

# Clear previous log
> "$LOG_FILE"

echo "   ✓ Cleanup complete, port 9222 available"

# Step 2: Launch Chrome with remote debugging (temporary profile)
echo "2. Launching Chrome with remote debugging..."
TEMP_PROFILE="/tmp/chrome-debug-profile-$$"
mkdir -p "$TEMP_PROFILE"

# NOTE: On macOS, Chrome may ignore --user-data-dir for its singleton lock and attach
# to the existing main process instead of spawning a separate one. When that happens,
# port 9222 ends up owned by regular Chrome, and the cleanup kill -9 crashes all tabs.
# If the port check above isn't enough, forcing a unique TMPDIR isolates the singleton:
#   TMPDIR="$TEMP_PROFILE/tmp" /Applications/Google\ Chrome.app/...
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

# Step 3: Wait for Chrome to start
echo "3. Waiting for Chrome to initialize..."
sleep 5

# Step 4: Verify debug port is open
echo "4. Verifying debug port..."
if curl -s http://localhost:9222/json > /dev/null 2>&1; then
  echo "   ✓ Debug port is open"
else
  echo "   ✗ Failed to open debug port"
  exit 1
fi

# Step 5: Start the console monitor
echo "5. Starting console monitor..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/chrome-console-monitor-all-tabs.py" > /tmp/monitor-output.log 2>&1 &
MONITOR_PID=$!
echo $MONITOR_PID > "$MONITOR_PID_FILE"
echo "   Monitor PID: $MONITOR_PID"

# Step 6: Done
echo "6. Monitoring active"
echo "================================"
echo ""
echo "✓ Ready - perform your actions in Chrome"
echo ""
