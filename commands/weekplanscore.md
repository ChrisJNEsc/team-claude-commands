---
description: Generate weekly escalations team metrics for fix recommendation effectiveness
---

Generate weekly escalation metrics report for the previous calendar week.

**PURPOSE:**
This command generates a metrics report showing the effectiveness of fix recommendations from the Escalations team. It analyzes Linear tickets marked as "Done" with either "ESC - Plan Applied" or "ESC - Plan Reworked" labels. By default, it looks at the previous calendar week (Monday through Sunday), but you can also specify custom date ranges.

**WORKFLOW:**

1. **ASK ABOUT DATE RANGE:**
   - Use the AskUserQuestion tool to ask the user which date range they want to analyze
   - Provide options:
     - **Previous week (default):** Use the previous calendar week (Monday through Sunday)
     - **Custom dates:** Allow the user to specify their own start and end dates
   - If the user selects "Custom dates", follow up by asking for:
     - Start date (in YYYY-MM-DD format)
     - End date (in YYYY-MM-DD format)

2. **CALCULATE DATE RANGE:**
   - If previous week was selected:
     - Determine today's date
     - Calculate the previous calendar week (Monday 00:00:00 through Sunday 23:59:59)
     - For example, if today is December 15, 2025 (Monday):
       - Previous week: December 8, 2025 (Monday) through December 14, 2025 (Sunday)
   - If custom dates were provided:
     - Use the user-specified start date (00:00:00) through end date (23:59:59)
   - Display the date range being analyzed in the report header

3. **DEFINE TEAM MEMBERS:**
   The Escalations team consists of:
   - **Christopher Berry** (also known as "Chris Berry")
   - **Garrett Young**
   - **Anthony Viglione**
   - **Brandy Kinsman**

4. **FETCH TICKETS FOR EACH LABEL:**
   Execute two parallel queries using mcp__plugin_engineering_linear__list_issues:

   **Query 1 - ESC - Plan Applied:**
   ```
   state: "Done"
   label: "ESC - Plan Applied"
   updatedAt: [ISO date for Monday of previous week]
   limit: 250
   ```

   **Query 2 - ESC - Plan Reworked:**
   ```
   state: "Done"
   label: "ESC - Plan Reworked"
   updatedAt: [ISO date for Monday of previous week]
   limit: 250
   ```

5. **FILTER BY DATE AND CREATOR:**
   For each returned ticket:
   - Verify the ticket was marked "Done" within the date range (check updatedAt)
   - Extract `createdBy` field to identify the creator
   - Only include tickets created by Escalations team members:
     - "Chris Berry" or "Christopher Berry"
     - "Garrett Young"
     - "Anthony Viglione"
     - "Brandy Kinsman"
   - Ignore tickets created by anyone else

6. **CATEGORIZE BY TEAM MEMBER:**
   Create buckets for each team member tracking:
   - Count of "ESC - Plan Applied" tickets
   - Count of "ESC - Plan Reworked" tickets
   - List of ticket identifiers for each category

7. **CALCULATE METRICS:**

   **Per Team Member:**
   - Plan Applied Count
   - Plan Reworked Count
   - Total Tickets
   - Plan Applied Rate = (Plan Applied / Total) * 100%

   **Team Totals:**
   - Total Plan Applied (all members)
   - Total Plan Reworked (all members)
   - Overall Total
   - Overall Plan Applied Rate = (Total Plan Applied / Overall Total) * 100%

8. **GENERATE REPORT:**

```markdown
# Escalations Weekly Metrics Report

**Report Period:** [Monday Date] - [Sunday Date]
**Generated:** [Today's Date]

---

## Team Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| ESC - Plan Applied | [X] | [Y%] |
| ESC - Plan Reworked | [X] | [Y%] |
| **Total Escalations** | **[X]** | **100%** |

**Overall Plan Applied Rate: [X%]**

---

## Individual Performance

### Christopher Berry
| Label | Count | Tickets |
|-------|-------|---------|
| ESC - Plan Applied | [X] | [TICKET-1, TICKET-2, ...] |
| ESC - Plan Reworked | [X] | [TICKET-3, ...] |
| **Total** | **[X]** | |
| **Plan Applied Rate** | **[X%]** | |

### Garrett Young
| Label | Count | Tickets |
|-------|-------|---------|
| ESC - Plan Applied | [X] | [TICKET-1, TICKET-2, ...] |
| ESC - Plan Reworked | [X] | [TICKET-3, ...] |
| **Total** | **[X]** | |
| **Plan Applied Rate** | **[X%]** | |

### Anthony Viglione
| Label | Count | Tickets |
|-------|-------|---------|
| ESC - Plan Applied | [X] | [TICKET-1, TICKET-2, ...] |
| ESC - Plan Reworked | [X] | [TICKET-3, ...] |
| **Total** | **[X]** | |
| **Plan Applied Rate** | **[X%]** | |

### Brandy Kinsman
| Label | Count | Tickets |
|-------|-------|---------|
| ESC - Plan Applied | [X] | [TICKET-1, TICKET-2, ...] |
| ESC - Plan Reworked | [X] | [TICKET-3, ...] |
| **Total** | **[X]** | |
| **Plan Applied Rate** | **[X%]** | |

---

## Notes

- **ESC - Plan Applied:** The developer followed the recommended fix approach from the escalation analysis
- **ESC - Plan Reworked:** The developer took a different approach than recommended (may indicate incorrect diagnosis or valid alternative implementation)
- Tickets without either label are excluded (no plan was recommended)
- Only tickets created by Escalations team members are included
```

**EDGE CASES:**

- **No tickets found:** Report "No escalation tickets were closed during this period"
- **Team member with 0 tickets:** Still include them in the report with 0 counts
- **Division by zero:** If a team member has 0 total tickets, show "N/A" for their percentage

**Example Usage:**
- `/weekplanscore` - Prompts for date range, then generates report
  - Select "Previous week" to use the previous calendar week
  - Select "Custom dates" to specify your own start and end dates

**Output Location:**
- Display the full report in the conversation
- Optionally save to a file if requested
