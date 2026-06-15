# Linear — Filing Reference

## Gather context

```bash
# Check for local Linear config
cat .linear.yml 2>/dev/null || cat linear.config.json 2>/dev/null
grep -i '"linear"' package.json 2>/dev/null

# Linear CLI (if installed)
linear team list 2>/dev/null
linear label list 2>/dev/null

# Current branch — useful for linking context
git branch --show-current
```

Ask the user if key values are missing:
- **Team** (e.g. `Engineering`, `Backend`, `Platform`)
- **Project** (optional — only if they want it tracked in a specific project)
- **Cycle / sprint** (optional)

## Labels

Linear labels are workspace-level. Common ones to use:

| Issue type | Linear label |
|---|---|
| Bug / defect | `Bug` |
| Tech debt / refactor | `Tech Debt` or `Improvement` |
| Security concern | `Security` or `Bug` |
| Missing tests | `Testing` |
| Missing docs | `Documentation` |

If a label doesn't exist, Linear lets you create them per workspace. Only suggest creating new labels if the user confirms.

## Priority

Linear uses numeric priority:
- `0` — No priority
- `1` — Urgent
- `2` — High
- `3` — Medium
- `4` — Low

## File the issue

### Using Linear CLI

```bash
linear issue create \
  --title "Short description of the problem" \
  --description "$(cat issue-body.md)" \
  --team "Engineering" \
  --label "Bug" \
  [--priority 2] \
  [--project "Q3 Cleanup"] \
  [--cycle "Current"]
```

### Using Linear API (GraphQL)

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier url } } }",
    "variables": {
      "input": {
        "title": "Short description of the problem",
        "description": "Issue body in Markdown...",
        "teamId": "TEAM_ID",
        "labelIds": ["LABEL_ID"],
        "priority": 2
      }
    }
  }'
```

Linear description supports Markdown natively — no conversion needed.

## After filing

Share the issue identifier and URL: `https://linear.app/{org}/issue/{TEAM-123}`

## Concept mapping

| Generic concept | Linear equivalent |
|---|---|
| Ticket / issue | Issue |
| Label / tag | Label |
| Milestone | Project or Cycle |
| Board / project | Project |
| Epic | Project (or parent issue) |
| Sprint | Cycle |
| Status | Issue state (Backlog / Todo / In Progress / Done / Cancelled) |
