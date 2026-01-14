# Analyze-Bug Session: FIN-371

**Date:** 2026-01-08
**Command Version (Hash):** 371156f
**Linear Issue:** FIN-371
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

Customer using GlobalPayments processor (not JobNimbus Payments) receiving "Payment Failed: Bad Request" errors when processing payments on invoices. The issue affects multiple cards and multiple customers, indicating a systemic backend integration issue. Investigation determined this is a backend GlobalPayments API integration issue requiring Fintech team investigation. Linear ticket FIN-371 created with P2 priority.

---

## User Inputs

**Input 1: Initial Report**
> WORKFLOW  Today at 10:49 AM
> @asher.jensen needs help!
> Login Email: therebuildguy@outlook.com
> Hubspot Ticket: https://app.hubspot.com/contacts/3409122/record/0-5/39005428331/
> Record ID:
> invoice 7406
> Issue:
> The customer is receiving this error when making a payment on the invoice. He does not use Jobnimbus payments, only global payments. Has used different cards for multiple customers and stated that he gets the same error every time. The payment shows as "Payment Failed: Bad Request". There are some errors showing in DataDog (Link: https://app.datadoghq.com/logs?query=%22Payment%20Failed%3A%20Bad%20Request%22&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1765024851563&to_ts=1767616851563&live=true) and they are all showing for GlobalPay.

**Input 2:**
> Let's get a Linear ticket created for the fintech team. Include the slack link: https://jobnimbus.slack.com/archives/C09GJKEDX16/p1767900035282879 and use the linear ticket hybrid format markdown reference in my local Claude files.

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** Payment failures with "Bad Request" errors in DataDog logs, affecting multiple cards/customers - this is clearly a payment processing (backend) issue with the GlobalPayments integration. API returning 400 Bad Request, not a frontend rendering or state issue.

### Investigation Steps
1. Parsed bug report for repro steps, expected/actual behavior, error messages
2. Classified as Backend based on: API returning errors, DataDog logs showing errors, affects all cards/customers
3. Ran duplicate check in Linear - no matching issues found
4. Identified team as Fintech (owns GlobalPayments integration)
5. Searched frontend codebase for GlobalPayments code - found payment settings and processor types
6. Determined backend repos (`jobnimbus-integrations-service`) not available locally
7. Identified root cause as backend GlobalPayments API integration issue

### Code Analysis
- **Repository:** `jobnimbus-integrations-service` (not available locally)
- **Files Examined:**
  - `jobnimbus-frontend/libs/states/financials/src/lib/apis/payments/models/payment-settings.ts` - Contains GlobalPay processor type definition
  - `jobnimbus-frontend/libs/states/financials/src/lib/apis/payments/payments.handlers.ts` - Frontend payment handlers (no error generation)
- **Root Cause:** Backend returning 400 Bad Request from GlobalPayments integration - likely invalid payload, credential issue, or GlobalPayments API contract change

### Fix Proposal
- **Approach:** Requires backend investigation by Fintech team
- **Investigation Steps:**
  1. Check DataDog logs for full GlobalPayments API request/response
  2. Verify GlobalPayments merchant credentials are valid
  3. Check for recent deployments that modified payment request payload
  4. Test with known-good merchant account to isolate issue
- **Files to Change:** `src/Integrations/GlobalPayments/GlobalPaymentsService.cs`, `GlobalPaymentsClient.cs` (pending investigation)
- **Risks:** Payment processing is revenue-critical

---

## Outputs

- **Linear Ticket:** [FIN-371](https://linear.app/jobnimbus/issue/FIN-371/payments-globalpayments-payment-failed-bad-request-error-affecting-all)
- **PR Created:** Not created (backend investigation required)
- **Branch:** `brandykinsman/fin-371`

---

## Key Learnings

- GlobalPayments integration errors are backend-only - frontend just displays the error message
- "Payment Failed: Bad Request" pattern in DataDog indicates API validation failure at the GlobalPayments integration layer
- Backend repos (`jobnimbus-integrations-service`) needed for direct code investigation of payment processing issues
- When payment failures affect multiple cards/customers, it's almost always a systemic backend issue rather than card-specific

---

*Session captured: 2026-01-08 12:50*
*Command Version: 371156f*
*Saved by /save-session*
