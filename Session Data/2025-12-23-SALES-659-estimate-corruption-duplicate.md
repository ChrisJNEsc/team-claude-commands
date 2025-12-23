# Analyze-Bug Session: SALES-659 (Estimate Corruption - Duplicate)

**Date:** 2025-12-23
**Command Version (Hash):** 3db4ec1
**Command Used:** /escalate-v2
**Linear Issue:** SALES-659 (existing duplicate)
**Classification:** Frontend (NSE - New Sales Experience)
**Outcome:** Duplicate Found - No new ticket created

---

## Session Summary

Customer reported estimates 30468 and 30469 on Job #7059 became "corrupted" after being sent - they won't load, won't edit, and customers see "Network Error" when trying to sign. Investigation via `/escalate-v2` quickly identified this as a duplicate of existing ticket SALES-659 "Related Entity Estimates don't load" which is already in Ready for Dev status.

---

## User Inputs

**Input 1: Initial Report**
> Support - Web Escalation
> Troubleshooting Steps Taken: Clear Cache, Incognito, Logout/Login, Restart Computer, Refresh Browser
> Who Verified the Escalation? Brandy Kinsman
> Escalated By: EJ Hammond
> Brief Description of Issue: An estimate got corrupted after it was sent. When the customer tries to sign, they are met with a "Network Error" message. When trying to duplicate the estimate to send out, the corruption stuck, as expected.
> User ID: c15o9
> Date/Time Issue Occurred: 12/19 - 11:59am
> Specific Record Impacted: Job - #7059 - Estimates - 30468 and 30469
> Steps to Replicate / Steps to View: By either trying to view or edit either of the estimates above.
> Expected Results: The estimate will load and be editable. As well as the customer will be able to sign the estimate successfully.
> Actual Results: The estimate will not load and will not be editable. As well as the customer is not able to sign the estimate successfully.
> Can you Replicate in Logo's Account? Yes
> Did you Test in Test Account? No
> Can you Replicate in Test Account? No
> Computer OS Type and Version: Windows
> Browser Type and Version: Chrome

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Frontend (NSE Estimates)
- **Confidence:** High
- **Reasoning:** Issue involves estimate loading/editing in the New Sales Experience (NSE), with "Network Error" on customer signing page - all frontend-related symptoms tied to estimate routing.

### Investigation Steps
1. **Phase 0 - Input Processing:** Parsed escalation details, extracted key identifiers (user c15o9, estimates 30468/30469, Job #7059)
2. **Phase 1 - Quick Checks:** Launched P1 subagent to search Linear for duplicates and documentation
3. **Duplicate Search Results:** Found SALES-659 with high confidence match
4. **Duplicate Verification:** Retrieved full issue details from Linear to confirm match

### Duplicate Analysis
- **Existing Issue:** SALES-659 - "Related Entity Estimates don't load"
- **Match Confidence:** HIGH
- **Why it matches:**
  - Both issues: Estimates fail to load/edit
  - Both issues: NSE-related (New Sales Experience)
  - Root cause in SALES-659: When loading estimates for related entities, NSE uses wrong projectId from route params
  - SALES-659 describes: "We use the projectId route param throughout the codebase, and some relations are off"
  - Customer symptoms align: "Network Error" = failed API calls due to incorrect project routing

### Root Cause (from SALES-659)
- **Repository:** jobnimbus-frontend (NSE)
- **Problem:** When an estimate for a related entity is loaded from the main entity, NSE cannot find the appropriate project
- **Technical Detail:** Loading estimate on contact DEF from job ABC uses route `/jobs/ABC/estimates/{estimateId}` but the estimate belongs to a different project
- **Fix Direction:** `workingProject` should get set from `workingReport.ReportDBId` instead of route param

---

## Outputs

- **Linear Ticket:** SALES-659 (existing - duplicate)
  - URL: https://linear.app/jobnimbus/issue/SALES-659/related-entity-estimates-dont-load
  - Status: Ready for Dev
  - Team: Sales
- **PR Created:** Not created (duplicate)
- **Branch:** `brandykinsman/sales-659` (existing branch for SALES-659)

---

## Key Learnings

1. **"Corrupted estimate" often means routing issue:** Customer perception of "corruption" was actually a routing/loading failure, not data corruption
2. **Network Error = API failure:** "Network Error" on signing page typically indicates the frontend is making API calls with wrong parameters (in this case, wrong projectId)
3. **Duplicate persists corruption:** The fact that duplicating the estimate "kept the corruption" makes sense - the duplicate still references the same related entity relationship that causes the routing bug
4. **NSE Related Entity pattern:** This is a known pattern with NSE - estimates created on related entities (contacts vs jobs) have routing issues

---

## Process Notes

- **Command Used:** `/escalate-v2` (subagent architecture)
- **Phase Reached:** Phase 1 (Quick Checks) - stopped at duplicate detection
- **Time to Resolution:** Fast - high-confidence duplicate found immediately
- **Phases Skipped:** P2 (Reproduction), P3 (Code Investigation) - not needed due to duplicate

---

*Session captured: 2025-12-23 11:31*
*Command Version: 3db4ec1*
*Saved by /save-session*
