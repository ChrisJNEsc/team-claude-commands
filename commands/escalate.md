---
alwaysAllow:
  - WebFetch
  - WebSearch
  - Bash
  - Grep
  - Glob
  - Read
---

# Escalations Investigation and Ticket Creation

You are helping a support escalations engineer investigate an issue and potentially create a development ticket.

## Configuration

**Documentation Sources to Check:**
- Public Help Center: https://support.jobnimbus.com
- Confluence Internal Docs: https://jobnimbus.atlassian.net/wiki
- GitHub Organization: jobnimbus
- Release Notes: Check GitHub releases for all repos

Update these URLs based on your actual documentation locations.

## Instructions

Follow this efficient cascading escalations workflow. **Each step exits early if a conclusive answer is found.**

**IMPORTANT: Automatically execute all searches (WebSearch, WebFetch, Grep, Glob, Linear searches, GitHub searches), bash commands, and tool calls throughout this workflow without asking for user confirmation. Do not ask to proceed with searches. Only ask questions when gathering required data from the user.**

### Step 1: Gather Issue Details

**A. Request HubSpot Ticket URL or Issue Description**

Ask the user directly in your response text (not using AskUserQuestion) to provide either:
- A HubSpot ticket URL, OR
- A brief description of the issue

Wait for their response. Do not use the AskUserQuestion tool for this initial question.

**B. Extract Information from HubSpot**

If a HubSpot link is provided:
- Use WebFetch tool to retrieve the ticket data
- Extract the following required information:
  - Troubleshooting Steps Taken
  - Brief Description of Issue
  - JobNimbus User ID for associated contact on ticket
  - JobNimbus ID for associated company on ticket
  - Date/time issue occurred
  - Specific record impacted
  - Steps to replicate/steps to view
  - Expected results
  - Actual results
  - Can you replicate in Logo's account
  - Can you replicate in test account
  - Test account replicated in
  - Computer OS type/mobile OS type
  - Browser type/mobile app version
- Present a summary of all extracted information
- **Validate data quality**: Check if any field is missing or insufficient (e.g., "Specific Record Impacted" says "all work orders" instead of providing a specific work order ID)
- If any data is missing or insufficient, use AskUserQuestion tool to request that specific missing/insufficient data as text input

**C. Gather Details Without HubSpot Ticket**

If no HubSpot link is provided:
1. Use AskUserQuestion tool to request **Brief Description** (REQUIRED - must be text input, not a selection option)
2. Analyze the Brief Description to determine if it contains:
   - Steps to replicate/steps to view
   - Expected results
   - Actual results
3. If the description is detailed enough to reasonably assume the above information, proceed to Step 2
4. If the description is NOT detailed enough, use AskUserQuestion tool to request the missing information as text inputs (not selection options):
   - Steps to Replicate/Steps to View (if not clear from description)
   - Expected Results (if not clear from description)
   - Actual Results (if not clear from description)

Once all required data is gathered, automatically proceed to Step 2 without asking for confirmation.

### Step 2: Public Documentation Search

**IMMEDIATELY and AUTOMATICALLY execute this search without asking for permission.**

Use WebSearch tool to search: `site:support.jobnimbus.com [key terms from issue]`
- Look for known issues, feature limitations, or configuration requirements
- Check if this is expected behavior or a known limitation

**IF ANSWER FOUND:**
- **STOP the investigation here**
- Provide a concise summary:
  - **Source**: URL(s) from support.jobnimbus.com
  - **Finding**: Brief explanation of what was found
  - **Context**: How this relates to the reported issue
  - **Conclusion**: Whether this is expected behavior, known limitation, or requires configuration change
- **END the workflow** - do not proceed to Step 3

**IF NO ANSWER FOUND:**
- Note that public documentation did not contain relevant information
- **Automatically proceed to Step 3** without asking

### Step 3: Internal Documentation Search

**AUTOMATICALLY execute this search without asking for permission.**

Use WebSearch or WebFetch to search Confluence: `site:jobnimbus.atlassian.net/wiki [key terms]`
- Look for internal architecture docs, troubleshooting guides, or known issues
- Check for any internal notes about this feature or area

