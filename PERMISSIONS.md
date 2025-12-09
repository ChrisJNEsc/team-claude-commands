# Required Permissions

Team commands require certain permissions to run without prompts. Add these to your `~/.claude/settings.json` in the `permissions.allow` array.

## Quick Setup

Copy these permissions to your settings file:

```json
{
  "permissions": {
    "allow": [
      "Bash(gh pr list:*)",
      "Bash(gh search prs:*)",
      "Bash(gh api:*)",
      "Bash(gh repo list:*)",
      "mcp__plugin_engineering_linear__get_*",
      "mcp__plugin_engineering_linear__list_*",
      "mcp__plugin_engineering_linear__search_*",
      "mcp__plugin_engineering_linear__create_*",
      "mcp__plugin_engineering_linear__update_*"
    ]
  }
}
```

## Per-Command Permissions

Each command file includes a `permissions` field in its frontmatter listing required permissions. Check individual command files for specifics.

### GitHub CLI Commands

| Permission | Used By | Purpose |
|------------|---------|---------|
| `Bash(gh pr list:*)` | pr-status | List PRs in repos |
| `Bash(gh search prs:*)` | pr-status | Search PRs across org |
| `Bash(gh api:*)` | pr-status | Get user info, API calls |
| `Bash(gh repo list:*)` | pr-status | List org repositories |

### Linear MCP Commands

| Permission | Used By | Purpose |
|------------|---------|---------|
| `mcp__plugin_engineering_linear__get_*` | pr-status, escalate, investigateline | Fetch issue details |
| `mcp__plugin_engineering_linear__list_*` | escalate, similar-issues | List issues, labels, teams |
| `mcp__plugin_engineering_linear__search_*` | similar-issues | Search Linear docs |
| `mcp__plugin_engineering_linear__create_*` | newreq, escalate | Create issues/comments |
| `mcp__plugin_engineering_linear__update_*` | lindone | Update issue status |

## Verifying Your Setup

Run `/pr-status` - if it completes without permission prompts, you're configured correctly.

## Notes

- Permissions use glob patterns (`*`) to match any arguments
- Read-only operations (get, list, search) are generally safe to allow
- Write operations (create, update) you may want in `ask` instead of `allow`
