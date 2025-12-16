# Linear Ticket Template

Use this template when creating Linear issues for bug reports.

## Issue Parameters

```
team: [from team-mapping.md]
title: [concise bug title]
priority: [1-4]
labels: ["Bug - Customer Reported"]
state: "Triage"
```

## Description Template

```markdown
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

**Code Fix:**
\`\`\`[language]
// File: [file:line]
[actual code fix - full function/method with changes applied]
\`\`\`

**Implementation Notes:**
- Risks: [impacts]
- Tests needed: [scenarios]
- Confidence: [H/M/L]
```

## Output Template

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

## Field Mapping from JSON State

When using with `/escalate-v2`, map JSON fields as follows:

| Template Field | JSON Source |
|----------------|-------------|
| Description | `finding.summary` |
| Date & Time Issue Occurred | `extracted.datetime` |
| Company JN ID | `extracted.company_id` |
| User JN ID | `extracted.user_id` |
| iOS App Version | `extracted.ios_app_version` |
| iOS Version | `extracted.ios_version` |
| Android App Version | `extracted.android_app_version` |
| Android OS Version | `extracted.android_version` |
| Replicable in Customer's Account | `extracted.replicable_in_customer_account` |
| Replicable in Test Account | `p2_reproduction.reproduced` |
| Test Account Replicated in | `p2_reproduction.environment` |
| Record Replicated with | `extracted.record_id` |
| Prerequisites | `extracted.prerequisites` |
| Steps to Replicate | `extracted.steps_to_replicate` |
| Expected Result | `extracted.expected_result` |
| Actual Result | `extracted.actual_result` |
| Steps to View | `extracted.steps_to_view` |
| Screenshots | `p2_reproduction.screenshot_paths` |
| User Recording/Zoom Meeting | `extracted.recording_url` |
| Specific Troubleshooting | `extracted.troubleshooting_steps` |
| Additional Information | `extracted.additional_info` |
| Related Issues | `p1_quick_checks.duplicate.issue_id` (if partial match) |
| Repo | `p3_code_investigation.repo` |
| Files | `p3_code_investigation.location` |
| Root Cause | `p3_code_investigation.root_cause` |
| Confidence | `p3_code_investigation.confidence` |
| Automated QA Test Status | `p2_reproduction.status` |
| Steps Executed | `p2_reproduction.steps_executed` |
| Console Errors | `p2_reproduction.console_errors` |
| Network Failures | `p2_reproduction.network_errors` |
| Findings | `p2_reproduction.findings` |
| Recent Changes | `p3_code_investigation.related_commits` |
| Regression Risk | `p3_code_investigation.regression_risk` |
| Code Fix (language) | `p3_code_investigation.code_fix.language` |
| Code Fix (full code) | `p3_code_investigation.code_fix.full_code` |
| Implementation Risks | `p3_code_investigation.code_fix.risks` |
| Tests Needed | `p3_code_investigation.code_fix.tests_needed` |
