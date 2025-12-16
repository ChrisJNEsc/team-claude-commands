---
alwaysAllow:
  - WebFetch
  - WebSearch
  - Bash
  - Grep
  - Glob
  - Read
  - Edit
  - Write
---

# Escalation Investigation Workflow

Investigate customer issues → Propose fix → Create Linear ticket

**Rules:**
- Execute all searches automatically (no confirmation needed)
- Stop workflow immediately if answer found in Steps 2-4
- Load shared files only when needed (Law 3: context on demand)
- Run automated QA test (Step 5) before falling back to manual live trace
- Use live trace (Step 5.5) only when QA test passes or is blocked

---

## Step 1: Gather Issue

Ask user for HubSpot URL or issue description. Wait for response.

**If HubSpot URL:** WebFetch to extract: description, troubleshooting done, JN IDs (user/company), date/time, affected record, steps to replicate, expected/actual results, replication status, environment. Present summary. Use AskUserQuestion only for missing critical fields.

**If description only:** Analyze for steps/expected/actual. Use AskUserQuestion if insufficient.

**Detect mobile issue:** Look for keywords: "mobile", "app", "iOS", "iPhone", "iPad", "Android", "phone", "tablet". If mobile detected, determine platform:
- **iOS only** → Need: iOS app version, iOS version
- **Android only** → Need: Android app version, Android OS version
- **Both platforms** → Need: iOS app version, iOS version, Android app version, Android OS version

Proceed automatically.

---

## Step 2: Documentation Search (Parallel)

Run both searches simultaneously:
- `site:support.jobnimbus.com [key terms]`
- `site:jobnimbus.atlassian.net/wiki [key terms]`

**IF ANSWER FOUND → OUTPUT & STOP:**
```
📚 DOCUMENTED BEHAVIOR
Source: [URL]
Finding: [explanation]
Conclusion: [expected behavior / known limitation / config needed]
```

**IF NOT FOUND → Step 3**

---

## Step 3: Linear Search

Search for duplicates:
1. `list_issues` with query terms, limit 15, states: In Progress, Todo, Triage, Backlog
2. Search Done/Canceled from last 90 days
3. `get_issue` for potential matches

**IF DUPLICATE FOUND → OUTPUT & STOP:**
```
🔗 EXISTING ISSUE
ID: [TICKET-ID]
URL: [url]
Status: [state]
Match Confidence: High/Medium/Low
Action: Link customer report to existing issue
```

**IF NO DUPLICATE → Step 4**

---

## Step 4: Code Investigation

**A. Update repos** (parallel git pulls, note failures, continue)

**B. Search code:**
- Error messages → Grep across repos
- Feature/component → Glob + Grep for files, functions, endpoints
- Complex analysis → Task(Explore): trace UI→API→DB for the issue

**C. Document:**
- Repo, files:lines, suspected root cause, confidence (High/Medium/Low)

**If Low confidence or no root cause → Step 4.5, else → Step 5**

---

## Step 4.5: Propose Fix

Based on code investigation findings, analyze and propose a fix:

**A. Identify fix approach:**
- Analyze root cause from Step 4
- Search for similar fixes in git history: `git log --oneline --all --grep="[related terms]"`
- Review how similar issues were resolved

**B. Document proposed fix:**
```
PROPOSED FIX
Files: [file:line] - [change needed]
Approach: [description of fix]
Risks: [potential impacts or side effects]
Tests needed: [scenarios to verify]
Confidence: High/Medium/Low
```

**If no fix can be proposed:** Note "Fix requires further investigation" and continue.

→ Proceed to Step 5

---

## Step 5: Automated QA Test (Conditional)

Only if: Steps to replicate are available AND feature URL can be determined.

**Purpose:** Validate expected behavior automatically before manual investigation.

**A. Determine test parameters from gathered issue:**
- Feature URL (from HubSpot or inferred from feature area)
- User flow (from steps to replicate)
- Expected behavior (from expected result)
- Auth user: Use `defaultUser.json` unless issue specifies permissions/role

**B. Run automated test:**
Using browser MCP tools (Playwright):
1. Navigate to feature URL with `browser_navigate`
2. Take initial snapshot with `browser_snapshot`
3. Execute steps to replicate using `browser_click`, `browser_type`, etc.
4. Capture evidence at each step:
   - Screenshots with `browser_take_screenshot`
   - Console errors with `browser_console_messages`
   - Network failures with `browser_network_requests`
5. Verify expected vs actual behavior

**C. Document QA results:**
```
🧪 AUTOMATED QA TEST
Status: PASS / FAIL / BLOCKED
Steps Executed: [count]
Evidence: [screenshots captured]
Console Errors: [count or None]
Network Failures: [count or None]
Findings: [observations]
```

