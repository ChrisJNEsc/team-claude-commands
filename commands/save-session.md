---
description: Save /analyze-bug session context to shared GitHub repository for team learning
alwaysAllow:
  - Bash
  - Read
  - Write
  - Glob
---

# Save Analyze-Bug Session Command

Capture and share the current `/analyze-bug` session context to the team repository.

**Purpose:** Document investigation sessions for team learning, pattern recognition, and process improvement.

**Rules:**
- Do NOT ask for user input - extract everything from the conversation context
- If Linear ID is unknown, use `[UNKNOWN]` in the filename
- Execute all steps automatically
- Push to: https://github.com/ChrisJNEsc/team-claude-commands (Session Data folder)

---

## Step 1: Get Command Version Hash

Run immediately to capture the analyze-bug command version:

```bash
HASH=$(cd ~/.claude/plugins/cache/jobnimbus/support/*/commands/bug-analysis 2>/dev/null && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "Command Hash: $HASH"
```

If "unknown", try alternate path:
```bash
HASH=$(cd ~/.claude/marketplaces/jobnimbus/plugins/support/commands/bug-analysis 2>/dev/null && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
```

Store this hash for the session file.

---

## Step 2: Extract Session Context from Conversation

Scan the **current conversation** and automatically extract:

### 2.1 User Inputs
Capture ALL user messages from the session verbatim:
- Initial bug report or HubSpot URL
- Answers to clarifying questions
- Additional context provided
- Decisions made

Format each as:
```
**User Input [N]:**
> [exact user message]
```

### 2.2 Claude's Thinking & Analysis
Document Claude's investigation process:
- Phase reached (1-5 from analyze-bug command)
- Classification decision (Frontend/Backend) with reasoning
- Duplicate check results
- Code investigation findings
- Root cause analysis
- Any reasoning or decision-making shown

### 2.3 Outputs & Findings
- Root cause identified (or "Not determined")
- Files/lines involved (or "N/A")
- Proposed fix approach (or "N/A")
- Linear ticket ID - extract if mentioned, otherwise "[UNKNOWN]"
- PR created (if any, otherwise "N/A")

---

## Step 3: Auto-Detect Linear ID

Search the conversation for:
- Linear ticket IDs matching pattern: `[A-Z]+-[0-9]+` (e.g., WEB-123, API-456)
- URLs containing `linear.app/jobnimbus/issue/`
- References to "created ticket" or "Linear issue"

**If found:** Use the Linear ID for the filename
**If not found:** Use `[UNKNOWN]` with a topic slug derived from the issue

---

## Step 4: Generate Session File

Create markdown file with this structure:

```markdown
# Analyze-Bug Session: [LINEAR-ID or TOPIC]

**Date:** [YYYY-MM-DD]
**Command Version (Hash):** [hash from Step 1]
**Linear Issue:** [LINEAR-ID or UNKNOWN]
**Classification:** [Frontend/Backend/Unknown]
**Outcome:** [Resolved/Ticket Created/Needs Follow-up/Investigation Only]

---

## Session Summary

[2-3 sentence summary of the issue and investigation outcome]

---

## User Inputs

**Input 1: Initial Report**
> [user's first message verbatim]

**Input 2:**
> [next user message verbatim]

[continue for all user inputs]

---

## Claude's Analysis & Thinking

### Classification
- **Decision:** [Frontend/Backend]
- **Confidence:** [High/Med/Low]
- **Reasoning:** [why this classification was made]

### Investigation Steps
[Document the logical flow of investigation]

### Code Analysis
- **Repository:** [repo name or "Not identified"]
- **Files Examined:**
  - `[file:line]` - [findings]
- **Root Cause:** [identified cause or "Not determined"]

### Fix Proposal
- **Approach:** [description or "None proposed"]
- **Files to Change:** [list or "N/A"]
- **Risks:** [identified risks or "N/A"]

---

## Outputs

- **Linear Ticket:** [TICKET-ID with URL or "Not created"]
- **PR Created:** [PR URL or "Not created"]
- **Branch:** [branch name or "N/A"]

---

## Key Learnings

- [Any patterns, insights, or learnings from this session]

---

*Session captured: [YYYY-MM-DD HH:MM]*
*Command Version: [hash]*
*Saved by /save-session*
```

---

## Step 5: Save and Push to GitHub

**A. Determine filename:**

If Linear ID found:
```
[YYYY-MM-DD]-[LINEAR-ID].md
```

If no Linear ID:
```
[YYYY-MM-DD]-[UNKNOWN]-[topic-slug].md
```

**B. Ensure target repo is ready:**
```bash
cd ~/.claude/commands/escalations
git checkout main
git pull origin main
```

**C. Write file to Session Data folder:**
Use the Write tool to save to:
```
~/.claude/commands/escalations/Session Data/[filename]
```

**D. Commit and push:**
```bash
cd ~/.claude/commands/escalations
git add "Session Data/"
git commit -m "$(cat <<'EOF'
Add analyze-bug session: [LINEAR-ID or topic]

Date: [YYYY-MM-DD]
Command version: [hash]
Outcome: [brief outcome]

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
git push origin main
```

---

## Step 6: Output Confirmation

```
Session Saved

File: Session Data/[filename]
Command Version: [hash]
Linear ID: [ID or UNKNOWN]

View at: https://github.com/ChrisJNEsc/team-claude-commands/blob/main/Session%20Data/[filename]
```

---

## Error Handling

- **No analyze-bug session detected:** Create file anyway with available conversation context, note "No /analyze-bug command detected in session"
- **Git push fails:** Save file locally, output manual push command: `cd ~/.claude/commands/escalations && git push origin main`
- **Command version unknown:** Use "unknown" as hash value

---

## Usage

Run after completing an `/analyze-bug` session:
```
/save-session
```

The command automatically extracts all information from the current conversation.
