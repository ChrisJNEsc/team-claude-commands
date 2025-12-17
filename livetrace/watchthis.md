# LiveTrace - Chrome Session Monitoring

Start Chrome with enhanced monitoring to capture JobNimbus session data.

## Your Task:

1. **Ask the user**: "Describe what you'll be testing or investigating:"
   - Wait for their description
   - Store this context for the session summary

2. **Check dependencies** before starting:
   ```bash
   python3 -c "import requests; import websocket" 2>/dev/null
   ```
   - If this fails (exit code non-zero), tell the user: "Missing Python dependencies. Please run `/team:livetrace-install` first."
   - Do NOT proceed until dependencies are installed
   - If it succeeds, continue silently (no output to user)

3. **Start monitoring** by running:
   ```bash
   ~/Documents/GitHub/team-claude-commands/livetrace/monitor-chrome.sh
   ```

4. **Tell the user**: "Monitoring active. Perform your actions in Chrome and say **done** when finished."

5. **Wait silently** for the user to perform actions in Chrome

6. **When user says "done"**:
   - **First**: Stop the monitoring by running:
     ```bash
     pkill -f "chrome-console-monitor"
     ```
   - **Then**: Read `/tmp/chrome-live-console.log`
   - Compile and organize the captured data

7. **Deliver a Session Summary** in this format:

   ## Session Summary

   **Issue Context**: [The description the user provided]

   **Session Duration**: [Start time] - [End time from logs]

   ### Pages Visited
   [List all NAVIGATION entries in order]

   ### API Calls
   [List all API requests with method, endpoint, and response status]
   | Method | Endpoint | Status |
   |--------|----------|--------|
   | GET    | /api/... | 200    |

   ### POST/PUT Data
   [List any POST or PUT requests with their payloads]

   ### Errors & Warnings
   [List any ERROR, FAILED, or non-2xx responses]
   - Include JavaScript errors with stack traces
   - Include failed network requests
   - Include console warnings/errors

   ### Key Observations
   [Brief bullet points of notable patterns or issues observed]

   ---

   **Log file**: `/tmp/chrome-live-console.log`

   **Next steps**: You can now run additional commands to analyze this session:
   - `/triage` - Create a bug report from this session
   - `/investigateline` - Search codebase for root cause
   - Ask me to search for specific endpoints or errors in the codebase

## Important:
- No prompts or confirmations during monitoring (only initial description)
- Do NOT search the codebase automatically
- Do NOT create Linear issues automatically
- Focus only on capturing and organizing the session data
- Let the user decide what to do next with the compiled data
