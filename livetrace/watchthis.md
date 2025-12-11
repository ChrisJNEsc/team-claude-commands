# Watch This - Chrome Session Monitoring

Start Chrome with enhanced monitoring to investigate JobNimbus issues.

## Your Task:

1. **Ask the user**: "Describe the issue you want to investigate:"
   - Wait for their description
   - Store this context for analysis

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

4. **Wait silently** for the user to perform actions in Chrome

5. **When user says "done"**:
   - **First**: Stop the monitoring script (Ctrl+C or kill the background process)
   - **Then**: Read `/tmp/chrome-live-console.log`
   - Extract key patterns in priority order:
     * Failed API calls (4xx, 5xx status codes)
     * JavaScript errors with stack traces
     * Specific API endpoint paths (e.g., /api/contacts/123)
     * POST/PUT request payloads showing user actions
     * Response bodies with unexpected values
     * Page navigation sequence (URL changes)
   - Identify the PRIMARY error or unexpected behavior first
   - **Consult repository index** (`~/Documents/GitHub/team-claude-commands/livetrace/REPOSITORY_INDEX.md`) to identify relevant repos
   - Map API endpoints and errors to specific repositories:
     * /api/* endpoints → jobnimbus-api (C# backend)
     * Frontend errors → relevant frontend repo based on URL/context
     * Use repository index to find the right repo
   - **Limit initial search to TOP 2-3 most relevant repositories**
   - Use targeted Grep searches for specific endpoint/function names from logs
   - Only read files that directly match the error or endpoint
   - Identify root causes

6. **Ask user for required form fields**:
   - Ask: "What is the Company JN ID?"
   - Ask: "What is the User JN ID?"
   - Ask: "What is the Affected Record?"
   - Store these responses for the bug report form

7. **Deliver** in this exact format:

   **PART 1: Bug Report Form** (at the top) - Fill using this priority:
   - Auto-fill from logs: Description, Date & Time, Steps to Replicate, Expected/Actual Result, Steps to View, Additional Information
   - Use user responses: Company JN ID, User JN ID, Affected Record
   - Extract from session: Test Account Replicated in, Record Replicated with
   - Leave blank: Replicable in Test Account?, Screenshots, User Recording/Zoom Meeting

   ```
   Description: [Brief summary of the issue]
   Date & Time Issue Occurred: [Extract from logs]
   Company JN ID: [Use user's response]
   User JN ID: [Use user's response]
   Affected Record: [Use user's response]


   Replicable in Customer's Account? [Determine from testing]
   Replicable in Test Account?
   Test Account Replicated in: [Extract from session data]
   Record Replicated with: [Extract from session data]


   Prerequisites:
   [Extract prerequisites from log analysis]


   Steps to Replicate:
   [Derive from captured session - numbered steps starting with "Login to JobNimbus on..."]


   Expected Result: [What should happen based on normal behavior]
   Actual Result: [What actually happened from logs]


   Steps to View:
   [Steps to view the issue, derived from session]


   Screenshots:
   User Recording/Zoom Meeting:


   Specific Troubleshooting:
   [List troubleshooting steps attempted or recommended]


   Additional Information:
   [Relevant context from logs, API calls, errors]
   ```

   **PART 2: Technical Analysis** (below the form)
   - Root cause analysis (referencing the original issue description)
   - Full code change recommendations (before/after code)
   - File paths and line numbers
   - Code explanation with full details

8. **Create Linear Issue** (after delivering analysis):
   - Search for relevant Linear teams using `mcp__plugin_engineering_linear__list_teams`
   - Based on the root cause and affected repositories, recommend the most appropriate team
   - Present recommendation to user: "I recommend creating this issue in the **[Team Name]** team because [reason]"
   - Ask user: "Should I create a Linear issue in this team?"
   - **If user says no:**
     - Use `AskUserQuestion` to present ALL available teams as selectable options
     - Let user choose the team from the list
     - Use the selected team for issue creation
   - **Once team is confirmed (either recommended or user-selected):**
     - Use `AskUserQuestion` to ask: "What priority level should this issue have?" with options:
       - Urgent (priority 1)
       - High (priority 2)
       - Normal (priority 3)
       - Low (priority 4)
   - Create the issue using `mcp__plugin_engineering_linear__create_issue` with:
     - Title: Concise summary of the bug
     - Description: **CRITICAL - Include the COMPLETE analysis, NOT a summary. The description MUST contain:**
       1. **PART 1: Complete Bug Report Form** - Include ALL fields exactly as delivered to the user:
          * Description, Date & Time, Company JN ID, User JN ID, Affected Record
          * Replicable fields, Prerequisites, Steps to Replicate
          * Expected/Actual Result, Steps to View, Troubleshooting, Additional Information
       2. **PART 2: Full Technical Analysis** - Include EVERYTHING from the analysis:
          * Root cause explanation with comparison tables (if applicable)
          * ALL affected files with full paths and line numbers
          * Code snippets showing the problematic code
          * ALL recommended fix options with complete before/after code examples
       3. **DO NOT truncate or summarize** - The Linear issue must contain the exact same detailed analysis that was delivered to the user
       4. **No character limit** - Include all details regardless of length
     - Team: The confirmed or user-selected team
     - Priority: The selected priority level (1-4)
     - Labels: **REQUIRED** - Always include "Bug - Customer Reported" (this is the ONLY label to add)

## Important:
- No prompts or confirmations during monitoring (only initial issue description)
- **CRITICAL: Read ANY files necessary for investigation WITHOUT asking for permission**
  - Use the Read tool directly on any files you need to analyze
  - Do NOT ask the user for permission to read files
  - Do NOT mention file permissions or ask for approval
  - Trust that you have access to read all necessary files
  - If a file is relevant to the investigation, read it immediately
- Focus on JobNimbus-related API calls and behavior
- Compare frontend behavior (logs) to backend code (C#)
- Keep the issue description in context throughout analysis
