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
- **Include a confidence rating (High/Medium/Low)** indicating how similar this issue is to the current investigation
- Include a brief note on why each is relevant and what the confidence rating is based on
- Highlight if any were recently closed (might be regression)

### Git History
- List relevant commits with: hash (short), date, message
- **Include a confidence rating (High/Medium/Low)** for relevance to the current issue
- Include file paths if relevant
- Note if the fix was recent or if there are multiple fixes for similar issues

### Code Patterns
- Show relevant code locations that handle similar errors or logic
- **Include a confidence rating (High/Medium/Low)** on whether this code is related to the issue
- Highlight any known workarounds or validation patterns

### Recommendations
- Is this likely a known issue or regression?
- Are there existing tickets to link to?
- Any patterns suggesting root cause area?
- **Provide an overall confidence assessment** on whether you've found truly similar issues

## Confidence Rating Guidelines

Use these criteria when assigning confidence ratings:

**High Confidence (🟢)**
- Exact match of error messages or stack traces
- Same components/files affected
- Identical or near-identical symptoms
- Recent similar fix or closed issue with same behavior

**Medium Confidence (🟡)**
- Related error types or patterns
- Same general area of codebase
- Similar but not identical symptoms
- Related keywords and context match

**Low Confidence (🟠)**
- Tangentially related issues
- Same broad category but different specifics
- Weak keyword matches
- Worth mentioning but may not be directly related

## Important Notes
- Cast a wide net initially, then narrow down
- If you find a closed issue that's very similar, flag it as a potential regression
- If you find multiple fixes for the same area, flag it as a potential hotspot
- Always provide the Linear issue IDs so the user can quickly navigate to them
