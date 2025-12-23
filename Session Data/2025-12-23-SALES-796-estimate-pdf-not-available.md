# Analyze-Bug Session: SALES-796

**Date:** 2025-12-23
**Command Version (Hash):** 371156f
**Linear Issue:** SALES-796
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

Customer reported NSE estimates showing "PDF not available" error. Investigation revealed the new PDF endpoint (SALES-688, deployed Dec 12) doesn't handle the edge case where `SignedPDFId` references a file that no longer exists in S3 - the `GetBlobFileAsStream()` method returns an empty MemoryStream instead of throwing an error, causing the frontend to display "PDF not available".

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
>
> Troubleshooting Steps Taken:
> Refresh Browser, Logout/Login, Check Browser Updates, Clear Cache, Incognito
>
> Who Verified the Escalation?
> Chris Berry
>
> Escalated By:
> JJ Repman Johnson
>
> Brief Description of Issue:
> Estimates are showing as "PDF not Available"
>
> User ID:
> m6qtiqdvzc47llkbne62hr2
>
> Date/Time Issue Occurred:
> 12/18/2025
>
> Specific Record Impacted:
> 17230 Estimate 9122
>
> Steps to Replicate / Steps to View:
> Logged in via admin, tried again incognito
>
> Expected Results:
> Estimate loads
>
> Actual Results:
> page says pdf not available.
>
> Can you Replicate in Logo's Account?
> Yes
>
> Can you Replicate in Test Account?
> No
>
> Browser Type and Version:
> Chrome
>
> Computer OS Type and Version:
> Windows 11 Pro

**Input 2: Estimate Type Clarification**
> It's NSE

**Input 3: Linear Ticket Format**
> Let's create a Linear ticket using the linear ticket hybrid format .md

**Input 4: Update Ticket Format**
> Please update the linear ticket to use the linear template hybrid format .md

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** Frontend correctly displays "PDF not available" when API returns no/empty PDF URL. The issue is the PDF doesn't exist or can't be retrieved from backend storage. Not reproducible in test account but reproducible in customer account suggests data-specific issue (missing S3 file).

### Investigation Steps
1. Ran parallel duplicate check on Linear for "estimate PDF not available" - found related issues (SALES-688, SALES-118) but no exact duplicate
2. Launched Explore agent to find "PDF not available" error message in frontend code
3. Found error in `jobnimbus-frontend/libs/experiences/sales/src/lib/estimates/estimate-internal-view/components/estimate-pdf-iframe.component.tsx:68`
4. Identified two PDF APIs - SumoQuote (NSE) and Legacy
5. User confirmed NSE estimate
6. Explored SumoQuote repository for PDF endpoint implementation
7. Found recently added endpoint from SALES-688 (Dec 12, 2025)
8. Identified silent failure in `S3StorageService.GetBlobFileAsStream()` - returns empty MemoryStream on 404
9. Found `ReportPdfService.cs` doesn't validate stream content before returning

### Code Analysis
- **Repository:** sumoquote
- **Files Examined:**
  - `jobnimbus-frontend/.../estimate-pdf-iframe.component.tsx:68` - Error message display
  - `jobnimbus-frontend/.../estimates.queries.ts:274-282` - SumoQuote PDF query
  - `SumoQuote.Services/Reports/ReportPdfService.cs:36-40` - PDF retrieval logic (ROOT CAUSE)
  - `SumoQuote.Azure.Blob.DataAccess/S3StorageService.cs:56-89` - Silent failure on 404
  - `SumoQuote/Controllers/V2/ReportController.cs:41-52` - Endpoint handler
- **Root Cause:** When `SignedPDFId` is populated but file is missing from S3, `GetBlobFileAsStream()` returns empty MemoryStream (not null, not exception). Service doesn't validate stream length, returns empty stream, frontend shows "PDF not available".

### Fix Proposal
- **Approach:** Add stream length validation in `ReportPdfService.cs` before returning; fall back to on-demand PDF generation if stream is empty
- **Files to Change:** `SumoQuote.Services/Reports/ReportPdfService.cs` (1 file, ~3 lines)
- **Risks:** Minimal - adds validation check, graceful fallback to existing functionality

---

## Outputs

- **Linear Ticket:** [SALES-796](https://linear.app/jobnimbus/issue/SALES-796/estimates-pdf-not-available-when-signedpdfid-references-missing-s3)
- **PR Created:** Not created
- **Branch:** `brandykinsman/sales-796`

---

## Key Learnings

- New endpoints should validate stream/response content, not just null checks - `Stream != null` doesn't mean `Stream.Length > 0`
- Silent failures in storage services (S3 returning empty stream on 404) can propagate up as confusing user-facing errors
- SALES-688 (Dec 12) introduced this edge case - worth reviewing other recent endpoint additions for similar patterns
- The `S3StorageService.GetBlobFileAsStream()` pattern of returning empty stream on 404 is a broader architectural concern that may affect other features

---

*Session captured: 2025-12-23 11:05*
*Command Version: 371156f*
*Saved by /save-session*
