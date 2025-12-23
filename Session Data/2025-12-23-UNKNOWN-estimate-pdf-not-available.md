# Analyze-Bug Session: Estimate PDF Not Available

**Date:** 2025-12-23
**Command Version (Hash):** ba98a98
**Linear Issue:** UNKNOWN (potentially related to SALES-659, SALES-795)
**Classification:** Frontend
**Outcome:** Investigation Only - User requested /save-session before ticket creation

---

## Session Summary

Customer reported estimates showing "PDF not Available" error when attempting to view estimate PDFs. Investigation found this is likely related to existing issues SALES-659 (related entity routing) or SALES-795 (estimate corruption). Code analysis revealed the frontend's PDF query handler silently swallows API errors, masking the root cause.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
>
> Troubleshooting Steps Taken: Refresh Browser, Logout/Login, Check Browser Updates, Clear Cache, Incognito
>
> Who Verified the Escalation? Chris Berry
>
> Escalated By: JJ Repman Johnson
>
> Brief Description of Issue: Estimates are showing as "PDF not Available"
>
> User ID: m6qtiqdvzc47llkbne62hr2
>
> Date/Time Issue Occurred: 12/18/2025
>
> Specific Record Impacted: 17230 Estimate 9122
>
> Steps to Replicate / Steps to View: Logged in via admin, tried again incognito
>
> Expected Results: Estimate loads
>
> Actual Results: page says pdf not available.
>
> Can you Replicate in Logo's Account? Yes
>
> Did you Test in Test Account? Yes
>
> Can you Replicate in Test Account? No
>
> Computer OS Type and Version: Windows 11 Pro
>
> Browser Type and Version: Chrome
>
> Additional Information: Screenshots from Logo in email thread

**Input 2: Next Step Decision**
> /save-session

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Frontend (with potential backend data issue)
- **Confidence:** High
- **Reasoning:** The "PDF not Available" message is rendered by frontend code, but the root cause is likely a backend API error being silently swallowed

### Investigation Steps
1. Extracted issue details from support escalation form
2. Launched parallel subagents for:
   - P1: Quick checks (duplicate search, documentation)
   - P3: Code investigation (root cause analysis)
3. Noted P2 reproduction was already completed by support (replicable in customer account, NOT in test account - indicating data-specific issue)
4. Found high-confidence duplicate match (SALES-659) and medium-confidence match (SALES-795)
5. Identified frontend code that silently swallows API errors

### Code Analysis
- **Repository:** jobnimbus-frontend
- **Files Examined:**
  - `libs/states/sales/src/lib/apis/estimates/estimates.queries.ts:274-282` - getSumoQuoteEstimatePdfLink query
  - `libs/experiences/sales/src/lib/estimates/estimate-internal-view/estimate-internal-view.component.tsx` - PDF display component
  - `libs/experiences/sales/src/lib/estimates/estimate-internal-view/components/estimate-pdf-preview.component.tsx` - PDF preview component
- **Root Cause:** The `getSumoQuoteEstimatePdfLink` query's `responseHandler` doesn't validate HTTP response status before calling `.blob()`. When API returns error (404, 500, etc.), it silently fails and returns undefined, showing "PDF not available" instead of actual error.

### Fix Proposal
- **Approach:** Add response status validation and proper error handling to the responseHandler before processing blob
- **Files to Change:**
  - `libs/states/sales/src/lib/apis/estimates/estimates.queries.ts:274-282`
- **Risks:**
  - UI needs updating to display new error messages appropriately
  - Need unit tests for error handling scenarios (404, 500, empty blob)

### Proposed Code Fix
```typescript
getSumoQuoteEstimatePdfLink: build.query<string, string>({
  query: (estimateId) => ({
    url: `${AppAuth.getSumoQuoteRoot()}/v2/report/${estimateId}/pdf`,
    responseHandler: async (response) => {
      // Validate response status before processing
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to fetch PDF: ${response.status} ${response.statusText}. ${errorText}`
        );
      }
      const blob = await response.blob();
      if (!blob || blob.size === 0) {
        throw new Error('PDF response body is empty');
      }
      const url = URL.createObjectURL(blob);
      if (!url) {
        throw new Error('Failed to create object URL for PDF');
      }
      return url;
    },
  }),
}),
```

---

## Related Issues Found

| Issue | Confidence | Description |
|-------|------------|-------------|
| **SALES-659** | HIGH | Related Entity Estimates don't load - when viewing estimate from wrong entity context, route uses wrong projectId causing load failures |
| **SALES-795** | MEDIUM | Estimate corruption - PublicQuoteId missing/corrupted, estimate won't load (created 2025-12-23) |
| **SALES-747** | LOW | Logo missing from PDFs - different symptom but related to PDF generation |

---

## Outputs

- **Linear Ticket:** Not created (session saved before ticket creation decision)
- **PR Created:** Not created
- **Branch:** N/A

---

## Key Learnings

- "PDF not Available" error can have multiple root causes - need to determine if it's routing (SALES-659), corruption (SALES-795), or a new issue
- The frontend silently swallows API errors in PDF queries, making debugging difficult - this should be fixed regardless of specific customer issue
- Data-specific issues (replicable in customer account but NOT test account) often indicate corrupted data rather than code bugs
- The `/escalate-v2` command successfully parallelized P1 (quick checks) and P3 (code investigation) subagents while skipping P2 (reproduction already done by support)

---

*Session captured: 2025-12-23 12:00*
*Command Version: ba98a98*
*Saved by /save-session*
