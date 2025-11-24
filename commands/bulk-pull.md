# Bulk Update All Repositories

Check if a saved GitHub directory path exists in `~/.claude/bulk-pull-config.json`.

If the config file does NOT exist or does NOT contain a `github_dir` field:
1. Ask the user: "Where is your GitHub repositories directory? (e.g., ~/Documents/GitHub)"
2. Wait for the user to provide the directory path
3. Save the path to `~/.claude/bulk-pull-config.json` in this format: `{"github_dir": "/full/path/to/github"}`
4. Expand any `~` to the full home directory path before saving

If the config file exists and contains a `github_dir` field:
1. Read the saved directory path from the config file
2. Use this directory for the bulk pull operation

Then, run `git pull` on all repositories in the configured directory.

For each repository:
1. Navigate to the repository directory
2. Run `git pull` to fetch and merge the latest changes from the remote
3. Display success or failure status
4. Show a summary at the end with total, successful, and failed updates

Run the pull operations in the background and provide status updates as repositories are processed.
