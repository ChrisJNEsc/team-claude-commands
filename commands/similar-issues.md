# Similar Issues Search

You are helping a support escalations engineer find similar issues to the one they're currently investigating.

## Your Task

Search for similar bugs, issues, and fixes across multiple sources and present findings in a clear, actionable format.

## Search Strategy

Execute the following searches in parallel:

1. **Linear Issues Search**
   - Search Linear for issues with similar keywords in title/description
   - Look for both open and closed issues
   - Prioritize recently updated issues and those marked as bugs
   - Include issues from the last 6 months

2. **Git History Search**
   - Search commit messages for related keywords
   - Look for commits that mention "fix", "bug", "issue" with similar terms
   - Search for related error messages or stack traces if provided

3. **Code Search**
   - If specific error messages or stack traces are mentioned, search the codebase for those
   - Look for related error handling or validation code
   - Find files that might be related to the issue area

## Output Format

Present your findings as:

### Linear Issues
- List relevant issues with: ID, title, status, last updated date
- Include a brief note on why each is relevant
- Highlight if any were recently closed (might be regression)

### Git History
- List relevant commits with: hash (short), date, message
- Include file paths if relevant
- Note if the fix was recent or if there are multiple fixes for similar issues

### Code Patterns
- Show relevant code locations that handle similar errors or logic
- Highlight any known workarounds or validation patterns

### Recommendations
- Is this likely a known issue or regression?
- Are there existing tickets to link to?
- Any patterns suggesting root cause area?

## Important Notes
- Cast a wide net initially, then narrow down
- If you find a closed issue that's very similar, flag it as a potential regression
- If you find multiple fixes for the same area, flag it as a potential hotspot
- Always provide the Linear issue IDs so the user can quickly navigate to them
