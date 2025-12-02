# Investigate and Create Customer Request Ticket

Create Linear ticket for customer-reported bug with optional code investigation and fix.

---

## Step 1: Initial Intake (ONE question)

Ask user for ALL of the following in a single prompt:

```
Title: [short, descriptive]
Feature: [what's affected]
Date/Time:
Company JN ID:
User JN ID:
Affected Record:
Replicable in Customer Account? [Y/N]
Replicable in Test Account? [Y/N]
Test Account ID: [if yes]
Record Replicated: [if yes]
Prerequisites: [or None]
Steps to Replicate: [start with "Login to JobNimbus on..."]
Expected Result:
Actual Result:
Steps to View: [or "Same as replication"]
Screenshots: [URLs or None]
Recording/Zoom: [URLs or None]
Troubleshooting Done: [or None]
Additional Info: [or None]
---
Options (Y/N for each):
- Investigate code?
- Implement fix after ticket creation?
```

---

## Step 2: Duplicate Check (parallel)

Extract key terms → `list_issues` with `query`, `limit: 10`, `updatedAt: -P30D`

**If matches found:** Show ID, title, status, URL, confidence (High/Medium/Low). Ask: "Duplicate? (yes=stop, no=continue)"

**If no matches:** Continue.

---

## Step 3: Team & Priority (AI decides, user confirms)

Infer team from feature. **Only read `shared/team-mapping.md` if unclear.**

Priority: P1=blocking/critical | P2=significant | P3=standard | P4=minor

Present: "Team: [X], Priority: [Y]. Correct? (or specify override)"

---

## Step 4: Code Investigation (if opted in)

### 4a. Identify Repos
Read `shared/repo-mapping.md` → lookup feature → get repo(s) + path hints.

**Skip exploration if mapping gives clear path.** Only use Task(Explore) if:
- Feature not in mapping
- Path hint doesn't yield results
- Need to trace cross-repo dependencies

### 4b. Investigate (parallel if multiple repos)
Use path hints to go directly to relevant files. Present per repo:
Repository | Type | Confidence | Files:lines | How it relates

### 4c. Fix Scope
Classify: `Frontend-only` | `Backend-only` | `Full-stack`

### 4d. Fix Plan (if scope identified)
Per affected repo: Root cause | Solution | Files to modify | Risks | Tests

### 4e. Confidence Assessment

| Factor | Value |
|--------|-------|
| Root Cause | Yes/Partially/No |
| Solution Clarity | Clear/Needs Validation/Uncertain |
| Scope | Isolated/Moderate/Wide-reaching |
| Test Coverage | Good/Partial/None |
| **Overall** | **High/Medium/Low** |

High=proceed | Medium=may iterate | Low=recommend manual validation first

---

## Step 5: Preview & Create

1. Compile ticket using template below
2. Save to `/tmp/linear-issue-preview.md` and `open` it
3. Ask: "Create this ticket? (yes/edit/cancel)"
4. Create with: `state: Triage`, `label: Bug - Customer Reported`
5. Display: ticket ID, URL, branch name

---

## Step 6: Implementation (if opted in)

Reference confidence from 4e. For full-stack: ask "Backend-first, frontend-first, or parallel?"

### Frontend (jobnimbus-frontend)
```bash
cd ~/Documents/GitHub/jobnimbus-frontend && git checkout main && git pull && git checkout -b [branch]
# implement fix
npx nx run [project]:lint && npx nx run [project]:typecheck
# test via import-map-override on dev.jobnimbus.com
git add . && git commit -m "[type]([ID]): [desc]" && git push -u origin [branch]
gh pr create --title "[ID]: [desc] (Frontend)" --body "[summary + test plan + linear link]"
```

### Backend (dotnet-monolith or other)
```bash
cd ~/Documents/GitHub/[repo] && git checkout main && git pull && git checkout -b [branch]
# implement fix
dotnet build && dotnet test  # or npm run build && npm test
git add . && git commit -m "[type]([ID]): [desc]" && git push -u origin [branch]
gh pr create --title "[ID]: [desc] (Backend)" --body "[summary + test plan + linear link]"
```

### Post to Linear
Add comment with: Confidence assessment | Root cause | Solution | Files changed (FE/BE) | Test results table | PR links | Deployment notes

---

## Ticket Template

```
**Description:** [Feature]
**Date/Time:** [When]
**Company JN ID:** [ID] | **User JN ID:** [ID]
**Affected Record:** [Record]

**Replication:**
- Customer Account: [Y/N]
- Test Account: [Y/N] → [Account ID] → [Record]

**Prerequisites:** [or None]

**Steps to Replicate:**
[Steps]

**Expected:** [Result]
**Actual:** [Result]

**Steps to View:** [or Same as replication]

**Attachments:** Screenshots: [URLs] | Recording: [URLs]
**Troubleshooting:** [Done or None]
**Additional:** [Info or None]

---

## Code Investigation

**Fix Scope:** [Frontend-only / Backend-only / Full-stack / N/A]

### Frontend
Repo: [name] | Confidence: [H/M/L] | Files: [paths:lines]
Analysis: [explanation]

### Backend
Repo: [name] | Confidence: [H/M/L] | Files: [paths:lines]
Analysis: [explanation]

### Confidence: [High/Medium/Low]
Root Cause: [Y/P/N] | Clarity: [C/V/U] | Scope: [I/M/W] | Tests: [G/P/N]

## Fix Plan

### Frontend
Root Cause: [analysis]
Solution: [approach]
Files: [list]
Risks: [details]
Tests: [recommendations]

### Backend
Root Cause: [analysis]
Solution: [approach]
Files: [list]
Risks: [details]
Tests: [recommendations]

**Deploy Order:** [Backend-first / Frontend-first / Parallel / N/A]
```

---

## Rules
- Batch questions → minimize interactions
- Parallel tool calls when no dependencies
- Load team-mapping.md only when team unclear
- State=Triage, Label=Bug - Customer Reported
- N/A for skipped sections
