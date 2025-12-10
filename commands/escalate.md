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

Investigate customer issues → Create Linear ticket → [Optional] Fix & PR

**Rules:**
- Execute all searches automatically (no confirmation needed)
- Stop workflow immediately if answer found in Steps 2-4
- Load shared files only when needed (Law 3: context on demand)

---

## Step 1: Gather Issue

Ask user for HubSpot URL or issue description. Wait for response.

**If HubSpot URL:** WebFetch to extract: description, troubleshooting done, JN IDs (user/company), date/time, affected record, steps to replicate, expected/actual results, replication status, environment. Present summary. Use AskUserQuestion only for missing critical fields.

**If description only:** Analyze for steps/expected/actual. Use AskUserQuestion if insufficient.

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

## Step 4.5: Live Trace (Conditional)

Only if: Low confidence OR no code found OR timing/race condition issue.

AskUserQuestion: "Code investigation inconclusive. Capture live trace?"
- **Yes** → Read `~/.claude/commands/escalations/livetrace/watchthis.md`, execute, update findings
- **No** → Continue, note "live trace recommended" for ticket

---

## Step 5: Release Check

For repos from Step 4:
- `gh release list --repo jobnimbus/[repo] --limit 5`
- Recent commits to affected files
- Merged PRs touching the area

Assess regression likelihood: High/Medium/Low/None

---

## Step 6: Create Linear Ticket

**A. Determine team** → Read `~/.claude/commands/escalations/commands/shared/team-mapping.md`

**B. Collect missing fields** via single AskUserQuestion:
- Date/Time, Company JN ID, User JN ID, Affected Record, Priority (1-4)

**C. Create issue** with `create_issue`:

```
team: [from mapping]
title: [concise bug title]
priority: [1-4]
labels: ["Bug - Customer Reported"]
state: "Triage"
description: |
  **Issue:** [summary]

  **Customer:** Company [ID] | User [ID] | Record [ID] | Date [datetime]

  **Replication:** Customer: [Y/N] | Test: [Y/N] | Account: [name or N/A]

  **Steps:**
  1. [step]
  2. [step]

  **Expected:** [result]
  **Actual:** [result]

  **Code Analysis:**
  - Repo: [name]
  - Files: [file:line, file:line]
  - Root Cause: [analysis]
  - Confidence: [H/M/L]

  **Recent Changes:** [releases/PRs or None]
  **Regression Risk:** [H/M/L/None]

  **Troubleshooting Done:** [steps taken]
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

**Ask: "Implement fix and create PR?"**

---

## Step 7: Fix & PR (Optional)

Only if user confirms.

**A. Propose fix first:**
```
PROPOSED FIX
Files: [file:line] - [change]
Risks: [impacts]
Tests needed: [scenarios]
```
Wait for approval.

**B. Implement:**
1. Load `engineering:jobnimbus-standards` skill
2. Branch: `support/[LINEAR-ID]-[desc]`
3. Minimal changes, match existing style
4. Run lint/test/build
5. Commit with Linear reference

**C. PR Confidence Summary (before posting):**

Present summary for validation before pushing/posting:

```
📊 PR CONFIDENCE SUMMARY

**PR:** #[num] - [title]
**Branch:** support/[ID]-[desc]
**Files Changed:** [count]

| Metric | Score | Reasoning |
|--------|-------|-----------|
| Relevance | [X]% | [why this PR addresses the reported issue] |
| Regression Risk | [Y]% | [likelihood this fix introduces new issues] |

**Changes:**
- [file:line] - [change description]
- [file:line] - [change description]

**Test Coverage:** [description of tests run/added]
**Risk Factors:** [any concerns or edge cases]
```

**Ask: "Post this PR?"**
- **Yes** → Push branch, create PR, link to Linear, then cleanup (checkout main, delete local branch)
- **No** → Keep changes local for manual review

**D. Output (after posting):**
```
✅ FIX COMPLETE
Linear: [ID] - [url]
PR: #[num] - [pr-url]
Branch: support/[ID]-[desc]

Next: PR review → Merge → Verify → Close issue
```

---

## Quick Reference (load only if needed)

Team mapping: `~/.claude/commands/escalations/commands/shared/team-mapping.md`
Repo mapping: `~/.claude/commands/escalations/commands/shared/repo-mapping.md`
Repository index: `~/.claude/commands/escalations/livetrace/REPOSITORY_INDEX.md`

---

Begin: Ask for HubSpot URL or issue description.
