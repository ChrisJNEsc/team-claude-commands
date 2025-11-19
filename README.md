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

Your commands will be available as `/team/bulk-fetch`, `/team/devtools`, etc.

### Option 3: Git Submodule (Most Maintainable)

If your `.claude` directory is already a git repository:

```bash
cd ~/.claude
git submodule add https://github.com/ChrisJNEsc/team-claude-commands.git commands
git submodule update --init --recursive
```

## Available Commands

- `/bulk-fetch` - Bulk fetch operations
- `/devtools` - Development tools helper
- `/hscheck` - Health and safety check
- `/investigateline` - Investigate specific code lines
- `/newreq` - Create new requirement
- `/similar-issues` - Find similar issues
- `/triage` - Issue triage helper

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
