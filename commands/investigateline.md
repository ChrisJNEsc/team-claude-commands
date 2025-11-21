# Investigate and Create Customer Request Ticket

Create a new Linear ticket for a customer-reported bug with optional code investigation and fix planning.

## Workflow

### 1. Gather Initial Information
Ask the user for:
- Ticket title (short, descriptive)
- Feature description (what's affected - be specific)

### 2. Check for Duplicates
Search Linear for existing issues:
- Extract key terms from title/feature (e.g., "invoice payment error" not "the invoice system has an error")
- Use `list_issues` with: `query: [key terms]`, `limit: 10`, `orderBy: updatedAt`, `updatedAt: -P30D`
- For each result, use `get_issue` to check full description
- Analyze confidence: High/Medium/Low that each is a duplicate (explain why)

If potential duplicates found:
- Show: ID, title, status, URL, confidence assessment
- Ask user: "Is this a duplicate?" (If yes → stop, provide URL. If no → continue)

If no duplicates → continue to step 3

### 3. Gather All Issue Details
**Ask user to provide (in ONE question):**
- Date & Time Issue Occurred
- Company JN ID
- User JN ID
- Affected Record
- Replicable in Customer's Account? (Y/N)
- Replicable in Test Account? (Y/N)
- Test Account Replicated in (if yes)
- Record Replicated with (if yes)
- Prerequisites (or "None")
- Steps to Replicate (start with "Login to JobNimbus on [platform]...")
- Expected Result
- Actual Result
- Steps to View (or "Same as replication")
- Screenshots (URLs or "None")
- User Recording/Zoom Meeting (URLs or "None")
- Specific Troubleshooting (or "None")
- Additional Information (or "None")

### 4. Optional Code Investigation
Ask once: **"Investigate code related to this issue?"**

If yes:
- Identify likely repository based on feature/area
- Use Task tool (subagent_type=Explore) to locate relevant code
- Present findings:
  - Confidence level (High/Medium/Low) with reasoning (cross-reference JobNimbus architecture knowledge)
  - Repository name
  - File paths with line numbers
  - Code snippets
  - How code relates to issue
- Ask once: **"Create fix plan?"**
  - If yes → provide: Root cause, solution approach, files to modify, risks, testing recommendations

Store investigation + fix plan for ticket description.

### 5. AI Recommendation + User Override
Analyze feature description and determine:
- **Team**: Use team ownership logic (see mapping below when needed)
- **Priority**: Based on impact/scope
  - P1 (Urgent): Critical, multiple customers, blocking
  - P2 (High): Significant customer impact
  - P3 (Normal): Standard bug
  - P4 (Low): Minor, minimal impact

Present: **"Based on [feature], I recommend Team: [X], Priority: [Y]. Reasoning: [brief]. Correct?"**
- Let user confirm or override team/priority in same interaction

### 6. Create Linear Issue
Use `create_issue` with:
- Team: from step 5
- Title: from step 1
- Description: formatted template (see below)
- Priority: from step 5 (Urgent=1, High=2, Normal=3, Low=4)
- Label: "Bug - Customer Reported"
- State: "Triage"

### 7. Confirm Creation
Display: ticket ID, URL, git branch name

---

## Ticket Description Template

```
**Description:** [Feature description]
**Date & Time Issue Occurred:** [Date/Time]
**Company JN ID:** [ID]
**User JN ID:** [ID]
**Affected Record:** [Record]

**Replicable in Customer's Account?** [Y/N]
**Replicable in Test Account?** [Y/N]
**Test Account Replicated in:** [ID or N/A]
**Record Replicated with:** [Record or N/A]

**Prerequisites:**
[Details or None]

**Steps to Replicate:**
[Steps]

**Expected Result:** [Expected]
**Actual Result:** [Actual]

**Steps to View:**
[Steps or "Same as replication"]

**Screenshots:** [URLs or None]
**User Recording/Zoom Meeting:** [URLs or None]

**Specific Troubleshooting:**
[Details or None]

**Additional Information:**
[Details or None]

---

## Code Investigation

**Confidence Level:** [High/Medium/Low with reasoning, or N/A]
**Repository:** [Repo name or N/A]
**Relevant Files:** [Files with line numbers, or N/A]
**Code Analysis:** [Explanation or N/A]

## Fix Plan

**Root Cause:** [Analysis or N/A]
**Proposed Solution:** [Approach or N/A]
**Files to Modify:** [List or N/A]
**Risks/Side Effects:** [Details or N/A]
**Testing Recommendations:** [Tests or N/A]
```

---

## Team Ownership Mapping

**Reference this when team is unclear from context:**

| Team | Features | APIs | Settings |
|------|----------|------|----------|
| **Fulfillment** | Engage, Email, Material Orders, Notifications, @Mention, Products & Services, Work Orders | Beacon, ABC, SRS, Simplii, Podium | Suppliers |
| **CoreCRM** | Boards, Contact/Job Details, Navigation/Search, Home Page, Tasks, Activity Feed, Calendar, Import Contacts, Photos, Documents, E-Signature, Forms | Public API, Zapier, Google Calendar, Outlook Calendar, CompanyCam, Google Maps | General, Automations, Features, Templates, Custom Fields, Task Type, Note Type, Workflows |
| **Marketing** | Assist AI, Leads, Marketing Hub | Contractor Boost | Lead Source |
| **Accounting** | Invoices, Credit Memos, Legacy Budgets, Profit Tracker, Legacy Proposals | QuickBooks | Tax |
| **FinTech** | JobNimbus Payments, Manual Payments, Job Deposits, Payouts, Payments Dashboard | Global Pay, Wise Tack, Sunlight Financial, WePay | Payments, Financing |
| **Sales** | NSE Estimates, Estimate Sidebar, Legacy Estimates, Smart Estimates, SumoQuote, Measurements, Layout Library, Insights, Classic Reports | EagleView, HOVER, mySalesman, NaturalForms, HailTrace, SalesRabbit, Xactimate, Leap | |
| **Mobile** | iOS App, Android App | | |
| **Account Platform** | Admin Panel, Feature Gating, Trial Accounts, Login/Authentication | | Access Profiles, Groups, Locations, Subscription, Teams |

If still unclear, ask user to select from: Fulfillment, CoreCRM, Marketing, Accounting, FinTech, Sales, Mobile, Account Platform

---

## Important Notes
- Always check for duplicates before creating tickets
- Always set state="Triage" and label="Bug - Customer Reported"
- Code investigation is optional - ask once early in process
- If investigation not performed, set those sections to "N/A"
- Batch user questions to minimize interactions
- Parallelize tool calls when no dependencies exist
- Use N/A or None for missing fields
