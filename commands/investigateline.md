# Investigate and Create Customer Request Ticket

Create a new Linear ticket for a customer-reported bug or issue with optional code investigation and fix planning.

## Team Ownership Mapping

Use the following mapping to determine which Linear team owns specific features:

**Fulfillment (Team: Fulfillment)**
- Features: Engage, Email, Material Orders (Legacy + New), Notifications, @Mention, Products & Services, Work Orders
- APIs: Beacon API, ABC API, SRS API, Simplii API, Podium API
- Settings: Suppliers

**Core CRM (Team: CoreCRM)**
- Features: Boards, Contact/Job Details, Navigation/Search, Home Page, Tasks, Activity Feed (Notes), Calendar, Import Contacts, Photos, Documents, E-Signature, Forms
- APIs: Public API, Zapier API, Google Calendar API, Outlook Calendar API, CompanyCam API, Google Maps API
- Settings: General, Automations, Features, Templates, Custom Fields, Task Type, Note Type, Contact/Job Workflows

**Marketing (Team: Marketing)**
- Features: Assist AI, Leads, Marketing Hub
- APIs: Contractor Boost API
- Settings: Lead Source

**Accounting (Team: Accounting)**
- Features: Invoices, Credit Memos, Legacy Budgets, Profit Tracker, Legacy Proposals
- APIs: QuickBooks API
- Settings: Tax

**FinTech (Team: FinTech)**
- Features: JobNimbus Payments, Manual Payments, Job Deposits, Payouts, Payments Dashboard
- APIs: Global Pay, Wise Tack, Sunlight Financial, WePay
- Settings: Payments, Financing

**Sales (Team: Sales)**
- Features: NSE Estimates, Estimate Sidebar, Legacy Estimates, Smart Estimates, SumoQuote Standalone, Measurements, Layout Library, Insights, Classic Reports
- APIs: EagleView API, HOVER API, mySalesman API, NaturalForms API, HailTrace API, SalesRabbit API, Xactimate API, Leap API

**Mobile (Team: Mobile)**
- Features: iOS App, Android App

**Account Platform (Team: Account Platform)**
- Features: Admin Panel, Feature Gating, Trial Accounts, Login/Authentication
- Settings: Access Profiles, Groups, Locations, Subscription, Teams

## Instructions

Follow these steps to create a customer request ticket:

1. **Gather Initial Information**: Ask the user to provide the following information:
   - Ticket title (short, descriptive)
   - Feature description (what feature is affected - be specific)

2. **Check for Existing Issues**: Before continuing, search for potential duplicate issues in Linear:
   - Use the Linear list_issues tool to search across all teams with:
     - query: Extract key terms from the title and feature description from step 1
     - limit: 10
     - orderBy: updatedAt
     - updatedAt: -P30D (search last 30 days)
   - For each search result, use the get_issue tool to retrieve the full description
   - Review both the title and description/content of each issue to identify similarities
   - Analyze the results and provide a confidence level:
     - If potential duplicates found: State your confidence level (e.g., "High confidence", "Medium confidence", "Low confidence") that each issue is a duplicate and explain why
     - If no duplicates found: State your confidence level (e.g., "High confidence of no duplicates", "Medium confidence of no duplicates") and explain why
   - If potential duplicates are found:
     - Display the matching issues with their identifiers, titles, status, URLs, and your confidence assessment
     - Use the AskUserQuestion tool to ask if this is a duplicate of any existing issue
     - If yes, stop the process and provide the existing issue URL
     - If no, continue to step 3
   - If no potential duplicates found, continue to step 3

3. **Code Investigation (Optional)**: Use the AskUserQuestion tool to ask if the user wants to locate the code related to the cause of this issue. If yes:
    - Analyze the feature description from step 1
    - Identify the most likely repository where this code lives based on the feature/area
    - Use the Task tool with subagent_type=Explore to locate the relevant code files and functions
    - Search for code related to the reported issue using the feature details and error messages
    - Present your findings to the user, including:
      - Confidence level (e.g., "High confidence", "Medium confidence", "Low confidence") with explanation of why. Cross-refrence the findings with knowledge on how JobNimbus operates to help your confidence level assessment.
      - Repository name
      - Relevant file paths with line numbers
      - Code snippets that are likely responsible
      - Brief explanation of how this code relates to the issue
    - After presenting findings, use the AskUserQuestion tool to ask if the user wants to develop a plan to fix the code
    - If yes to fix plan:
      - Analyze the identified code and the issue details
      - Create a detailed plan to resolve the issue, including:
        - Root cause analysis
        - Proposed solution approach
        - Files that need to be modified
        - Potential risks or side effects
        - Testing recommendations
      - Present this plan to the user
    - Store the investigation findings and fix plan (if created) to include in the Linear ticket

