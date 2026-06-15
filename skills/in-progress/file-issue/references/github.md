# GitHub Issues — Filing Reference

## Gather context

```bash
# Repo identity
gh repo view --json nameWithOwner,defaultBranchRef,description

# Existing labels
gh label list --limit 100

# Issue templates
ls .github/ISSUE_TEMPLATE/ 2>/dev/null
cat .github/ISSUE_TEMPLATE.md 2>/dev/null

# Milestones (optional)
gh api repos/{owner}/{repo}/milestones

# Projects (optional)
gh project list
```

## Templates

If `.github/ISSUE_TEMPLATE/` exists, pick the closest matching template by issue type and respect all its front-matter fields (labels, assignees, title prefix). Otherwise use the default templates from SKILL.md.

## Labels

GitHub labels are free-form strings. Map issue types to these standard labels:

| Issue type | Labels |
|---|---|
| Bug | `bug` |
| Tech debt | `tech-debt` or `refactor` |
| Security | `security` |
| Missing tests | `needs-tests` |
| Missing docs | `documentation` |

Add priority labels if the repo uses them: `priority: high`, `priority: medium`, `priority: low`.

If a standard label doesn't exist yet, offer to create it:
```bash
gh label create "tech-debt" --color "#e4e669" --description "Technical debt and refactoring"
```
Only create labels the user confirms.

## File the issue

```bash
gh issue create \
  --title "bug: short description of the problem" \
  --body "$(cat issue-body.md)" \
  --label "bug,priority: high" \
  [--milestone "v2.0"] \
  [--project "Backlog"] \
  [--assignee "@me"]
```

- Use a conventional prefix in the title: `bug:`, `refactor:`, `security:`, `docs:`, `test:`
- Pass the body via a temp file or heredoc to preserve formatting
- Milestones and projects are optional — only add if the user asks

## After filing

Share the issue URL directly: `https://github.com/{owner}/{repo}/issues/{number}`

## Concept mapping

| Generic concept | GitHub equivalent |
|---|---|
| Ticket / issue | Issue |
| Label / tag | Label |
| Milestone | Milestone |
| Board / project | GitHub Project |
| Epic | — (use label or milestone) |
| Sprint | — (use iteration in Projects v2) |
