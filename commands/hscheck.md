# HubSpot Link and MRR Check

Check how many HubSpot weblinks are attached to a Linear issue and calculate the total MRR from those tickets.

## Usage

```
/hscheck ISSUE-ID
```

Example: `/hscheck CORE-8387`

## Instructions

1. Extract the Linear issue ID from the user's command (e.g., "CORE-8387")
2. Use the `mcp__plugin_engineering_linear__get_issue` tool to retrieve the issue details
3. Analyze the `attachments` array in the response
4. Count all attachments that have URLs containing "hubspot.com"
5. For each HubSpot attachment:
   - Extract the MRR value from the title if present
   - Look for patterns like "MRR: $X", "MRR: $X.XX", or "MRR: $X,XXX.XX"
   - Parse the numeric value (handling commas and decimals)
6. Calculate the total MRR from all parsed values
7. Display results in this format:

```
## HubSpot Links Analysis for [ISSUE-ID]

**Total HubSpot Links:** [count]
**Total MRR (from specified values):** $[total]

### Breakdown:
- [count] tickets with specified MRR totaling $[amount]
- [count] tickets with unspecified MRR (shown as "MRR: $" without value)
- [count] other attachments (non-HubSpot links like GitHub PRs, etc.)

### Individual HubSpot Tickets:
1. [Title] - $[amount]
2. [Title] - $[amount]
...

### Unspecified MRR:
- [Title]
...
```

## Notes

- Only count attachments with "hubspot.com" in the URL as HubSpot links
- MRR values may appear in various formats: $0, $123.45, $1,234.56
- Some tickets may show "MRR: $" without a number - count these separately
- GitHub PR links and other non-HubSpot attachments should be counted separately
- Handle edge cases where MRR might not be present in the title
- If no HubSpot links are found, display a clear message stating that
