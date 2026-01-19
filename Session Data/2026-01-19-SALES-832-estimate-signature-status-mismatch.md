# Analyze-Bug Session: SALES-832

**Date:** 2026-01-19
**Command Version (Hash):** 371156f
**Linear Issue:** SALES-832
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

Customer reported that a fully signed estimate (Estimate 6204) shows "1/1" signed in the detail view but "Partially Signed" in the list/column view. Investigation revealed a data synchronization issue where the stored `signature_status` database field is not being updated when the `Report_Signed` webhook fires from SumoQuote after all signers complete.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
> Troubleshooting Steps Taken:
> Refresh Browser, Logout/Login, Check Browser Updates, Different Browser, Incognito, Clear Cache, Restart Computer
>
> Who Verified the Escalation?
> Ui Keo
>
> Escalated By:
> Westley Holden
>
> Brief Description of Issue:
> Fully signed estimate is showing as partially signed
>
> User ID:
> bchristie@beardroofing.com
>
> Date/Time Issue Occurred:
> 1/6
>
> Specific Record Impacted:
> Estimate 6204
>
> Steps to Replicate / Steps to View:
> Open estimate
> See it is signed 1/1
> Check estimate column for sig status and see partially signed
>
> Expected Results:
> Fully signed
>
> Actual Results:
> Partially signed
>
> Can you Replicate in Logo's Account?
> Yes
>
> Did you Test in Test Account?
> No
>
> Computer OS Type and Version: Windows
> Browser Type and Version: Chrome

**Input 2:**
> Can you update the linear formatting to use the linear hybrid format markdown in my local files?

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** The detail view shows correct data (1/1 signed) calculated from live signer data, while the list view shows incorrect data (Partially Signed) from a stored database field. This indicates the webhook handler that should update the stored `signature_status` field is failing to do so when all signers complete.

### Investigation Steps

1. **Duplicate Check:** Searched Linear for similar issues. Found related historical issue JNA-41522 ("Fully Signed Estimate Showing Status Draft") but determined it was a different root cause (handler not registered).

2. **Frontend Code Analysis:** Traced the signature status display in jobnimbus-frontend:
   - `JobEstimatesTable` component displays `signatureStatus` directly from API response
   - `estimates-mapper.ts:24` does a direct passthrough of `signature_status` from API
   - `estimates.queries.ts:54-91` has correct `getSignatureStatus()` function that calculates from signer data

3. **Data Flow Discovery:** Identified two different data sources:
   - Detail view: Fetches fresh data from SumoQuote API and calculates status live
   - List view: Uses stored `signature_status` field from database (not calculated)

4. **SumoQuote Webhook Investigation:** Found the webhook flow in sumoquote repository:
   - `EstimateSyncWebhookNotificationHandler.cs:143` sends `Report_Signed` webhook
   - Posts to: `POST /estimates/v1/integrations/sumoquote/webhook?eventtype=Report_Signed`
   - This should trigger an update to `signature_status` but appears to be failing

### Code Analysis
- **Repository:** jobnimbus-frontend, sumoquote
- **Files Examined:**
  - `jobnimbus-frontend/libs/states/financials/src/lib/apis/estimates/mapper/estimates-mapper.ts:24` - Direct passthrough of stored signature_status
  - `jobnimbus-frontend/libs/states/sales/src/lib/apis/estimates/estimates.queries.ts:54-91` - Correct calculation logic for detail view
  - `jobnimbus-frontend/libs/experiences/job-management/src/lib/components/job-estimates/job-estimates-table/job-estimates-table.component.tsx` - List view display
  - `sumoquote/SumoQuote.Background/Notifications/Integration/JobNimbus/EstimateSyncWebhookNotificationHandler.cs:143` - Webhook sender
  - `sumoquote/SumoQuote.Data/PublicAPI/Views/Report/SumoReport.cs` - Status calculation logic
- **Root Cause:** The stored `signature_status` field is not being updated when the `Report_Signed` webhook fires. The detail view calculates from live signer data; the list view uses the stale stored field.

### Fix Proposal
- **Approach:** Backend investigation needed to find the JobNimbus webhook handler that processes `Report_Signed` events and ensure it updates the `signature_status` field to "Fully Signed"
- **Files to Change:** JobNimbus webhook handler for `/estimates/v1/integrations/sumoquote/webhook`
- **Risks:** May affect other estimates if fix is too broad; need to test with multiple signers
- **Alternative:** Frontend workaround to calculate `signatureStatus` in list view (more expensive but consistent)

---

## Outputs

- **Linear Ticket:** [SALES-832](https://linear.app/jobnimbus/issue/SALES-832/estimate-fully-signed-estimate-shows-partially-signed-in-list-view)
- **PR Created:** Not created
- **Branch:** brandykinsman/sales-832

---

## Key Learnings

- **Data source discrepancy pattern:** When detail views show correct data but list views show stale data, look for stored vs calculated field differences
- **Webhook tracing:** SumoQuote → JobNimbus webhook flow involves `DocumentSignedNotification` → `Report_Signed` webhook → JN handler
- **Signature status flow:** SumoQuote determines `ReportStatus` dynamically based on `SignatureDate.HasValue`, but this needs to be synced to JN's stored field
- **Related historical issue:** JNA-41522 had similar symptoms but different root cause (handler not registered) - useful reference for Sales team

---

*Session captured: 2026-01-19 09:20*
*Command Version: 371156f*
*Saved by /save-session*
