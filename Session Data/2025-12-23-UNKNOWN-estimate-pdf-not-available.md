# Analyze-Bug Session: Estimate PDF Not Available

**Date:** 2025-12-23
**Command Version (Hash):** 371156f
**Linear Issue:** UNKNOWN (session saved before ticket creation)
**Classification:** Backend
**Outcome:** Investigation Only

---

## Session Summary

Customer reported estimates showing "PDF not Available" in the NSE (New Sales Experience) internal view. Investigation traced the issue through the frontend PDF iframe component to the backend ReportPdfService, identifying that the PDF endpoint `/api/v2/report/{id}/pdf` is failing for specific estimates, likely due to missing blob storage references or PDF generation failures.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
>
> Troubleshooting Steps Taken: Refresh Browser, Logout/Login, Check Browser Updates, Clear Cache, Incognito
> Who Verified the Escalation? Chris Berry
> Verified in person
> Escalated By: JJ Repman Johnson
> Brief Description of Issue: Estimates are showing as "PDF not Available"
> User ID: m6qtiqdvzc47llkbne62hr2
> Date/Time Issue Occurred: 12/18/2025
> Specific Record Impacted: 17230 Estimate 9122
> Steps to Replicate: Logged in via admin, tried again incognito
> Expected Results: Estimate loads
> Actual Results: page says pdf not available.
> Can you Replicate in Logo's Account? Yes
> Did you Test in Test Account? Yes
> Can you Replicate in Test Account? No
> Computer OS Type: Windows 11 Pro
> Browser: Chrome

**Input 2: Ticket Decision**
> /save-session (chose to save session before creating ticket)

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend (with frontend display component)
- **Confidence:** Medium
- **Reasoning:** The "PDF not available" message is displayed by the frontend when the backend PDF API endpoint fails or returns an error. The root cause is in the backend service, but the frontend lacks detailed error messaging.

### Investigation Steps

1. **P1 Quick Checks:**
   - Linear search: No exact duplicate found
   - Related issues: SALES-118 (PDF preview component), SALES-688 (PDF endpoint - recently added)
   - Support docs: No specific troubleshooting article for this error

2. **P2 Reproduction:**
   - Playwright auth blocked (requires login)
   - Support already verified reproduction in Logo's account
   - Marked as verified by support

3. **P3 Code Investigation:**
   - Traced "PDF not available" message to frontend component
   - Identified backend PDF service flow
   - Found recently added PDF endpoint (SALES-688, Dec 2025)

### Code Analysis
- **Repository:** jobnimbus-frontend, sumoquote
- **Files Examined:**
  - `estimate-pdf-iframe.component.tsx:57-75` - Shows "PDF not available" when pdfUrl is falsy
  - `estimates.queries.ts:274-282` - RTK Query that fetches PDF, no error handling
  - `ReportPdfService.cs:29-66` - Backend service with multiple failure points
  - `ReportController.cs:38-52` - V2 API endpoint for PDF
- **Root Cause:** Backend PDF endpoint failing for specific estimate. Possible causes:
  1. SignedPDFId blob missing from Azure storage
  2. PDF generation service failure
  3. Report data preventing PDF generation

### Fix Proposal
- **Approach:**
  1. Backend: Check if SignedPDFId exists and blob is accessible
  2. Backend: Add better logging for PDF failures
  3. Frontend (optional): Improve error messaging to show specific failure reason
- **Files to Change:**
  - `ReportPdfService.cs` - Add logging
  - `estimate-pdf-iframe.component.tsx` - Better error states
- **Risks:** Data-specific issue may require manual intervention for affected estimate

---

## Outputs

- **Linear Ticket:** Not created (session saved before decision)
- **PR Created:** Not created
- **Branch:** N/A

---

## Key Learnings

- The NSE PDF preview feature was recently added (SALES-688, Dec 2025) and may have edge cases not yet handled
- Frontend displays generic "PDF not available" without distinguishing between different failure modes (missing blob, generation failure, etc.)
- Need to check Azure blob storage to verify if SignedPDFId references exist for problematic estimates
- Consider adding more specific error messaging in the frontend to help diagnose issues faster

---

*Session captured: 2025-12-23 11:00*
*Command Version: 371156f*
*Saved by /save-session*
