# GitLab Issues — Filing Reference

## Gather context

```bash
# Confirm GitLab remote
git remote -v | grep gitlab

# GitLab CLI (glab)
glab repo view 2>/dev/null
glab label list 2>/dev/null
glab milestone list 2>/dev/null

# Issue templates
ls .gitlab/issue_templates/ 2>/dev/null

# Current branch
git branch --show-current
```

## Templates

If `.gitlab/issue_templates/` exists, pick the closest matching template by issue type. GitLab templates are Markdown files — pass the template name with `--template` or reference it manually. Otherwise use the default templates from SKILL.md.

## Labels

GitLab labels are project-level. Map issue types to these standard labels:

| Issue type | Labels |
|---|---|
| Bug | `bug` or `type::bug` |
| Tech debt | `technical debt` or `type::maintenance` |
| Security | `security` or `~security` |
| Missing tests | `needs tests` |
| Missing docs | `documentation` or `type::documentation` |

GitLab also supports scoped labels (e.g. `priority::high`, `type::bug`) if the project uses them. Check existing labels first with `glab label list`.

## File the issue

### Using glab CLI

```bash
glab issue create \
  --title "Short description of the problem" \
  --description "$(cat issue-body.md)" \
  --label "bug,priority::high" \
  [--milestone "v2.0"] \
  [--assignee "@me"] \
  [--confidential]  # use for security issues
```

### Using GitLab REST API

```bash
curl -s -X POST "$GITLAB_URL/api/v4/projects/$PROJECT_ID/issues" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Short description of the problem",
    "description": "Issue body in Markdown...",
    "labels": "bug,tech-debt",
    "milestone_id": 5,
    "confidential": false
  }'
```

**Security issues**: use `--confidential` (glab) or `"confidential": true` (API) so the issue is only visible to project members.

## After filing

Share the issue URL: `https://gitlab.com/{group}/{project}/-/issues/{number}`

## Concept mapping

| Generic concept | GitLab equivalent |
|---|---|
| Ticket / issue | Issue |
| Label / tag | Label (supports scoped labels with `::`) |
| Milestone | Milestone |
| Board / project | Issue Board |
| Epic | Epic (GitLab Ultimate) |
| Sprint | Iteration |
| Status | Open / Closed (+ label-based workflow) |
