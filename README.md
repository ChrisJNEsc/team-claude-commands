# Team Claude Commands

Shared Claude Code slash commands for the team. These commands are designed to work with [Claude Code](https://claude.com/claude-code).

## Installation

### Option 1: Fresh Setup (No existing commands)

If you don't have a `.claude/commands/` directory yet:

```bash
cd ~
mkdir -p .claude
git clone https://github.com/ChrisJNEsc/team-claude-commands.git .claude/commands
```

### Option 2: Existing Commands Directory (Recommended)

If you already have commands in `.claude/commands/`, use a subdirectory approach:

```bash
cd ~/.claude/commands/
git clone https://github.com/ChrisJNEsc/team-claude-commands.git team
```

Your commands will be available as `/team/bulk-pull`, `/team/devtools`, etc.

### Option 3: Git Submodule (Most Maintainable)

If your `.claude` directory is already a git repository:

```bash
cd ~/.claude
git submodule add https://github.com/ChrisJNEsc/team-claude-commands.git commands
git submodule update --init --recursive
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/bulk-pull` | Bulk update all repositories with git pull |
| `/devtools` | Dev Tools Doctor (Requires .har) |
| `/escalate` | Comprehensive escalations investigation with cascading searches and automated Linear ticket creation |
| `/hscheck` | Hubspot Ticket Counter via Linear |
| `/investigateline` | Create Linear ticket with duplicate check, code investigation (FE+BE), fix plan, and optional implementation+local testing |
| `/lindone` | Validate Linear issue recommendations against branch commits and apply status labels |
| `/newreq` | Create Linear ticket without code investigation |
| `/similar-issues` | Find similar issues in Linear |
| `/triage` | Test Command |
| `/pr-status` | Show status of all my PRs grouped by status with linked Linear issues |

## Shared Resources

The `commands/shared/` folder contains lookup files loaded on-demand (Law 3):

| File | Purpose |
|------|---------|
| `team-mapping.md` | Feature → Team ownership lookup |
| `repo-mapping.md` | Feature → Repository + path hints for fast code investigation |
| [PERMISSIONS.md](PERMISSIONS.md) | Pre-approved permissions so commands run without confirmation prompts |

## Updating Commands

To pull the latest commands:

```bash
cd ~/.claude/commands/
git pull origin main
```

Or if using the subdirectory approach:
```bash
cd ~/.claude/commands/team
git pull origin main
```

## Contributing New Commands

1. Create your command as a `.md` file in the `commands/` directory
2. Test it locally in your Claude Code environment
3. Submit a pull request with:
   - The command file
   - A description of what it does
   - Any requirements or dependencies

## Command Format

Commands should be markdown files (`.md`) with clear instructions for Claude. Example:

```markdown
# Command Name

Brief description of what this command does.

## Instructions

Detailed instructions for Claude to follow...
```

## Token Efficiency Principles
  - The 3 Laws:
  1. Minimize round trips → Batch questions, parallel tool calls
    - Bad: 10 sequential questions = 10 user waits + 10 AI responses
    - Good: 1 question with 10 fields = 1 interaction
  2. Be specific, not verbose → Examples > explanations
  3. Context on demand → Don’t front-load. Use tools when needed.
    - Bad: 300-line team mapping upfront (AI reads every token every time)
    - Best: Separate tool/file that AI calls only when needed

     
## Permissions Setup

By default, Claude Code asks for confirmation before running certain tools (GitHub CLI, Linear API, etc.). Adding permissions to your settings file lets commands run without these interruptions.

**Quick setup** - add to your `~/.claude/settings.json` under `permissions.allow`:

```json
"Bash(gh pr list:*)",
"Bash(gh search prs:*)",
"Bash(gh api:*)",
"Bash(gh repo list:*)",
"mcp__plugin_engineering_linear__get_*",
"mcp__plugin_engineering_linear__list_*",
"mcp__plugin_engineering_linear__search_*"
```

See [PERMISSIONS.md](PERMISSIONS.md) for the full list including write operations (create/update). Some command files include a `permissions` frontmatter field listing their specific requirements.

## Troubleshooting

**Commands not showing up?**
- Restart Claude Code after adding new commands
- Verify the `.md` files are in the correct directory
- Check file permissions (should be readable)

**Path issues?**
- Commands must be in `~/.claude/commands/` or a subdirectory
- Use `/` prefix when calling commands: `/commandname`

## License

[Choose your license - MIT, Apache 2.0, etc.]