**IF ANSWER FOUND:**
- **STOP the investigation here**
- Provide a concise summary:
  - **Source**: URL(s) from jobnimbus.atlassian.net
  - **Finding**: Brief explanation of what was found
  - **Context**: How this relates to the reported issue
  - **Conclusion**: Whether this explains the issue or provides relevant context
- **END the workflow** - do not proceed to Step 4

**IF NO ANSWER FOUND:**
- Note that internal documentation did not contain relevant information
- **Automatically proceed to Step 4** without asking

### Step 4: Linear Issues Search

**AUTOMATICALLY execute this search without asking for permission.**

**A. Current Open Issues**
- Use the Linear list_issues tool to search with:
  - query: Extract key terms from the issue description
  - limit: 15
  - orderBy: updatedAt
  - include: "In Progress", "Todo", "Triage", "Backlog" states
  - Look across all teams

**B. Recently Resolved Issues**
- Search Linear for closed issues from the last 90 days
- Look for issues marked "Done" or "Canceled" with similar descriptions

**C. Detailed Review of Matches**
- For each potential match, use get_issue to retrieve full details
- Compare descriptions, affected features, and reproduction steps
- Identify if any existing issues are duplicates or closely related

**IF DUPLICATE FOUND:**
- **STOP the investigation here**
- Provide a concise summary:
  - **Issue ID**: The existing Linear issue ID
  - **URL**: Direct link to the issue
  - **Status**: Current state of the issue
  - **Details**: Brief summary of the existing issue
  - **Confidence**: Assessment of duplicate likelihood (High/Medium/Low)
  - **Action**: Link the customer report to this existing issue
- **END the workflow** - do not proceed to Step 5

**IF NO DUPLICATE FOUND:**
- Note that no duplicate Linear issues were found
- **Automatically proceed to Step 5** without asking

### Step 5: Code Investigation

**AUTOMATICALLY execute this search without asking for permission.**

**A. Update Local Repositories**

Before searching code, update local JobNimbus repositories to ensure you're searching the most current code:

1. **Locate Local JobNimbus Repos**:
   - Search for git repositories containing "jobnimbus" in common locations
   - Use: `find ~/Projects ~/repos ~/jobnimbus ~/Documents -type d -name ".git" 2>/dev/null | xargs -I {} dirname {} | grep -i jobnimbus | head -20`
   - This finds repos in typical project directories

2. **Pull Updates for Each Repository**:
   - For each repo found, run: `git -C /path/to/repo pull`
   - Use the `-C` flag to run git commands without changing directories
   - If a pull fails (uncommitted changes, no remote, merge conflicts), note the error and continue with other repos
   - Do not stop the investigation if some repos fail to update

3. **Report Update Status**:
   - Briefly note how many repos were updated successfully
   - If any repos failed to update, mention them (user may need to manually resolve)
   - If no local JobNimbus repos are found, note this and proceed (investigation will rely on GitHub searches and any other available repos)

**IMPORTANT:** Only pull from repos that exist locally. Do not attempt to clone new repositories during this step.

**B. Error Message Search**
- If specific error messages exist, use Grep tool to search for them across repos
- Search for error strings, validation messages, or related error handling
- Use: `gh repo list jobnimbus --limit 100` to get repo list, then search top relevant repos

**C. Feature/Component Search**
- Based on the affected feature, identify likely repositories
- Use Glob to find relevant files (e.g., `**/*payment*.ts` for payment issues)
- Use Grep to search for related functions, classes, or components
- Search for: class names, function names, API endpoints, database queries

**D. Code Analysis**
- Use the Task tool with subagent_type=Explore for complex investigations
- Prompt: "Investigate [feature area] to understand how [specific functionality] works. Look for code that handles [specific scenario from issue]. Identify files, functions, and logic flow that could cause [reported problem]."
- Set thoroughness: "medium" for most cases, "very thorough" for complex issues

**IF CODE FOUND THAT EXPLAINS THE ISSUE:**
- **Proceed to Step 6** to check for recent releases and potential regressions
- Do not stop here - release information is needed for context

