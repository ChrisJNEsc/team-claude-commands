# Analyze-Bug Session: SALES-795

**Date:** 2025-12-23
**Command Version (Hash):** 371156f
**Linear Issue:** SALES-795
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

Customer's estimate became corrupted after being sent, causing "Network Error" when homeowner tries to sign and preventing the estimate from loading/editing in the JN UI. Investigation identified missing `PublicQuoteId` as the likely root cause, with the SumoQuote mapper also hardcoding empty values for `external_id` and `duplicate_from_id` during duplication. Linear ticket SALES-795 created for Sales team investigation.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
> Troubleshooting Steps Taken:
> Clear Cache, Incognito, Logout/Login, Restart Computer, Refresh Browser
> Who Verified the Escalation?
> Brandy Kinsman
> Escalated By:
> EJ Hammond
> Brief Description of Issue:
> Notes:
>
> An estimate got corrupted after it was sent. When the customer tries to sign, they are met with a "Network Error" message. When trying to duplicate the estimate to send out, the corruption stuck, as expected.
>
> User ID:
> Notes:
>
> c15o9
>
> Date/Time Issue Occurred:
> Notes:
>
> 12/19 - 11:59am
>
> Specific Record Impacted:
> Notes:
>
> Job - #7059 - Estimates - 30468 and 30469
>
> Steps to Replicate / Steps to View:
> Notes:
>
> By either trying to view or edit either of the estimates above.
>
> Expected Results:
> Notes:
>
> The estimate will load and be editable. As well as the customer will be able to sign the estimate successfully.
>
> Actual Results:
> Notes:
>
> The estimate will not load and will not be editable. As well as the customer is not able to sign the estimate successfully.
>
> Can you Replicate in Logo's Account?
> Yes
> Did you Test in Test Account?
> No
> Can you Replicate in Test Account?(Include Email Login for Test Account if Yes)
> No
> Computer OS Type and Version (Select Type and Add Version in Notes)
> Windows
> Browser Type and Version: (Select Type and Add Version in Notes)
> Chrome

**Input 2:**
> Let's create a ticket.

**Input 3:**
> Can you update the linear ticket to include the linear hybrid format .md?

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** "Network Error" on signing + estimate won't load/edit + corruption persists through duplication = corrupted data in the database, not a frontend rendering issue. The fact that duplication carries the corruption forward confirms this is a data issue, not a UI rendering problem.

### Investigation Steps
1. Parsed bug report to extract key details (account c15o9, Job #7059, estimates 30468/30469)
2. Ran parallel duplicate check in Linear (searched "estimate corrupted network error sign" and "estimate won't load corrupt")
3. Launched Explore agent to investigate estimate loading, signing, and duplication code paths
4. Identified that SumoQuote mapper hardcodes empty values for critical fields
5. Determined `PublicQuoteId` missing/corrupted as root cause for signing failures

### Code Analysis
- **Repository:** `jobnimbus-frontend`, `estimate-signing-frontend`, `job-costing-frontend`
- **Files Examined:**
  - `job-costing-frontend/src/apis/existing-documents.api.ts` - Estimate loading API
  - `job-costing-frontend/src/models/estimates/estimate.ts` - Estimate model with `source` and `jnid` fields
  - `estimate-signing-frontend/src/utils/api.ts` - Signing endpoints (three variants based on context)
  - `estimate-signing-frontend/src/utils/shared.ts` - Header requirements for signing
  - `jobnimbus-frontend/libs/states/financials/src/lib/apis/estimates/mapper/sumoquote-to-api2-estimate.mapper.ts:76-77` - **Root cause location**
- **Root Cause:** The estimate's `PublicQuoteId` (SumoQuote signing identifier) is missing or corrupted. The signing endpoint `/pub/saveAndSignMultiSignatureQuote/{reviewId}/{signatoryId}` receives null/undefined for `reviewId`, creating a malformed URL. Additionally, the mapper hardcodes `external_id: ''` and `duplicate_from_id: ''`, losing SumoQuote integration data on duplication.

### Fix Proposal
- **Approach:**
  1. Immediate: Investigate database records for estimates 30468/30469 to restore `PublicQuoteId` if possible
  2. Code fix: Update mapper to preserve `PublicQuoteId`, `external_id`, and `duplicate_from_id` during duplication
- **Files to Change:** `sumoquote-to-api2-estimate.mapper.ts:76-77`
- **Risks:** Need to verify field names in Report model; may need backend coordination

---

## Outputs

- **Linear Ticket:** [SALES-795](https://linear.app/jobnimbus/issue/SALES-795/estimate-corruption-network-error-on-signing-estimate-wont-load-job)
- **PR Created:** Not created
- **Branch:** brandykinsman/sales-795

---

## Key Learnings

- Estimate "corruption" symptoms (won't load, won't sign, duplication carries issue) often point to missing SumoQuote integration identifiers like `PublicQuoteId`
- The SumoQuote mapper explicitly hardcodes empty strings for `duplicate_from_id` and `external_id`, which can cause loss of critical data during duplication
- When signing fails with "Network Error", check if the `reviewId` (PublicQuoteId) is being properly passed to the signing endpoint
- Similar issue pattern seen in CORE-8673 (data corruption causing 500 errors)

---

*Session captured: 2025-12-23 17:25*
*Command Version: 371156f*
*Saved by /save-session*
