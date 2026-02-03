# Analyze-Bug Session: IOS-261, FULFMNT-555, FULFMNT-556

**Date:** 2026-02-03
**Command Version (Hash):** 6ab264d
**Linear Issues:** IOS-261, FULFMNT-555, FULFMNT-556
**Classification:** Frontend (iOS) + Backend
**Outcome:** Tickets Created (3 related issues)

---

## Session Summary

iOS users reported documents stuck showing "Uploading" status indefinitely despite successful uploads. Investigation revealed a race condition between `files-backend` and `dotnet-monolith` where blind CAS overwrites cause the `is_uploading` flag to remain `true`. Three tickets were created: iOS defensive fix, backend cleanup script, and root cause investigation.

---

## User Inputs

**Input 1: Initial Report**
> Hey team! Here's the post compiling the findings I currently have for the perpetual document upload issue. I'm in communication with three Logos experiencing this issue.
>
> GenX Roofing - User ID: m37j1rt8ovrwv2czs8lthk9 - iPhone 16 Pro Max - iOS 26.2 - App Version 2026.01.16.8573
> Captain Roofing - User ID: m7drx6mtacxtxmbhvegykqs - iPhone 13 Pro Max - iOS 26.2 - App Version 2026.01.27.8587
> Great Roofing/Great Adjusting - User ID: lgwqk6omq7i97zeyezp0gc5 - iPhone 15 Pro Max - iOS 26.2 - App Version 2026.01.09
>
> Despite not all the devices being on the most recent version, there is one that is and it is still not displaying correctly. Additionally, they've gone through several updates, force quits, uninstalled and reinstalled, etc.
>
> Kira's analysis: Web doesn't look at the is_uploading field at all — if the file appears in the list with size > 0, it shows as complete. iOS reads and trusts the is_uploading field from the backend — if it says true, iOS shows "Uploading" forever. Same document can look fine on web but stuck on iOS.
>
> Proposed fixes: Backend cleanup script (low effort), iOS fallback logic (low effort)

**Input 2: Additional Evidence**
> Key Finding: This is still happening on new uploads
> Found a specific example from a recent customer report:
> jnid: mk1mamg3mgkbpzpv
> date_created: January 5, 2026 (after the Dec 10 fix)
> is_uploading: true (stuck)
> size: 140,816 bytes (file exists, upload succeeded)
>
> What's happening: Troy's Dec 10 fix added CAS protection to files-backend, which helps. But dotnet-monolith still does blind overwrites (CAS = 0), so if a user edits anything on the document while upload processing is happening, the is_uploading field can still get stuck.

**Input 3: Ticket Creation Request**
> User selected "iOS + Backend investigation" but clarified: "Let's create the iOS one for the iOS team and the two backend ones for the Fulfilment team and also reference the relation for each Linear."

**Input 4: Relation Correction**
> "The relation should be for 'IOS-261' now instead of 'MOBL-388'"

**Input 5: Format Request**
> "Do they all reference the relation? Also, can you review the linear ticket hybrid format and update the issues to include that formatting?"

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** Frontend (iOS) + Backend
- **Confidence:** High
- **Reasoning:** Kira's analysis confirmed iOS-specific behavior. Web ignores `is_uploading` field (treats documents with `size > 0` as complete), while iOS trusts the backend flag literally. Same documents appear fine on web but stuck on iOS. However, backend race condition is root cause.

### Investigation Steps
1. Parsed bug report to extract affected customers, device info, and symptoms
2. Ran duplicate check against Mobile team issues (none found)
3. Identified platform difference: Web vs iOS handling of `is_uploading` field
4. Confirmed ongoing issue with evidence document created Jan 5, 2026 (after Dec 10 fix)
5. Identified root cause: `dotnet-monolith` blind overwrites with CAS=0

### Code Analysis
- **Repositories:** `jobnimbus-mobile-ios`, `files-backend`, `dotnet-monolith`
- **Files Examined:**
  - Document display component in iOS (needs investigation for exact file)
  - `files-backend` - has CAS protection (Troy's Dec 10 fix)
  - `dotnet-monolith` - uses CAS=0 (blind overwrite)
- **Root Cause:** Race condition where user edits document metadata during upload causes `dotnet-monolith` to overwrite with CAS=0, leaving `is_uploading = true` stuck

### Fix Proposal
- **Approach:** Three-pronged fix:
  1. iOS: Match web behavior - if `size > 0`, treat as complete regardless of `is_uploading`
  2. Backend: One-time cleanup script to fix existing corrupted documents
  3. Backend: Investigate and fix `dotnet-monolith` CAS behavior
- **Files to Change:**
  - iOS document display component
  - Backend cleanup script (one-time)
  - `dotnet-monolith` document update handlers
- **Risks:** Low for iOS fix (matches web behavior). Medium for monolith CAS changes (could affect other operations).

---

## Outputs

- **Linear Tickets Created:**
  - [IOS-261](https://linear.app/jobnimbus/issue/IOS-261/ios-or-documents-stuck-showing-uploading-when-is-uploading=true-but) - iOS defensive fix (P3)
  - [FULFMNT-555](https://linear.app/jobnimbus/issue/FULFMNT-555/backend-or-cleanup-script-for-documents-stuck-with-is-uploading=true) - Cleanup script (P3)
  - [FULFMNT-556](https://linear.app/jobnimbus/issue/FULFMNT-556/backend-or-investigate-dotnet-monolith-blind-overwrites-causing-is) - Root cause investigation (P2)
- **All tickets related:** IOS-261 ↔ FULFMNT-555 ↔ FULFMNT-556
- **PR Created:** Not created
- **Branch:** N/A

---

## Key Learnings

- **Platform parity matters:** Web's defensive approach (ignore `is_uploading` if `size > 0`) prevents this class of bug entirely. iOS trusting the backend flag made it vulnerable.
- **CAS consistency across services:** Troy's fix to `files-backend` was partial because `dotnet-monolith` still uses blind overwrites. Multi-service systems need consistent concurrency control.
- **Post-fix validation:** The Dec 10 fix didn't fully resolve the issue - evidence document from Jan 5 shows ongoing race condition. Important to verify fixes with real customer data.
- **Three-ticket pattern:** When a bug has data corruption + client display + root cause aspects, creating separate tickets for each allows parallel work across teams.

---

*Session captured: 2026-02-03 18:20*
*Command Version: 6ab264d*
*Saved by /save-session*
