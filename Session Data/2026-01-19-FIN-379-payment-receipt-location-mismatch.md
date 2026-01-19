# Analyze-Bug Session: FIN-379

**Date:** 2026-01-19
**Command Version (Hash):** unknown
**Linear Issue:** FIN-379
**Classification:** Backend
**Outcome:** Duplicate Found - Already In Progress

---

## Session Summary

Customer reported payment receipts showing wrong location for multi-location customers. Investigation revealed FIN-379 already tracks this exact issue (In Progress, assigned to Ryan Pendleton). Root cause identified: `PaymentReceiptPdfManager.cs` uses merchant address instead of job's location address from the `LocationId` field.

---

## User Inputs

**Input 1: Initial Report**
> [Urgent]
> We are getting a lot of negative feedback with payment requests and Payment Receipt
> Right now, the payment receipt looks like it is based on the contact record.
> Gurr brothers has multiple jobs with different locations.
> When a payment is received it goes to the correct account, but the receipt shows a different location all together.
> The example I provided below was a payment logged on a job for Dalene Bishop
> Dalene Bishop #18640
> However, the customer and Gurr Brothers received a payment receipt stating it was under Utah Water and Fire (the location the contact is assigned to)
> This might have been an over site as most companies don't have multiple locations for the same customer.
> The functionality of the receipt should match the location the payment came from. (the job Record)
> Reason why it needs to be fixed:
> if the customer is receiving this payment receipt they see a different location name and could fight to say it way paid to the wrong company and could take legal action to gurr brotheres
> Thoughts?

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** Receipt is sent to customers (email/PDF generation), and the data source (contact vs job location) is determined server-side during receipt generation. The payment goes to the correct account but receipt shows wrong location - this is a data retrieval issue in backend receipt generation.

### Investigation Steps
1. Parsed bug report for repro steps, expected/actual behavior
2. Classified as Backend based on receipt generation being server-side
3. Ran duplicate check in parallel with code exploration
4. Found existing ticket FIN-379 tracking same issue
5. Explored SumoQuote codebase to identify root cause

### Code Analysis
- **Repository:** SumoQuote (sumoquote)
- **Files Examined:**
  - `SumoQuote.Services/Payment/PDF/PaymentReceiptPdfManager.cs:165-214` - `AddMerchantDetails()` uses `transaction.Merchant.Address` (merchant's business address) instead of job location
  - `SumoQuote.Services/Payment/DTO/TransactionReceiptDTO.cs` - Missing job location fields entirely
  - `SumoQuote.Services/Payment/Payrix/PayrixApiService.cs:116-162` - `GetTransactionReceipt()` never fetches `Report.LocationId`
  - `SumoQuote.Background/Notifications/Payment/SendTransactionReceiptEmail.cs:77-81` - Shows correct pattern using `GetLocationBasedBrandingQuery`
- **Root Cause:** Payment receipt PDF uses merchant address from Payment Addon settings instead of the job's location address. The DTO lacks job location fields, and the API service never retrieves the `LocationId` from the report to fetch the correct location.

### Fix Proposal
- **Approach:**
  1. Add job location fields to `TransactionReceiptDTO`
  2. Update `PayrixApiService.GetTransactionReceipt()` to fetch `Report.LocationId` → `Location` entity
  3. Update `PaymentReceiptPdfManager.AddMerchantDetails()` to use job location address
- **Files to Change:**
  - `SumoQuote.Services/Payment/DTO/TransactionReceiptDTO.cs`
  - `SumoQuote.Services/Payment/Payrix/PayrixApiService.cs`
  - `SumoQuote.Services/Payment/PDF/PaymentReceiptPdfManager.cs`
- **Risks:** Need to ensure all receipt generation paths use the new location data; multi-location customers are the edge case that exposed this

---

## Outputs

- **Linear Ticket:** [FIN-379](https://linear.app/jobnimbus/issue/FIN-379/bug-payment-receipt-shows-mismatched-location-for-multi-location) (already exists - In Progress)
- **PR Created:** Not created (duplicate ticket already being worked)
- **Branch:** N/A

---

## Key Learnings

- Payment receipt location bug affects multi-location customers where contact location differs from job location
- The `SendTransactionReceiptEmail` handler already demonstrates the correct pattern for fetching location-based branding - this pattern should be applied to PDF generation as well
- Data flow issue: Current path goes Payment → Transaction → Merchant.Address; should go Payment → Transaction → Report.LocationId → Location.Address

---

*Session captured: 2026-01-19*
*Command Version: unknown*
*Saved by /save-session*
