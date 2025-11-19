# New Customer Request Ticket

Create a new Linear ticket for a customer-reported bug or issue.

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
     - If no, continue to step 4
   - If no potential duplicates found, continue to step 4

3. **Gather Customer Information**: Ask the user to provide the following information:
   - Date & Time Issue Occurred
   - Customer Login
   - Company JN ID
   - User JN ID

4. **Determine Team Ownership**: Analyze the feature description from step 1 to identify which feature or area is affected. Use the Team Ownership Mapping above to determine the appropriate Linear team. If it's unclear which team should own this ticket, use the AskUserQuestion tool to ask the user which team it belongs to, presenting these options:
   - Fulfillment
   - CoreCRM
   - Marketing
   - Accounting
   - FinTech
   - Sales
   - Mobile
   - Account Platform

5. **Gather Replication Information**: Use the AskUserQuestion tool to ask:
   - Replicable in Customer's Account? (Yes/No)
   - Allowed to Test in Customer's Account? (Yes/No)
   - Record to Test with
   - Replicable in Test Account? (Yes/No)
   - Test Account Replicated in
   - Record Replicated with

6. **Gather Prerequisites**: Use the AskUserQuestion tool to ask:
   - Prerequisites (any setup or conditions needed)

7. **Gather Steps to Replicate**: Use the AskUserQuestion tool to ask:
   - Steps to Replicate (detailed step-by-step)
   - Expected Result
   - Actual Result

8. **Gather View Information**: Use the AskUserQuestion tool to ask:
   - Steps to View
   - Last Known Date Feature Functioned as Designed

9. **Gather Supporting Materials**: Use the AskUserQuestion tool to ask:
   - Screenshots (URLs or "None")
   - User Recording/Zoom Meeting (URLs or "None")
   - LogRocket Session (URL or "None")

10. **Gather Basic Troubleshooting**: Use the AskUserQuestion tool to ask:
    - Logged Out/In? (Yes/No)
    - Tested in Incognito/Cleared Cache? (Yes/No)
    - Browsers/Versions Replicable in
    - Devices Replicable with
    - Internet Speed
    - Antivirus
    - Extensions
    - Pop-up Blockers

11. **Gather Specific Troubleshooting and Additional Info**: Use the AskUserQuestion tool to ask:
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
**Date & Time Issue Occurred:** [From step 3]
**Customer Login:** [From step 3]
**Company JN ID:** [From step 3]
**User JN ID:** [From step 3]
**Replicable in Customer's Account?** [From step 5]
**Allowed to Test in Customer's Account?** [From step 5]
**Record to Test with:** [From step 5]
**Replicable in Test Account?** [From step 5]
**Test Account Replicated in:** [From step 5]
**Record Replicated with:** [From step 5]
**Prerequisites:** [From step 6]
**Steps to Replicate:** [From step 7]
**Expected Result:** [From step 7]
**Actual Result:** [From step 7]
**Steps to View:** [From step 8]
**Last Known Date Feature Functioned as Designed:** [From step 8]
**Screenshots:** [From step 9]
**User Recording/Zoom Meeting:** [From step 9]
**LogRocket Session:** [From step 9]
**Basic Troubleshooting:** Logged Out/In: [From step 10] | Tested in Incognito/Cleared Cache: [From step 10] | Browsers/Versions: [From step 10] | Devices: [From step 10] | Internet Speed: [From step 10] | Antivirus: [From step 10] | Extensions: [From step 10] | Pop-up Blockers: [From step 10]
**Specific Troubleshooting:** [From step 11]
**Additional Information:** [From step 11]
```

14. **Create the Issue**: Use the Linear create_issue tool with:
    - The determined/selected team from step 4
    - The provided title from step 1
    - The formatted description from step 13
    - Priority mapped from the selection (Urgent=1, High=2, Normal=3, Low=4)
    - Label: "Bug-Customer Reported" (use this exact label name)
    - State: "Triage"

15. **Confirm Creation**: Display the created ticket details including the identifier, URL, and git branch name.

## Important Notes
- Always set the status to "Triage" for new customer requests
- Always include the "Bug-Customer Reported" label
- Always check for existing/duplicate issues before creating a new ticket (step 2)
- If a duplicate is found, do not create a new ticket - provide the existing issue URL instead
- Follow the exact template format for the description
- If any field is not provided or not applicable, write "N/A" or "None" as appropriate
- Maintain consistent formatting with markdown for readability
- If any step fails, provide clear error information to the user
