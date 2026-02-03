# Analyze-Bug Session: SALES-823 (Estimate-Invoice Total Mismatch)

**Date:** 2026-02-03
**Command Version (Hash):** 371156f
**Linear Issue:** SALES-823 (related: SALES-420, SALES-829)
**Classification:** Backend
**Outcome:** Duplicate Identified - Linked to Existing Issue

---

## Session Summary

Customer (Horizon Restoration - paul@horizonrestoration.com) reported that converting an approved estimate to an invoice results in different totals. Investigation revealed this is a duplicate of the known SumoQuote/JobNimbus rounding discrepancy issue (SALES-420, marked Done but with incomplete fix). The comprehensive fix (SALES-823) with 6 sub-tickets remains in Backlog. Horizon Restoration was previously linked to SALES-420.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
> Troubleshooting Steps Taken:
> Refresh Browser
>
> Who Verified the Escalation?
> Brandy Kinsman
>
> Slack URL:
> Notes:
> https://jobnimbus.slack.com/archives/CBWG040CF/p1769053819144179
>
> Escalated By:
> Natalie Bishop
>
> Brief Description of Issue:
> Notes:
> When the approved estimate is converted to an invoice, the total changes on the invoice.
>
> User ID:
> Notes:
> paul@horizonrestoration.com
>
> Date/Time Issue Occurred:
> Notes:
> Jan, 20th, 9:30am
>
> Specific Record Impacted:
> Notes:
> Customer id # 8248
> Estimate # 261
> Invoice # 262
>
> Steps to Replicate / Steps to View:
> Notes:
> Logged into paul@horizonrestoration.com
> Typed in Contact #8248 into the search bar, went to estimate #261 and compared the estimate with the total on invoice #262 (converted from #261) and saw that the totals were different.
> Attempted to replicate by converting the estimate to another invoice and saw the same issue, only the total was a different amount again.
> The logo left the original and manually edited the converted invoice #264 to be the correct amount to send to the customer.
>
> Expected Results:
> Notes:
> The converted invoice would have the same total as the estimate
>
> Actual Results:
> Notes:
> The converted invoice has a different total than the estimate.
>
> Can you Replicate in Logo's Account?
> Yes
>
> Did you Test in Test Account?
> No
>
> Can you Replicate in Test Account?
> No
>
> Computer OS Type and Version
> Windows
>
> Browser Type and Version:
> Chrome

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** Data calculation changes during conversion (same estimate produces different totals each time) indicates server-side calculation logic issue, not UI display. The total discrepancy occurs during the estimate-to-invoice conversion process which is a backend operation.

### Investigation Steps
1. Parsed bug report for key details (user, records, repro steps)
2. Ran parallel duplicate checks searching for "estimate invoice convert total different" and "estimate to invoice total mismatch"
3. Found SALES-420 which specifically mentions Horizon Restoration
4. Retrieved full details of SALES-420 - marked Done but linked to parent SALES-823
5. Retrieved SALES-823 - comprehensive rounding alignment fix still in Backlog
6. Identified the root cause: SumoQuote vs JobNimbus rounding strategy mismatch

### Code Analysis
- **Repository:** `estimate-sq-integration-backend` (partial fix deployed), `sumoquote-frontend` (fix pending)
- **Files to Change (from SALES-829):**
  - `src/pages/invoice/_projectId/_reportId/index.vue:438,489`
  - `src/components/Invoice/InvoiceAuthorizationSection.vue:167`
  - `src/components/Invoice/InvoiceEstimateSection.vue:194`
- **Root Cause:** SumoQuote uses "aggregate-then-round" (`lineTotal = Price * Quantity`) while JobNimbus uses "per-item rounding" (`amount = round(price * quantity, 2)`). This causes floating-point precision errors when estimate totals are converted to invoices.

### Fix Proposal
- **Approach:** Change SumoQuote's calculation to match JobNimbus by rounding each line item total to 2 decimal places BEFORE summing
- **Code Change Pattern:**
```typescript
// Before
const cost = item.Price * item.Quantity

// After
const cost = Number((item.Price * item.Quantity).toFixed(2))
```
- **Files to Change:** 6 sub-tickets covering backend calculator, frontend calculator, model classes, services, financing calculations, and frontend invoice components
- **Risks:** Requires coordinated deployment across multiple services

---

## Outputs

- **Linear Ticket:** SALES-823 (existing) - https://linear.app/jobnimbus/issue/SALES-823/align-sumoquote-rounding-with-jobnimbus
- **Related Tickets:**
  - SALES-420 (Done - partial fix): https://linear.app/jobnimbus/issue/SALES-420/nse-estimate-totals-differ-between-pdf-and-estimates-tab
  - SALES-829 (Backlog - frontend fix): https://linear.app/jobnimbus/issue/SALES-829/sumoquote-frontend-update-line-item-total-calculations-in-invoice
- **PR Created:** Not created (duplicate of existing issue)
- **Branch:** N/A

---

## Duplicate Chain

| Ticket | Title | Status | Notes |
|--------|-------|--------|-------|
| SALES-420 | NSE - Estimate Totals Differ Between PDF and Estimates Tab | Done | Horizon Restoration was already linked here |
| SALES-823 | Align SumoQuote Rounding with JobNimbus | Backlog | Parent comprehensive fix with 6 sub-tickets |
| SALES-829 | SumoQuote Frontend: Update line item total calculations | Backlog | Sub-task for frontend invoice components |

---

## Key Learnings

- **Pattern Recognition:** Customer escalations that match known issues should be quickly identified via duplicate search with customer name/feature keywords
- **Incomplete Fix Detection:** SALES-420 was marked "Done" but the comprehensive fix (SALES-823) remained in Backlog - this gap allowed the same customer to be impacted again
- **Horizon Restoration Recurrence:** This specific customer (paul@horizonrestoration.com) was already linked to SALES-420 via HubSpot tickets (32597948597, 32622422404), indicating they are a repeat reporter of this issue
- **Technical Root Cause:** Rounding strategy mismatches between systems (aggregate-then-round vs per-item-round) cause cumulative floating-point precision errors that manifest as penny discrepancies

---

## Recommended Actions

1. Link this new escalation to SALES-823
2. Consider priority bump for SALES-823 given recurring customer impact
3. Add HubSpot ticket to track this occurrence

---

*Session captured: 2026-02-03 11:15*
*Command Version: 371156f*
*Saved by /save-session*
