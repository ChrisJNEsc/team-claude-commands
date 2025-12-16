---
description: Bug analysis with subagent architecture (context-optimized)
allowed-tools:
  - Read
  - Write
  - Task
  - AskUserQuestion
  - mcp__plugin_engineering_linear__create_issue
  - mcp__plugin_engineering_linear__update_issue
  - mcp__plugin_engineering_linear__list_teams
---

# Escalation Orchestrator

Lightweight orchestrator that delegates heavy work to subagents. Each subagent updates a shared JSON file.

**Context budget:** Main agent stays under 50k tokens by delegating browser, search, and code analysis to subagents.

## Setup

Create state file:
```bash
export ESC_JSON="/tmp/escalation-$(date +%s).json"
```

Initialize JSON:
```json
{
  "id": "escalation-[timestamp]",
  "status": "in_progress",
  "input": { "raw": "$ARGUMENTS", "source": null },
  "extracted": {},
  "p1_quick_checks": { "status": "pending" },
  "p2_reproduction": { "status": "pending" },
  "p3_code_investigation": { "status": "pending" },
  "finding": {},
  "ticket": {}
}
```

Write to `$ESC_JSON`.

---

## Phase 0: Input Processing

**If $ARGUMENTS is empty:** Ask "Describe the bug or paste HubSpot URL"

**If HubSpot URL detected:**
```
Task(subagent_type: "general-purpose", prompt: "
  Read ./commands/escalate-v2/subagents/p0-hubspot-extract.md for instructions.
  JSON file: [ESC_JSON path]
  HubSpot URL: [URL]
  Extract issue details and update the JSON file.
")
```

**If plain description:** Parse locally for IDs, datetime, feature area. Update `extracted` section.

**Read JSON** to confirm `extracted` is populated. If missing critical fields, use AskUserQuestion.

---

## Phase 1: Quick Checks

```
Task(subagent_type: "general-purpose", prompt: "
  Read ./commands/escalate-v2/subagents/p1-quick-checks.md for instructions.
  JSON file: [ESC_JSON path]
  Search for duplicates and documentation. Update the JSON file.
")
```

**Read JSON** `p1_quick_checks`:

- **If `duplicate.found` = true AND `duplicate.match_confidence` = "high":**
  Update JSON: `finding.type = "duplicate"`
  Output: `🔗 DUPLICATE: [issue_id] - [title]\n[url]`
  Delete JSON. **STOP.**

- **If `documented.found` = true:**
  Update JSON: `finding.type = "documented"`
  Output: `📚 DOCUMENTED: [summary]\n[url]`
  Delete JSON. **STOP.**

- **Otherwise:** Continue to Phase 2.

---

## Phase 2: Reproduction

**Pre-check:** Verify `extracted.steps_to_replicate` exists. If not, skip to Phase 3 with note.

```
Task(subagent_type: "qa-specialist", prompt: "
  Read ./commands/escalate-v2/subagents/p2-reproduction.md for instructions.
  JSON file: [ESC_JSON path]
  Attempt to reproduce the bug in dev environment. Update the JSON file.
")
```

**Read JSON** `p2_reproduction`:

- **If `status` = "blocked":** Note for ticket, continue to Phase 3.
- **If `reproduced` = false:** Set `finding.type` = "cannot_reproduce", skip to Phase 4.
- **If `reproduced` = true:** Continue to Phase 3.

---

## Phase 3: Code Investigation

**Pre-check:** Read JSON, confirm `p2_reproduction.status` is not "pending".

```
Task(subagent_type: "Explore", prompt: "
  Read ./commands/escalate-v2/subagents/p3-code-investigation.md for instructions.
  JSON file: [ESC_JSON path]
  Find root cause and propose fix. Update the JSON file.
")
```

**Read JSON** `p3_code_investigation` for root cause and fix.

---

## Phase 4: Compile Finding

**Read full JSON.** Synthesize:

```json
{
  "finding": {
    "type": "duplicate|documented|new|cannot_reproduce",
    "summary": "[1-2 sentence summary]",
    "recommendation": "create_ticket|needs_more_info|close"
  }
}
```

**Present to user:**
```
## [summary]

**Type:** [finding.type]
**Reproduced:** [p2_reproduction.reproduced]
**Root Cause:** [p3_code_investigation.root_cause]
**Location:** [p3_code_investigation.location]
**Confidence:** [p3_code_investigation.confidence]

**Proposed Fix:**
[p3_code_investigation.code_fix.approach]

Files:
- [file:line] - [change]

**Risks:** [risks]
**Tests:** [tests_needed]
```

---

## Phase 5: User Confirmation

