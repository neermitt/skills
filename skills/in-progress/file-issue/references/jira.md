# Jira — Filing Reference

## Gather context

```bash
# Check for local Jira config
cat .jira.yml 2>/dev/null || cat .jira/config.yml 2>/dev/null

# Environment-based config
env | grep -iE "JIRA_URL|JIRA_PROJECT|JIRA_TOKEN"

# If jira-cli is installed (go-jira or similar)
jira project list 2>/dev/null
jira issue types 2>/dev/null

# Current branch — useful for linking context
git branch --show-current
```

Ask the user if key values are missing:
- **Project key** (e.g. `PROJ`, `ENG`, `INFRA`)
- **Issue type** (Bug, Task, Story, Improvement — depends on project config)
- **Jira base URL** if not in env
- **Sprint or fix version** (optional)

## Issue types

Map issue type to the closest Jira type available in the project:

| Issue type | Jira issue type |
|---|---|
| Bug / defect | `Bug` |
| Tech debt / refactor | `Task` or `Improvement` |
| Security concern | `Bug` (with `security` label) or `Task` |
| Missing tests | `Task` |
| Missing docs | `Task` |

Confirm available issue types for the project before filing — they vary by Jira configuration.

## Labels and components

- Use Jira labels for cross-cutting concerns: `tech-debt`, `security`, `needs-tests`, `documentation`
- Use **components** if the project has them configured — they're more structured than labels
- Use **priority** field (Highest / High / Medium / Low / Lowest)

## File the issue

### Using jira-cli (go-jira)

```bash
jira issue create \
  --project PROJ \
  --issuetype Bug \
  --summary "Short description of the problem" \
  --description "$(cat issue-body.md)" \
  --label "tech-debt" \
  [--priority High] \
  [--component "API"] \
  [--fixVersion "v2.0"]
```

### Using curl against the REST API

```bash
curl -s -u "$JIRA_USER:$JIRA_TOKEN" \
  -X POST "$JIRA_URL/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": { "key": "PROJ" },
      "issuetype": { "name": "Bug" },
      "summary": "Short description of the problem",
      "description": {
        "type": "doc",
        "version": 1,
        "content": [{
          "type": "paragraph",
          "content": [{ "type": "text", "text": "Issue body here..." }]
        }]
      },
      "labels": ["tech-debt"],
      "priority": { "name": "High" }
    }
  }'
```

Note: Jira Cloud description uses Atlassian Document Format (ADF), not Markdown. Convert Markdown to ADF when using the API directly.

## After filing

Share the issue key and URL: `https://{org}.atlassian.net/browse/{PROJECT-123}`

## Concept mapping

| Generic concept | Jira equivalent |
|---|---|
| Ticket / issue | Issue |
| Label / tag | Label |
| Milestone | Fix Version |
| Board / project | Project + Board |
| Epic | Epic (issue type) |
| Sprint | Sprint (active iteration in the board) |
| Status | Workflow status (To Do / In Progress / Done) |
