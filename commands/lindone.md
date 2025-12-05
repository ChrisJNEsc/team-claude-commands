---
description: Validate whether recommended adjustments from a Linear issue were implemented in the corresponding branch
---

Validate Linear issue recommended adjustments against branch commits using: $ARGUMENTS

**PURPOSE:**
This command checks whether the specific recommended adjustments or changes described in a Linear issue have been implemented in the corresponding git branch. It compares the issue's recommendations against actual code changes.

**WORKFLOW:**

1. **Parse Arguments** from $ARGUMENTS to extract:
   - **Issue ID:** Linear issue identifier (e.g., WEB-123, API-456) - REQUIRED
   - **Branch Name:** Optional specific branch name (defaults to issue's suggested branch)
   - **Repository Path:** Optional specific repository path to analyze

2. **FETCH ISSUE DETAILS:**
   - Use mcp__plugin_engineering_linear__get_issue to retrieve the issue
   - Extract the recommended adjustments from the **issue description body ONLY**:
     - Look for "Recommended", "Adjustment", "Change", "Fix", "Modify", "Update" sections
     - Technical requirements section
     - Implementation guidance section
   - **DO NOT use comments for recommendations** - only the issue description body
   - If no plan/recommendations are found in the description body, note this for step 11 (will default to "ESC - Plan Reworked")
   - Identify the expected branch name from issue attachments or git branch name field
   - Note the issue's team prefix for repository correlation

3. **DETERMINE TARGET BRANCH:**
   - **If branch provided:** Use the specified branch name
   - **If issue has git branch:** Use the attached branch name from Linear
   - **If neither:** Construct expected branch name from issue ID (e.g., `feature/WEB-123-*` or `WEB-123-*`)
   - Validate branch exists using: `git branch -a | grep [branch-pattern]`

4. **IDENTIFY RECOMMENDED ADJUSTMENTS:**
   Parse the issue description and comments to extract specific recommendations:
   - **Code Changes:** Files to modify, specific functions/methods to change
   - **Logic Adjustments:** Behavioral changes, new conditions, modified flows
   - **Configuration Changes:** Environment variables, settings, feature flags
   - **API Changes:** Endpoints, request/response modifications
   - **Database Changes:** Schema updates, migration requirements
   - **Test Requirements:** Specific tests to add or modify

   Create a checklist of all identified adjustments with:
   - Adjustment ID (A1, A2, A3...)
   - Description of the recommended change
   - Expected file(s) affected
   - Specific code pattern or keyword to look for

5. **FETCH BRANCH COMMITS:**
   - Use `git log` to get commits on the branch since it diverged from main/master:
     ```
     git log main..[branch-name] --oneline --format="%H %s"
     ```
   - Get the full diff of changes:
     ```
     git diff main...[branch-name]
     ```
   - List all modified files:
     ```
     git diff --name-only main...[branch-name]
     ```

6. **ANALYZE CODE CHANGES:**
   For each file modified in the branch:
   - Read the file content using the Read tool
   - Use `git diff main...[branch-name] -- [file]` to see specific changes
   - Identify what was added, modified, or removed
   - Map changes to the recommended adjustments from step 4

7. **VALIDATE EACH ADJUSTMENT:**
   For each recommended adjustment, determine:
   - **Implemented:** Code change found that addresses the recommendation
   - **Partially Implemented:** Some aspects addressed, others missing
   - **Not Implemented:** No evidence of the recommended change
   - **Differently Implemented:** Change made but approach differs from recommendation

   Provide evidence for each determination:
   - File and line number where change was found
   - Code snippet showing the implementation
   - Explanation of how it addresses (or doesn't address) the recommendation

8. **CHECK COMMIT MESSAGES:**
   - Analyze commit messages for references to the Linear issue ID
   - Verify commits mention the adjustments being made
   - Flag commits that may contain relevant changes but lack proper references

9. **GENERATE VALIDATION REPORT:**

**Recommended Adjustment Validation for [ISSUE-ID]**

**Issue:** [Issue Title]
**Branch:** [Branch Name]
**Commits Analyzed:** [Number of commits]
**Files Changed:** [Number of files]

---

**Summary:**
| Status | Count |
|--------|-------|
| Implemented | [X] |
| Partially Implemented | [X] |
| Not Implemented | [X] |
| Differently Implemented | [X] |

---

**Detailed Adjustment Validation:**

**[A1] [Adjustment Description]**
- **Status:** [Implemented/Partial/Not Implemented/Different]
- **Expected Change:** [What the issue recommended]
- **Actual Change:** [What was found in the code]
- **Evidence:**
  - File: `[file path]:[line number]`
  - Code: `[relevant code snippet]`
- **Gap Analysis:** [If partial/not implemented, what's missing]

**[A2] [Adjustment Description]**
...

---

**Commit Coverage:**
| Commit | Message | Adjustments Addressed |
|--------|---------|----------------------|
| [short hash] | [message] | A1, A3 |
| [short hash] | [message] | A2 |
...

---

**Recommendations:**

**If All Implemented:**
- Ready for code review and testing
- Suggested next steps for the issue

**If Gaps Found:**
- List specific items still needed
- Suggest code changes to complete implementation
- Recommend whether to request changes or create follow-up issue

10. **POST COMMENT TO LINEAR:**
    - Use mcp__plugin_engineering_linear__create_comment to post the validation report as a comment on the Linear issue
    - The comment should include:
      - Summary of recommendations from the issue description
      - What was actually implemented in the branch
      - Status of each recommended adjustment (Implemented/Partially Implemented/Not Implemented/Differently Implemented)
      - Evidence with file paths and code snippets

11. **APPLY LABEL BASED ON RESULTS:**
    - Use mcp__plugin_engineering_linear__update_issue to add the appropriate label:
    - **If NO plan/recommendations were found in the description body:**
      - Add label: `ESC - Plan Reworked` (default when no plan exists)
    - **If recommendations were found AND followed** (majority of adjustments are "Implemented"):
      - Add label: `ESC - Plan Applied`
    - **If recommendations were found but NOT followed** (majority are "Not Implemented" or "Differently Implemented"):
      - Add label: `ESC - Plan Reworked`
    - Decision criteria:
      - "Plan Applied" = Developer followed the recommended approach from the description body
      - "Plan Reworked" = No plan existed OR developer took a different approach than recommended

**Example Usage:**
- `/lindone WEB-123`
- `/lindone API-456 branch feature/api-update`
- `/lindone WEB-789 repo /path/to/repo`

**Smart Behaviors:**
- **Automatic Branch Detection:** Uses Linear's git integration to find the associated branch
- **Semantic Matching:** Understands different implementations of the same recommendation
- **Evidence-Based:** Provides specific code references for all determinations
- **Actionable Results:** Clear next steps based on validation outcome
- **Issue Integration:** Can update Linear with validation results

**Error Handling:**
- **Issue Not Found:** Prompt user to verify issue ID and Linear access
- **Branch Not Found:** List available branches matching issue pattern, ask for clarification
- **No Recommendations Found:** Check issue format, suggest checking comments or linked documents
- **Repository Not Found:** Prompt for correct repository path