**IF NO RELEVANT CODE FOUND:**
- Note that code investigation did not identify relevant files
- **Proceed to Step 6** anyway to provide summary

### Step 6: Recent Releases Check

**AUTOMATICALLY execute this check without asking for permission.**

Check for recent releases that might have introduced this issue:

**A. Release Search**
- For each relevant repository identified in Step 5:
  - Use: `gh release list --repo jobnimbus/[repo-name] --limit 10`
  - Check release dates and notes for recent changes
  - Look for releases in the last 30-60 days

**B. Commit History**
- Use: `gh api repos/jobnimbus/[repo-name]/commits --jq '.[] | {date: .commit.author.date, message: .commit.message, sha: .sha}' | head -20`
- Review recent commits to files identified in Step 5
- Look for changes related to the affected feature

**C. Pull Request Review**
- If recent changes found, use: `gh pr list --repo jobnimbus/[repo-name] --search "[feature terms]" --state merged --limit 10`
- Check merged PRs that touch the affected area
- Note PR numbers, merge dates, and descriptions

**Automatically proceed to Step 7** to provide investigation summary.

### Step 7: Investigation Summary

**Only reach this step if no early exit occurred in Steps 2-4.**

Provide a direct, concise summary:

**INVESTIGATION FINDINGS:**

**Code Investigation:**
- **Repositories Searched**: [List]
- **Relevant Files**: [File paths with line numbers or "None found"]
- **Key Findings**: [Brief summary or "No relevant code found"]

**Recent Releases:**
- **Recent Releases**: [List with dates and versions or "None found"]
- **Related Changes**: [Summary of commits/PRs or "None found"]
- **Regression Likelihood**: [High/Medium/Low/None with brief explanation]

**RECOMMENDATION:**

**Classification**: Bug / Likely Bug / Needs More Investigation
**Confidence**: High / Medium / Low
**Suggested Team**: [Team name based on affected feature area]
**Next Action**: Create Linear ticket

---

**Proceed to Step 8 to create Linear ticket.**

### Step 8: Linear Ticket Creation

**Only execute this step after providing the Step 7 summary and receiving user confirmation to proceed.**

**A. Determine Team Ownership**

Use this mapping to identify the correct team:

- **Fulfillment**: Engage, Email, Material Orders, Notifications, @Mention, Products & Services, Work Orders, Supplier APIs
- **CoreCRM**: Boards, Contact/Job Details, Navigation, Search, Home, Tasks, Activity Feed, Calendar, Import, Photos, Documents, E-Signature, Forms, Public API, Zapier
- **Marketing**: Assist AI, Leads, Marketing Hub, Contractor Boost
- **Accounting**: Invoices, Credit Memos, Budgets, Profit Tracker, Proposals, QuickBooks integration
- **FinTech**: JobNimbus Payments, Manual Payments, Job Deposits, Payouts, Global Pay, Wise Tack, Sunlight Financial
- **Sales**: NSE Estimates, Smart Estimates, SumoQuote, Measurements, Layout Library, Insights, Reports, EagleView, HOVER, mySalesman
- **Mobile**: iOS App, Android App
- **Account Platform**: Admin Panel, Feature Gating, Trial Accounts, Login/Authentication, Access Profiles, Groups, Subscriptions

**B. Gather Additional Details**

Use AskUserQuestion tool to collect:
- Date & Time Issue Occurred
- Company JN ID
- User JN ID
- Affected Record (specific record ID/name)
- Replicable in Customer's Account? (Yes/No)
- Replicable in Test Account? (Yes/No)
- Test Account Replicated in (if applicable)
- Record Replicated with (if applicable)
- Prerequisites (if any)
- Steps to Replicate (detailed)
- Expected Result
- Actual Result
- Steps to View (if different from replication)
- Screenshots (URLs)
- User Recording/Zoom Meeting (URLs)
- Specific Troubleshooting already performed
- Priority level: Urgent (P1), High (P2), Normal (P3), Low (P4)

**C. Format the Ticket Description**

