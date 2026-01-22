# Analyze-Bug Session: ACC-631

**Date:** 2026-01-22
**Command Version (Hash):** 812a15f
**Linear Issue:** ACC-631
**Classification:** Frontend (updated from initial Backend classification)
**Outcome:** Ticket Created

---

## Session Summary

Profit Tracker pulls in ALL estimates from every job related to a contact instead of just the estimates for the specific job being viewed. Root cause identified as `related: true` parameter in the `useGetEstimateListQuery` hook causing over-fetching. Linear ticket ACC-631 created with high confidence fix proposal.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
> Troubleshooting Steps Taken: Refresh Browser
> Who Verified the Escalation? Skyler Holbrook
> Escalated By: EJ Hammond
> Slack Thread: https://jobnimbus.slack.com/archives/C02TPNDMB55/p1768601040281269
>
> Brief Description of Issue:
> Profit tracker is pulling in every estimate from every job related to a single contact instead of just the ones on the job.
>
> User ID: jn-lrtiecs07ebwchj3u2c41ja
> Date/Time Issue Occurred: 1/16 3:04pm
> Specific Record Impacted: UT-2102
>
> Steps to Replicate / Steps to View:
> Go to the job, then to the profit tracker and try adding an estimate, or really any of the "Planned" products, and then check the corresponding page to see that there aren't that many of that record.
>
> Expected Results: PT only pulls in the records related to the job.
> Actual Results: PT pulls in all records related to every job related to the primary contact.
>
> Can you Replicate in Logo's Account? Yes
> Did you Test in Test Account? Yes
> Can you Replicate in Test Account? Yes (joe.brown@jobnimbus.com)
> Computer OS Type and Version: Windows
> Browser Type and Version: Chrome
> Additional Information: Photos in pinned.

**Input 2:**
> Let's make a Linear.

**Input 3:**
> Can you include the hash commit on the ticket metadata from the template?

---

## Claude's Analysis & Thinking

### Classification
- **Initial Decision:** Backend (data query/filtering issue)
- **Updated Decision:** Frontend
- **Confidence:** High
- **Reasoning:** Initially classified as Backend because it appeared to be a data filtering issue. Upon code investigation, determined the root cause is in the frontend React component passing `related: true` to the API query, causing the backend to return all related estimates. The fix is a frontend-only change.

### Investigation Steps
1. Extracted bug report details from escalation form
2. Ran duplicate check in Linear (no matches found for this specific issue)
3. Identified team (Accounting) and priority (P2 - High)
4. Used Explore agent to search jobnimbus-frontend for Profit Tracker code
5. Traced the data flow from component → query hook → API call
6. Identified the `related: true` parameter as the root cause

### Code Analysis
- **Repository:** jobnimbus-frontend
- **Files Examined:**
  - `libs/experiences/financial/src/lib/pages/profit-tracker/create-edit-job-costing-page/details-drawer/projected-revenue/linkable-estimates/linkable-estimates.component.tsx:76-80` - Contains the buggy query with `related: true`
  - `libs/states/financials/src/lib/apis/estimates/estimates.queries.ts:25-53` - Query definition showing how `related` parameter adds `&related=1` to URL
  - `libs/utils/services/src/lib/elasticsearch-query-builder.ts:94-96` - Shows how `related` config appends to query
- **Root Cause:** The `useGetEstimateListQuery` hook is called with `related: true`, which adds `&related=1` to the API request. This parameter causes the backend to return estimates from ALL related entities (all jobs for the contact) instead of just the current job.

### Fix Proposal
- **Approach:** Remove or set `related` to `false` in the query call
- **Files to Change:**
  - `linkable-estimates.component.tsx` line 76-80
- **Risks:** Low - simply removes over-fetching behavior. May need to verify other "Planned" products (invoices, etc.) don't have the same issue.

---

## Outputs

- **Linear Ticket:** [ACC-631](https://linear.app/jobnimbus/issue/ACC-631/profit-tracker-or-pulls-estimates-from-all-contact-jobs-instead-of)
- **PR Created:** Not created
- **Branch:** brandykinsman/acc-631

---

## Key Learnings

- The `related` parameter in estimate queries is designed to fetch across the entire related entity tree (contact → all jobs → all estimates), which is useful for some views but not for job-specific contexts like Profit Tracker
- Initial classification as "Backend" was revised to "Frontend" after code investigation revealed the issue is in query parameters, not backend logic
- Similar pattern may exist in other Profit Tracker "Planned" product components (invoices, etc.) - noted as future improvement in ticket

---

*Session captured: 2026-01-22 16:03*
*Command Version: 812a15f*
*Saved by /save-session*
