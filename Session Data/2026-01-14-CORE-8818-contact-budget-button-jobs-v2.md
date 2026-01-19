# Analyze-Bug Session: CORE-8818

**Date:** 2026-01-14
**Command Version (Hash):** 371156f
**Linear Issue:** CORE-8818
**Classification:** Frontend
**Outcome:** Ticket Created

---

## Session Summary

Investigated a bug where the "Add Budget" button appears on the Contact page Financials tab for Jobs V2 accounts but is non-functional when clicked. Analysis revealed that Budget is a Job-specific feature, and the Contact page is incorrectly displaying this option. Created Linear ticket CORE-8818 with two potential scenarios for the CoreCRM team to clarify whether budgets should or shouldn't be supported for Jobs V2 accounts.

---

## User Inputs

**Input 1: Initial Report**
> Here's the support notes: Support - Web Escalation
> Troubleshooting Steps Taken: Refresh Browser
> Who Verified the Escalation? Skyler Holbrook
> Escalated By: Brandon Kersh
> Brief Description of Issue:
> Notes: option for creating a budget is available on contact page
> User ID: lmatpzoj1ds2xne2jdld6fg
> Date/Time Issue Occurred: 1/9/26
> Specific Record Impacted: Contacts - + Add budget button
> Steps to Replicate / Steps to View: Go to any contact → Financials tab → Add budget is a clickable option → button does nothing
> Expected Results: no button
> Actual Results: button
> Can you Replicate in Logo's Account? Yes
> Did you Test in Test Account? Yes
> Can you Replicate in Test Account? Yes (brandon.kersh@jobnimbus.com)
> Computer OS Type and Version: Windows
> Browser Type and Version: Chrome
> This appears to only be happening to Jobs V2 accounts. Can you investigate and write up something for me to post in slack for that team to see if this is intended?

**Input 2:**
> Yes. Let's create a linear. Please use the linear ticket hybrid markdown format.

**Input 3:**
> Could you update it to include more that it might be either of these options? Hey team! We're looking at an issue where the button on a Contact's "Financials" tab for "Add Budget" is non-responsive. This only occurs with Jobs V2 accounts. I know we're making a push for Profit Tracker, so this could be intended.
> Potential Scenario:
> We do not support Budgets for Jobs V2 accounts. If this is the case, that button needs to be removed from that location.
> We do support Budgets for Jobs V2 accounts. If this is the case, the button needs to be responsive.

**Input 4:**
> Can you also update the formatting to utilize the linear ticket hybrid formatting from the markdown file in my local files?

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Frontend
- **Confidence:** High
- **Reasoning:** Button renders when it shouldn't (UI visibility issue), click does nothing (no handler connected or feature incomplete), Jobs V2 account-specific indicates feature flag/conditional rendering bug. No backend errors mentioned - purely UI element that shouldn't be showing or isn't wired up correctly.

### Investigation Steps
1. Searched for duplicate Linear issues - none found for this specific budget button issue
2. Determined team ownership (CoreCRM) based on Contact page + Jobs V2 + financial components
3. Searched jobnimbus-frontend for budget button implementation
4. Found Budget feature is Job-specific in React code
5. Discovered Contact page is NOT in jobnimbus-frontend - likely in legacy Single-SPA/Angular system
6. Analyzed permission helpers - found they check account features but don't validate entity type (Job vs Contact)
7. Identified root cause: Budget link requires `jobId` which doesn't exist on Contact pages

### Code Analysis
- **Repository:** jobnimbus-frontend
- **Files Examined:**
  - `job-payments-and-invoices-create-button.component.tsx:82-92` - Budget button renders based on permissions + feature flag
  - `details-navigation-permission.helper.ts:30-32` - Permission check lacks entity type validation
  - `job-payments-and-invoices.component.tsx:40-41` - Jobs V2 hides create button, but Contact page may use different path
- **Root Cause:** Budget functionality is Job-specific, but Contact page Financials tab uses shared components without entity type guards. The Budget link (`/budget/0?jobid=${jobId}`) requires a valid `jobId` which doesn't exist on Contact pages.

### Fix Proposal
- **Approach:** Two scenarios depending on team clarification:
  - Scenario A (Budgets NOT supported): Add entity type guard to hide Budget option on Contact pages
  - Scenario B (Budgets ARE supported): Wire up Budget creation flow for Contacts
- **Files to Change:** Contact page Financials component (location TBD - likely legacy system), potentially `details-navigation-permission.helper.ts`
- **Risks:** Need to identify where Contact page components are defined (likely legacy Single-SPA/Angular system)

---

## Outputs

- **Linear Ticket:** [CORE-8818](https://linear.app/jobnimbus/issue/CORE-8818/contact-page-add-budget-button-incorrectly-visible-on-financials-tab)
- **PR Created:** Not created
- **Branch:** brandykinsman/core-8818

---

## Key Learnings

- Budget feature is intentionally Job-specific in the React frontend
- Contact page implementation is NOT in jobnimbus-frontend - it's in legacy Single-SPA/Angular system
- Jobs V2 rollout may have had unintended side effects on Contact page UI
- Permission helpers check account features but don't guard against entity type (Job vs Contact)
- When investigating Jobs V2 issues that appear on Contacts, check for shared component usage between Job and Contact pages

---

*Session captured: 2026-01-14 12:30*
*Command Version: 371156f*
*Saved by /save-session*