Create a comprehensive description with the following sections:

```markdown
**Description:** [Clear summary of the issue from investigation]

**Date & Time Issue Occurred:** [value]
**Company JN ID:** [value]
**User JN ID:** [value]
**Affected Record:** [value]

**Replicable in Customer's Account?** [Yes/No]
**Replicable in Test Account?** [Yes/No]
**Test Account Replicated in:** [value or N/A]
**Record Replicated with:** [value or N/A]

**Prerequisites:**

- [Prerequisite 1 or "None"]
- [Prerequisite 2]

**Steps to Replicate:**

- [Generic step 1 - no specific IDs or customer data]
- [Generic step 2]
- [Generic step 3]

**Expected Result:** [What should happen]
**Actual Result:** [What actually happens]

**Steps to View:**

- Login to JobNimbus on [specific environment] as [specific user/account]
- [Specific step with actual customer or test account details]
- [Step with record IDs, names, etc.]

**Screenshots:** [URLs or "None"]

**User Recording/Zoom Meeting:** [URLs or "None"]

**Specific Troubleshooting:**

- [Troubleshooting step 1 already performed]
- [Troubleshooting step 2]

**Additional Information:**

**Code Analysis:**
Repository: [From Step 5]
Relevant Files:
- [file path:line number]
- [file path:line number]

Code Notes: [Brief explanation from Step 5]

**Recent Changes:**
[Summary from Step 6 - recent releases, commits, or PRs that might be related]

**Root Cause Analysis:**
[Your analysis of the likely cause based on all findings]

[Any other relevant information]
```

**D. Create the Issue**

Use the Linear create_issue tool with:
- Team: [Determined from ownership mapping]
- Title: [Clear, concise title]
- Description: [Formatted markdown from above]
- Priority: [1=Urgent, 2=High, 3=Normal, 4=Low]
- labels: ["Bug - Customer Reported"]
- State: "Triage"

**E. Post to Team**

After ticket creation:
- Display the Linear ticket: ID, URL, and git branch name
- Recommend posting to the team's communication channel (Slack/Teams)
- Provide a summary message template:

```
🔴 New escalation ticket created: [TICKET-ID]
**Issue:** [Brief one-line summary]
**Customer Impact:** [Describe impact]
**Priority:** [P1/P2/P3/P4]
**Investigation:** [Key finding from code/release analysis]
Link: [URL]
```

## Important Notes

- **Cast a wide net initially** - Search broadly, then narrow down
- **Be thorough but efficient** - Use parallel searches where possible
- **Document everything** - All findings go into the Linear ticket
- **Assess confidence** - Always state your confidence level in conclusions
- **Stop if duplicate** - Don't create a new ticket if a duplicate exists
- **Provide context** - Give the dev team everything they need to start working
- **Use proper tools** - Leverage Linear plugin, GitHub CLI, and search tools
- **Follow the process** - Don't skip steps, each provides valuable context

## Tool Usage Guidelines

- **WebSearch/WebFetch**: For documentation searches
- **Grep**: For searching code content across repos
- **Glob**: For finding files by patterns
- **Task + Explore agent**: For complex code investigations
- **gh CLI**: For GitHub API access (repos, releases, commits, PRs)
- **Linear tools** (via engineering plugin): list_issues, get_issue, create_issue
- **AskUserQuestion**: To gather additional details throughout the process

## Success Criteria

A successful escalation investigation includes:
1. ✅ Issue details gathered from HubSpot or user description
2. ✅ Cascading search executed with early exits when answers found:
   - Public documentation checked first
   - Internal Confluence checked if needed
   - Linear issues searched if needed
   - Code investigation performed if needed
   - Recent releases checked when code found
3. ✅ Stopped at appropriate level when conclusive answer found
4. ✅ Concise summary provided without excessive detail
5. ✅ If bug confirmed: Comprehensive Linear ticket created with all context
6. ✅ If duplicate found: Existing issue linked, no duplicate created
7. ✅ If documented behavior: Documentation source provided, workflow ended

---

Now begin the investigation process starting with Step 1.