4. **Gather Customer Information**: Ask the user to provide the following information:
   - Date & Time Issue Occurred
   - Company JN ID
   - User JN ID
   - Affected Record

5. **Determine Team Ownership**: Analyze the feature description from step 1 to identify which feature or area is affected. Use the Team Ownership Mapping above to determine the appropriate Linear team. If it's unclear which team should own this ticket, use the AskUserQuestion tool to ask the user which team it belongs to, presenting these options:
   - Fulfillment
   - CoreCRM
   - Marketing
   - Accounting
   - FinTech
   - Sales
   - Mobile
   - Account Platform

6. **Gather Replication Information**: Ask the user to provide the following information:
   - Replicable in Customer's Account? (Yes/No)
   - Replicable in Test Account? (Yes/No)
   - Test Account Replicated in
   - Record Replicated with

7. **Gather Prerequisites**: Ask the user to provide:
   - Prerequisites (any setup or conditions needed)

8. **Gather Steps to Replicate**: Ask the user to provide:
   - Steps to Replicate (detailed step-by-step, should start with "Login to JobNimbus on [platform]...")
   - Expected Result
   - Actual Result

9. **Gather View Information**: Ask the user to provide:
   - Steps to View (should start with "Login to JobNimbus on [platform]...")

10. **Gather Supporting Materials**: Ask the user to provide:
    - Screenshots (URLs or "None")
    - User Recording/Zoom Meeting (URLs or "None")

11. **Gather Troubleshooting and Additional Info**: Ask the user to provide:
    - Specific Troubleshooting (any specific steps taken)
    - Additional Information (any other relevant details)

12. **Ask Priority**: Use the AskUserQuestion tool to ask for the priority level with these options:
    - **Urgent (P1)**: Critical issue affecting multiple customers or blocking critical functionality
    - **High (P2)**: Significant issue affecting customer experience
    - **Normal (P3)**: Standard priority for most bugs
    - **Low (P4)**: Minor issue with minimal impact

13. **Format the Description**: Format all collected information into this exact template:

```
**Description:** [Feature description from step 1]
**Date & Time Issue Occurred:** [From step 4]
**Company JN ID:** [From step 4]
**User JN ID:** [From step 4]
**Affected Record:** [From step 4]


**Replicable in Customer's Account?** [From step 6]
**Replicable in Test Account?** [From step 6]
**Test Account Replicated in:** [From step 6]
**Record Replicated with:** [From step 6]


**Prerequisites:**
[From step 7]


**Steps to Replicate:**
[From step 8]

**Expected Result:** [From step 8]
**Actual Result:** [From step 8]


**Steps to View:**
[From step 9]


**Screenshots:** [From step 10]
**User Recording/Zoom Meeting:** [From step 10]


**Specific Troubleshooting:**
[From step 11]


**Additional Information:**
[From step 11]

---

## Code Investigation

**Confidence Level:** [From step 3, confidence level with explanation, or "N/A" if not performed]
**Repository:** [From step 3, or "N/A" if not performed]
**Relevant Files:** [From step 3, list files with line numbers, or "N/A"]
**Code Analysis:** [From step 3, explanation of code related to issue, or "N/A"]

## Fix Plan

**Root Cause:** [From step 3, or "N/A" if fix plan not created]
**Proposed Solution:** [From step 3, or "N/A"]
**Files to Modify:** [From step 3, or "N/A"]
**Risks/Side Effects:** [From step 3, or "N/A"]
**Testing Recommendations:** [From step 3, or "N/A"]
```

14. **Create the Issue**: Use the Linear create_issue tool with:
    - The determined/selected team from step 5
    - The provided title from step 1
    - The formatted description from step 13 (including code investigation and fix plan if performed)
    - Priority mapped from the selection (Urgent=1, High=2, Normal=3, Low=4)
    - Label: "Bug-Customer Reported" (use this exact label name)
    - State: "Triage"

15. **Confirm Creation**: Display the created ticket details including the identifier, URL, and git branch name.

## Important Notes
- Always set the status to "Triage" for new customer requests
- Always include the "Bug-Customer Reported" label
- Always check for existing/duplicate issues before creating a new ticket (step 2)
- If a duplicate is found, do not create a new ticket - provide the existing issue URL instead
- Code investigation (step 3) is optional - ask the user if they want to perform it
- Code investigation happens EARLY in the process (after checking for duplicates, before gathering customer details) to help understand the issue better
- If code investigation is performed, include all findings and fix plan in the Linear ticket description
- If code investigation is not performed, set those fields to "N/A" in the description
- Follow the exact template format for the description
- If any field is not provided or not applicable, write "N/A" or "None" as appropriate
- Maintain consistent formatting with markdown for readability
- If any step fails, provide clear error information to the user
