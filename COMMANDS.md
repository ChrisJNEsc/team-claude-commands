# Command Reference

Detailed documentation for all available commands.

## /bulk-pull

**Purpose:** Bulk update all git repositories in a directory

**Usage:** `/bulk-pull`

**Description:** Runs `git pull` on all repositories in `/Users/chrisberry/Documents/GitHub`. Provides status updates and a summary of successful/failed pulls.

**Use Cases:**
- Keep all local repositories up to date
- Pull latest changes across multiple projects
- Batch operations before starting work

---

## /devtools

**Purpose:** Deep file analysis and comprehension

**Usage:** `/devtools [file-path]`

**Description:** Specialized tool for thoroughly analyzing files. Identifies file types, data structures, patterns, and provides comprehensive insights about the file's purpose and functionality.

**Use Cases:**
- Understanding unfamiliar codebases
- Analyzing data structures
- Identifying issues or inconsistencies
- Getting comprehensive file summaries

---

## /hscheck

**Purpose:** Health and safety check

**Usage:** `/hscheck`

**Description:** [Add description based on your team's use case]

---

## /investigateline

**Purpose:** Create Linear tickets for customer-reported bugs with optional code investigation

**Usage:** `/investigateline`

**Description:** Comprehensive workflow for creating customer bug reports in Linear. Checks for duplicate issues, gathers detailed reproduction steps and customer information, optionally investigates related code and creates fix plans, then creates a properly formatted Linear ticket with the "Bug - Customer Reported" label in Triage state.

**Use Cases:**
- Creating customer-reported bug tickets
- Investigating code related to customer issues
- Generating fix plans for bugs
- Ensuring consistent bug report formatting
- Avoiding duplicate issue creation

---

## /newreq

**Purpose:** Create new requirement

**Usage:** `/newreq`

**Description:** Structured workflow for creating and documenting new requirements.

**Use Cases:**
- Feature planning
- Requirement documentation
- Specification creation

---

## /similar-issues

**Purpose:** Find similar issues

**Usage:** `/similar-issues`

**Description:** Searches for and identifies similar issues across the codebase or issue tracker.

**Use Cases:**
- Avoiding duplicate work
- Finding related bugs
- Pattern identification

---

## /triage

**Purpose:** Error and issue triage helper

**Usage:** `/triage`

**Description:** Structured workflow for triaging errors and issues. Reviews error messages, identifies root causes, summarizes impact, and suggests testing strategies.

**Use Cases:**
- Bug investigation
- Error analysis
- Incident response
- Testing strategy development

---

## Contributing

To add a new command:
1. Create a `.md` file in `commands/` directory
2. Follow the command format guidelines in README.md
3. Add documentation to this file
4. Test thoroughly before submitting PR
