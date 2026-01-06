# Analyze-Bug Session: FIN-361

**Date:** 2026-01-06
**Command Version (Hash):** 371156f
**Linear Issue:** FIN-361
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

Customer reported "Error in retrieving policy run summary Not Found" when attempting ACH/eCheck payments. Investigation identified root cause in `PayrixApiRepository.cs` where GIACT policy lookup failures (404) block normal error handling. Created Linear ticket FIN-361 with proposed fix to gracefully handle missing policy data.

---

## User Inputs

**Input 1: Initial Report**
> When attempting to make a payment, the customer is seeing this error:Error: "Error in retrieving policy run summary Not Found"
> Reports: Only one so far, but seeing 25 logs in DataDog (LINK HERE)
> Unable to confirm if it's only one contact for one account or multiple.
> Logo: kz5ua3tb6eb79btvyvpm6gt
> MID: p1_mer_647a0d2a1cc6f3a5dc99f4b
> User: baroofing3@exec.partners

**Input 2:**
> Let's get a Linear ticket created.

**Input 3:**
> Let's update the ticket formatting to use the linear hybrid format .md reference.

**Input 4:**
> Please use the hybrid linear template markdown from my local files.

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** The error message "Error in retrieving policy run summary Not Found" indicates a 404/missing resource from an API call. The "policy run summary" terminology suggests a payment processor integration (Payrix given the `p1_mer_` MID prefix). This is not a UI rendering issue.

### Investigation Steps
1. Ran duplicate check in Linear - no matching issues found
2. Used Task/Explore agent to search for "policy run summary" across payments repositories
3. Located error origin in `dotnet-monolith/App/Fintech/Payrix/PayrixApiRepository.cs`
4. Read the `HandleECheckErrors()` and `GetPolicyRunSummaryForAchTransaction()` methods
5. Identified that 404 from Payrix Risk API throws exception blocking normal error flow

### Code Analysis
- **Repository:** dotnet-monolith
- **Files Examined:**
  - `App/Fintech/Payrix/PayrixApiRepository.cs:165-181` - HandleECheckErrors() method
  - `App/Fintech/Payrix/PayrixApiRepository.cs:433-455` - GetPolicyRunSummaryForAchTransaction() method
- **Root Cause:** When Payrix Risk API returns 404 for GIACT policy lookup, `GetPolicyRunSummaryForAchTransaction()` throws `PayrixApiException` with code "GiactPolicyRunSummaryError". This bubbles up and displays the confusing policy error instead of the actual payment error.

### Fix Proposal
- **Approach:** Wrap policy lookup in try-catch with exception filter for "GiactPolicyRunSummaryError", allowing normal error handling to continue when policy data unavailable
- **Files to Change:** `App/Fintech/Payrix/PayrixApiRepository.cs` (lines 165-181)
- **Risks:** Low - only affects error handling path, preserves existing GIACT block detection

---

## Outputs

- **Linear Ticket:** [FIN-361](https://linear.app/jobnimbus/issue/FIN-361/ach-payment-error-error-in-retrieving-policy-run-summary-not-found)
- **PR Created:** Not created
- **Branch:** brandykinsman/fin-361

---

## Key Learnings

- Payrix Risk API `/risk/v2/decision/policy-run-summary` is optional - not all merchants have GIACT policies configured
- MID prefix `p1_mer_` indicates Payrix payment processor
- Error handling should gracefully handle missing optional data rather than failing completely
- The hybrid Linear template format provides better structure for bug tickets with code analysis

---

*Session captured: 2026-01-06 10:55*
*Command Version: 371156f*
*Saved by /save-session*
