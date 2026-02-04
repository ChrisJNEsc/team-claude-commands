# Analyze-Bug Session: FULFMNT-563

**Date:** 2026-02-03
**Command Version (Hash):** 2a130ae
**Linear Issue:** FULFMNT-563
**Classification:** Backend
**Outcome:** Ticket Created

---

## Session Summary

User reported Work Order PDF "Download PDF" and "View PDF" actions returning nothing when clicked. Investigation revealed 404 "Not Found" responses from the backend `/api2/download` endpoint. The issue is intermittent and self-resolving, suggesting a PDF generation timing or race condition issue. Linear ticket FULFMNT-563 created and assigned to Fulfillment team QA (Kira Holyoak).

---

## User Inputs

**Input 1: Initial Report**
> When selecting the three dots to the right of a Work Order, I select "Download PDF" and nothing downloads. I also choose "View PDF" and nothing pops open to view. This happened again earlier this morning, but self-resolved.

**Input 2: Location Clarification**
> On Jobs or Contacts. There are no console errors. I'm using Chrome.

**Input 3: Screenshot with Network Tab**
> Here is what we are seeing.
> [Screenshot showing Network tab with 404 "Not Found" response for document request `2071d80fec7b421b9913...`]

**Input 4: Customer IDs**
> JNID: 1kc8re, COMP ID:1kc8rd

**Input 5: Linear Request**
> Let's create a Linear.

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Backend
- **Confidence:** High
- **Reasoning:** Network request fires successfully (frontend click handler works), but returns 404 "Not Found" from the `/api2/download` endpoint. The response tab in DevTools clearly showed "Not Found" status. No JavaScript console errors present.

### Investigation Steps
1. Gathered initial bug report - identified missing info (repro steps, errors)
2. Asked clarifying questions about location, console errors, browser
3. Requested Network tab check - user provided screenshot showing 404 response
4. Classified as Backend issue based on API 404 response
5. Ran parallel duplicate check (none found) and team mapping lookup
6. Used Explore agent to trace code path from UI to API endpoint
7. Identified complete frontend code flow - working correctly
8. Determined root cause is backend `/api2/download` endpoint returning 404 intermittently

### Code Analysis
- **Repository:** jobnimbus-frontend (frontend), jobnimbus-api (backend)
- **Files Examined:**
  - `jobnimbus-frontend/libs/states/financials/src/lib/apis/work-orders/work-orders.queries.ts:27-47` - RTK Query endpoints for PDF view/download
  - `jobnimbus-frontend/libs/experiences/job-management/src/lib/components/job-material-work-orders/work-orders/job-work-orders-table/job-work-orders-table-overflow-menu.component.tsx` - UI component with overflow menu actions
  - `jobnimbus-frontend/libs/experiences/job-management/src/lib/hooks/work-orders/use-work-order-actions.hook.ts` - Action handlers
  - `jobnimbus-frontend/libs/experiences/job-management/src/lib/hooks/files/use-view-file.hook.ts` - View file hook
  - `jobnimbus-frontend/libs/experiences/job-management/src/lib/hooks/files/use-download-file.hook.ts` - Download file hook
- **Root Cause:** Backend `/api2/download?type=pdf_view&w_id={id}` endpoint returns 404 intermittently. Frontend code path is working correctly. Likely PDF generation timing issue or race condition where PDF isn't ready when request arrives.

### Fix Proposal
- **Approach:** Backend investigation needed to determine why PDFs are not found intermittently. Possible fixes include retry logic, PDF availability check before returning URL, or fixing async generation timing.
- **Files to Change:** Backend `/api2/download` endpoint (exact file unknown - backend investigation required)
- **Risks:** Could affect other PDF downloads (Invoice, Material Order, Credit Memo) if they share the same endpoint

---

## Outputs

- **Linear Ticket:** [FULFMNT-563](https://linear.app/jobnimbus/issue/FULFMNT-563/work-orders-or-pdf-downloadview-returns-404-not-found-intermittently)
- **PR Created:** Not created
- **Branch:** `brandykinsman/fulfmnt-563`

---

## Key Learnings

- Intermittent issues that "self-resolve" often indicate timing/race conditions rather than persistent bugs
- Screenshot with DevTools Network tab was critical for classification - immediately confirmed backend 404 vs frontend issue
- Work Order PDF uses same pattern as Invoice/Material Order PDFs via `/api2/download` endpoint - fix may benefit multiple features
- Team mapping: Work Orders owned by Fulfillment (Panda) team, escalations contact Garrett Young, Slack #fulfillment-domain-dev

---

*Session captured: 2026-02-03 16:29*
*Command Version: 2a130ae*
*Saved by /save-session*