AskUserQuestion: "Create Linear ticket?"
- Options: "Yes", "No", "Need changes"

- **If "Need changes":** Ask what to change, update `finding`, re-present.
- **If "No":** Delete JSON. **STOP.**
- **If "Yes":** Continue to Phase 6.

---

## Phase 6: Ticket Creation

**Read JSON** for all context.

**Determine team:** Read `./commands/escalate-v2/shared/team-mapping.md`
Match `extracted.feature_area` to team.

**Collect missing fields** via AskUserQuestion (single prompt):
- Priority (1-4)
- Any missing: Company ID, User ID, Record ID

**Create issue:**
```
create_issue({
  team: "[mapped team]",
  title: "[concise title from finding.summary]",
  priority: [1-4],
  labels: ["Bug - Customer Reported"],
  state: "Triage",
  description: "[Build from JSON - see template below]"
})
```

**Description template:**
```markdown
**Description:** [finding.summary]

**Date & Time Issue Occurred:** [extracted.datetime]
**Company JN ID:** [extracted.company_id]
**User JN ID:** [extracted.user_id]

<!-- MOBILE SECTION: Include only if extracted.is_mobile = true -->
<!-- For iOS only (extracted.mobile_platform = "ios"): -->
**iOS App Version:** [extracted.ios_app_version]
**iOS Version:** [extracted.ios_version]

<!-- For Android only (extracted.mobile_platform = "android"): -->
**Android App Version:** [extracted.android_app_version]
**Android OS Version:** [extracted.android_version]

<!-- For both platforms (extracted.mobile_platform = "both"): -->
**iOS App Version:** [extracted.ios_app_version]
**iOS Version:** [extracted.ios_version]
**Android App Version:** [extracted.android_app_version]
**Android OS Version:** [extracted.android_version]
<!-- END MOBILE SECTION -->

**Replicable in Customer's Account?** [extracted.replicable_in_customer_account or "Unknown"]
**Replicable in Test Account?** [p2_reproduction.reproduced ? "Yes" : "No" or "Unknown"]
**Test Account Replicated in:** [p2_reproduction.environment or "N/A"]
**Record Replicated with:** [extracted.record_id or "N/A"]

**Prerequisites:**
- [extracted.prerequisites or "N/A"]

**Steps to Replicate:**
[extracted.steps_to_replicate as numbered list]

**Expected Result:** [extracted.expected_result]

**Actual Result:** [extracted.actual_result]

**Steps to View:**
[extracted.steps_to_view as numbered list or "N/A"]

**Screenshots:** [p2_reproduction.screenshot_paths or "None"]

**User Recording/Zoom Meeting:** [extracted.recording_url or "None"]

**Specific Troubleshooting:**
- [extracted.troubleshooting_steps or "N/A"]

**Additional Information:** [extracted.additional_info or "N/A"]

**Related Issues:**
- [p1_quick_checks.duplicate.issue_id if partial match: "TICKET-ID: Title (Status) - brief description"]

---

**Code Analysis:**
- Repo: [p3_code_investigation.repo]
- Files: [p3_code_investigation.location]
- Root Cause: [p3_code_investigation.root_cause]
- Confidence: [p3_code_investigation.confidence - H/M/L]

**Automated QA Test:**
- Status: [p2_reproduction.status - PASS/FAIL/BLOCKED/SKIPPED]
- Steps Executed: [p2_reproduction.steps_executed or "N/A"]
- Console Errors: [p2_reproduction.console_errors.length or "None"]
- Network Failures: [p2_reproduction.network_errors.length or "None"]
- Findings: [p2_reproduction.findings or "N/A"]

**Recent Changes:** [p3_code_investigation.related_commits or "None"]
**Regression Risk:** [p3_code_investigation.regression_risk or "None"]

**Code Fix:**
\`\`\`[language from p3_code_investigation.code_fix.language]
// File: [path]:[line]
[p3_code_investigation.code_fix.full_code - complete function/method with fix applied]
\`\`\`

**Implementation Notes:**
- Risks: [p3_code_investigation.code_fix.risks]
- Tests needed: [p3_code_investigation.code_fix.tests_needed]
- Confidence: [p3_code_investigation.confidence - H/M/L]
```

**Output:**
```
✅ [TICKET-ID]: [title]
Team: [team] | Priority: P[n]
URL: [url]
Branch: [branchName]

📋 Slack: 🔴 New escalation: [TICKET-ID] - [one-line summary] P[n] [url]
```

**Cleanup:** Delete JSON file.

---

## Error Recovery

If any subagent fails:
1. Read JSON to check what completed
2. Note the failure in `finding`
3. Present partial findings to user
4. Offer to create ticket with available info or retry failed phase
