---
name: session-handover
description: >
  Create or update a handover document so a new agent can continue this session's work.
  Saves to .handovers/ in the project root. Use when the user says "handover to
  new agent", "create a handover", "summarize for next agent", "context dump", "pass
  context to new agent", "let's hand this off", or is ending a session and wants to
  continue in a fresh one. Also trigger proactively when the session has been long and
  significant work remains. Companion skills: session-resume (pick up a handover),
  session-cleanup (archive completed ones).
argument-hint: "What should the next session focus on?"
---

# Session Handover

Create a compact handover document under `.handovers/` so a new agent can resume
this session's work without re-reading the entire conversation.

Point at artifacts — don't duplicate them. The next agent can read commits, issues, diffs,
and docs directly. Capture only what can't be derived from those.

## File naming

```
.handovers/<YYYYMMDD-HHMM>-<branch-slug>.md
```

Example: `.handovers/20260615-1430-feat-auth-flow.md`

Use the current branch name, slugified (replace `/` and non-alphanumeric with `-`).
If not in a git repo, use a short description slug from the session topic.

The file uses YAML frontmatter so `session-resume` and `session-cleanup` can filter
and display handovers without reading the full body:

```yaml
---
branch: feature/auth-flow
worktree: /path/to/worktree        # omit if main working tree
main-repo: /path/to/main-repo      # omit if main working tree
created: 2026-06-15T14:30:00
status: active                     # active | completed
focus: "<user-provided focus or one-line summary>"
---
```

## Step 1: Check for existing handover on this branch

```bash
ls .handovers/ 2>/dev/null | grep "<branch-slug>"
```

If one exists: ask whether to **update** it (overwrite) or **create a new one** (both kept).
Default to update — avoids accumulating stale files.

## Step 2: Gather artifact references

Run these; don't ask the user:

```bash
git branch --show-current
git worktree list
git log --oneline -10
git status --short
git diff --stat
git stash list
```

If `git worktree list` shows multiple entries, capture the current worktree path and the
main repo path — the next agent needs to `cd` to the right place.

For issues and PRs: extract any IDs or URLs mentioned in the conversation, commit messages,
or the branch name (e.g. `feat/GH-42-auth` → #42).

## Step 3: Scrub sensitive data

Before writing, scan everything you're including for:

- API keys / tokens: `sk-`, `Bearer `, `ghp_`, `xoxb-`, `AIza`, env vars with `KEY`,
  `SECRET`, `TOKEN`, `PASSWORD`, `CREDENTIAL` in the name
- Connection strings with embedded credentials: `postgres://user:pass@`, `mysql://`, `mongodb+srv://`
- Personal email addresses appearing as data (not code references like `user@example.com`)

Replace with `[REDACTED: <type>]`. If anything was redacted, add at the top of the document:

> ⚠ Sensitive values redacted: `api_key` (line 12). Obtain from team vault / env before continuing.

## Step 4: Write the document

```markdown
# Session Handover

> Branch: `<branch>` | Created: <datetime> | Focus: <focus>

<!-- ⚠ Sensitive values redacted: ... -->  <!-- only if applicable -->

## What we were working on

<1–3 sentences: goal of the session and relevant background>

## Completed this session

- [x] <task> — commit `<hash>`
- [x] <task> — issue <ref> / PR <ref>

## Remaining tasks

- [ ] <task> — <where things stand, any blockers>
  - Refs: `<file path>`, issue <ref>
- [ ] <task> — blocked by <ref or task above>

## Artifacts

| | |
|---|---|
| Branch | `<branch>` |
| Worktree | `<path>` _(omit if main working tree)_ |
| Main repo | `<path>` _(omit if main working tree)_ |
| Recent commits | `git log --oneline <base>..<HEAD>` |
| Files in flight | `<path>`, `<path>` |
| Issues / PRs | <refs> |
| Key docs | <paths or URLs> |

## Decisions & context

<Key choices made this session not captured in commits or issue comments.>
<Non-obvious gotchas: env quirks, flaky tests, deprecated APIs still in use.>

## Suggested next steps for the agent

<Tools, skills, or workflows the next agent should invoke — e.g. run a specific test suite,
file spotted bugs as issues, or call session-cleanup when the work is done.>

## Next agent instructions

<User-provided focus from args. If none given, write the single most important next step.>
```

Omit any section that has nothing to say rather than leaving it empty.

## Step 5: Confirm with user

Print the document path and ask:
> "Handover saved to `.handovers/<filename>`. Does this look right, or anything to adjust?"

Don't save without confirmation if the user is actively reviewing the draft.