**D. Decision tree:**
- **FAIL (reproduced issue)** → High confidence, proceed to Step 6
- **PASS (expected behavior works)** → Issue may be data/timing-dependent → Step 5.5
- **BLOCKED (auth/environment issue)** → Step 5.5

---

## Step 5.5: Live Trace (Fallback)

Only if: QA test passed but user reports issue persists, OR QA was blocked, OR timing/race condition suspected.

AskUserQuestion: "Automated test [passed/was blocked]. The issue may be data-specific or intermittent. Capture live trace with your session?"
- **Yes** → Read `~/.claude/commands/escalations/livetrace/watchthis.md`, execute, update findings
- **No** → Continue, note "live trace recommended - issue may be account-specific" for ticket

---

## Step 6: Release Check

For repos from Step 4:
- `gh release list --repo jobnimbus/[repo] --limit 5`
- Recent commits to affected files
- Merged PRs touching the area

Assess regression likelihood: High/Medium/Low/None

---

## Step 7: Create Linear Ticket

**A. Determine team** → Read `~/.claude/commands/escalations/commands/shared/team-mapping.md`

**B. Collect missing fields** via single AskUserQuestion:
- Date/Time, Company JN ID, User JN ID, Affected Record, Priority (1-4)
- **If mobile issue (iOS only):** iOS App Version, iOS Version
- **If mobile issue (Android only):** Android App Version, Android OS Version
- **If mobile issue (both platforms):** iOS App Version, iOS Version, Android App Version, Android OS Version

**C. Create issue** with `create_issue`:

```
team: [from mapping]
title: [concise bug title]
priority: [1-4]
labels: ["Bug - Customer Reported"]
state: "Triage"
description: |
  **Description:** [detailed description of the issue]

  **Date & Time Issue Occurred:** [datetime]
  **Company JN ID:** [company_id]
  **User JN ID:** [user_id]

  <!-- MOBILE SECTION: Include only if mobile issue detected -->
  <!-- For iOS only: -->
  **iOS App Version:** [version]
  **iOS Version:** [version]

  <!-- For Android only: -->
  **Android App Version:** [version]
  **Android OS Version:** [version]

  <!-- For both platforms: -->
  **iOS App Version:** [version]
  **iOS Version:** [version]
  **Android App Version:** [version]
  **Android OS Version:** [version]
  <!-- END MOBILE SECTION -->

  **Replicable in Customer's Account?** [Yes/No/Unknown]
  **Replicable in Test Account?** [Yes/No/Unknown]
  **Test Account Replicated in:** [account name or N/A]
  **Record Replicated with:** [record ID or N/A]

  **Prerequisites:**
  - [prerequisite or N/A]

  **Steps to Replicate:**
  1. [step]
  2. [step]

  **Expected Result:** [expected behavior]

  **Actual Result:** [actual behavior]

  **Steps to View:**
  1. [step to view issue in customer account]
  2. [step]

  **Screenshots:** [None or description]

  **User Recording/Zoom Meeting:** [None or link]

  **Specific Troubleshooting:**
  - [troubleshooting step taken]
  - [findings]

  **Additional Information:**

  **Related Issues:**
  - [TICKET-ID: Title (Status) - brief description]

  ---

  **Code Analysis:**
  - Repo: [name]
  - Files: [file:line, file:line]
  - Root Cause: [analysis]
  - Confidence: [H/M/L]

  **Automated QA Test:**
  - Status: [PASS/FAIL/BLOCKED/SKIPPED]
  - Steps Executed: [count or N/A]
  - Console Errors: [count or None]
  - Network Failures: [count or None]
  - Findings: [observations or N/A]

  **Recent Changes:** [releases/PRs or None]
  **Regression Risk:** [H/M/L/None]

  **Proposed Fix:**
  - Files: [file:line] - [change needed]
  - Approach: [description]
  - Risks: [impacts]
  - Tests needed: [scenarios]
  - Confidence: [H/M/L]
```

**D. Output:**
```
✅ LINEAR TICKET CREATED
ID: [TICKET-ID]
URL: [url]
Branch: [branchName]
Team: [team]

📋 SLACK TEMPLATE:
🔴 New escalation: [TICKET-ID]
Issue: [one-line]
Priority: P[1-4]
Link: [url]
```

---

## Quick Reference (load only if needed)

Team mapping: `~/.claude/commands/escalations/commands/shared/team-mapping.md`
Repo mapping: `~/.claude/commands/escalations/commands/shared/repo-mapping.md`
Repository index: `~/.claude/commands/escalations/livetrace/REPOSITORY_INDEX.md`
QA auth states: `plugins/qa/.auth/*.json` (defaultUser, adminUser, etc.)

---

Begin: Ask for HubSpot URL or issue description.
