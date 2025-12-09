---
description: Show status of all my PRs grouped by status with linked Linear issues
permissions:
  - "Bash(gh pr list:*)"
  - "Bash(gh search prs:*)"
  - "Bash(gh api:*)"
  - "Bash(gh repo list:*)"
  - "mcp__plugin_engineering_linear__get_*"
---

# My PR Status Report

Fetch all PRs authored by me across JobNimbus repos and display them grouped by status, with linked Linear issues.

## Steps

1. Run this command to get all my PRs:
```bash
gh pr list --author @me --state all --json number,title,headRepository,url,reviewDecision,state,mergedAt,closedAt,createdAt,headRefName,body --limit 50
```

2. For each PR, extract the Linear issue ID from:
   - Branch name (e.g., `anthonyviglione/sales-458` → `SALES-458`)
   - PR title (e.g., `fix(SALES-458):` → `SALES-458`)
   - PR body (look for `linear.app/jobnimbus/issue/XXX-###` links)

3. Group PRs by status and display in this format:

```
OPEN (needs attention)
  #123 repo-name: PR title
       Linear: SALES-123 | Review: PENDING | Created: 2 days ago

MERGED (last 30 days)
  #456 repo-name: PR title
       Linear: QA-456 | Merged: Dec 8, 2025

CLOSED (not merged, last 30 days)
  #789 repo-name: PR title
       Linear: CORE-789 | Closed: Dec 1, 2025
```

4. For OPEN PRs, also show:
   - Review status: APPROVED, CHANGES_REQUESTED, PENDING, or REVIEW_REQUIRED
   - Any blocking CI checks if available

5. For MERGED/CLOSED, only show PRs from the last 30 days to keep output manageable.

6. If a Linear issue is found, fetch its current status from Linear using:
   - `mcp__plugin_engineering_linear__get_issue` with the issue ID

7. Display Linear issue status alongside PR status to show if they're in sync (e.g., PR merged but issue still "In Progress").
