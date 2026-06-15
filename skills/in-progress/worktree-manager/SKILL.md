---
name: worktree-manager
description: >
  Manage git worktrees using a consistent path convention: worktrees for a repo
  live at <repo-parent>/<repo-name>.worktrees/<worktree-name>. Use this skill whenever
  the user wants to create, list, switch to, or remove a worktree; when parallel work
  needs isolation without stashing; when spawning agents that should run in isolated
  worktrees; or when the user says things like "create a worktree", "spin up a worktree
  for this branch", "work on X in a worktree", "clean up worktrees", or "run this agent
  in a worktree". Also use proactively when a task involves file-mutating parallel agents
  that would conflict if run in the same working tree.
argument-hint: "Worktree name or branch (leave blank to list existing worktrees)"
---

# Worktree Manager

Manage git worktrees with a stable path convention that keeps worktrees out of the
repo directory but close enough to find easily.

## Path convention

Given a repo at `/path/to/org/repo`:

```
/path/to/org/
├── repo/                          ← main working tree
└── repo.worktrees/
    ├── feat-auth/                 ← worktree for feat/auth branch
    ├── fix-payments/              ← worktree for fix/payments branch
    └── experiment-xyz/            ← worktree for experiment/xyz branch
```

Compute paths:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")
WORKTREES_DIR="$(dirname "$REPO_ROOT")/${REPO_NAME}.worktrees"
WORKTREE_PATH="${WORKTREES_DIR}/<worktree-name>"
```

Use the worktree name as the directory name. When the worktree name maps to a branch
with slashes (e.g., `feat/auth-flow`), use a slug with hyphens for the directory name
(`feat-auth-flow`) but track the real branch inside.

## Operations

### List worktrees

```bash
git worktree list
```

Show the user: path, branch, HEAD commit. Highlight which one is the main working tree.

### Create a worktree

```bash
git worktree add "$WORKTREE_PATH" [<branch>]
```

If `<branch>` doesn't exist yet, create it:

```bash
git worktree add -b <branch> "$WORKTREE_PATH" [<base>]
```

Default `<base>` to the current branch unless the user specifies otherwise.

After creation, print the full path so the user can `cd` to it or open it in their editor.

### Remove a worktree

```bash
git worktree remove "$WORKTREE_PATH"
```

If the worktree has uncommitted changes, git will refuse. Ask the user before using `--force`.

After removing, prune stale refs:

```bash
git worktree prune
```

### Prune stale worktrees

Run this when worktrees were deleted manually (directory removed without `git worktree remove`):

```bash
git worktree prune --verbose
```

## Agent isolation

When spawning agents that mutate files in parallel, always use convention-path worktrees
rather than the Agent tool's built-in `isolation: "worktree"` parameter. This keeps
all worktrees at predictable paths and avoids the harness creating a second worktree
alongside yours.

### With the hooks installed

If the hooks are configured, you can still write `isolation: "worktree"` in an Agent
call — the pre-hook will intercept it, create the convention-path worktree, block the
call, and tell you to re-spawn without isolation. Follow the instructions in the message.

### Without the hooks (manual flow)

Create the worktree before spawning the agent:

```bash
WORKTREE_PATH=$(python3 scripts/worktree-path.py "<agent-name>")
git worktree add -b "worktree/<agent-name>" "$WORKTREE_PATH" HEAD
```

Spawn the agent without `isolation: "worktree"`, and include in its prompt:

> "Work exclusively inside the directory: `<WORKTREE_PATH>`. Do not modify files outside it."

After the agent finishes, remove the worktree:

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

## Common flows

### Start work on a feature in isolation

1. Derive worktree name from branch: `feat/new-checkout` → `feat-new-checkout`
2. Compute path using convention
3. `git worktree add -b feat/new-checkout <path> main`
4. Print path

### Clean up after a merged branch

1. List worktrees
2. Identify worktrees whose branches are merged or deleted
3. Confirm with user before removing
4. `git worktree remove <path>` for each confirmed
5. `git worktree prune`

### Run parallel agents without conflicts

1. Assess whether agents write to overlapping files
2. If yes → use `isolation: "worktree"` in Agent tool calls, or create explicit worktrees
3. If no → worktree isolation is unnecessary; don't add overhead

## Claude Code hooks

Two hooks automate worktree lifecycle when using the Agent tool with `isolation: "worktree"`.
Set them up in `.claude/settings.json` (project-level) or `~/.claude/settings.json` (global).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Agent",
        "hooks": [
          {
            "type": "command",
            "command": "python3 <skill-path>/scripts/hook-pre-agent.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Agent",
        "hooks": [
          {
            "type": "command",
            "command": "python3 <skill-path>/scripts/hook-post-agent.py"
          }
        ]
      }
    ]
  }
}
```

Replace `<skill-path>` with the absolute path to this skill's directory.

### What the hooks do

**`hook-pre-agent.py`** (PreToolUse):
- Fires before any Agent tool call
- If the agent has `isolation: "worktree"`, **blocks** the call (exit 2) and:
  - Creates a convention-path worktree at `<repo-parent>/<repo-name>.worktrees/<label>-<timestamp>`
  - Creates a branch `worktree/<name>` from HEAD
  - Returns a message telling Claude to re-spawn the agent **without** `isolation: "worktree"`,
    instead passing the worktree path in the agent prompt
- Non-worktree agents: no-op (exit 0)

This ensures exactly one worktree per agent at the convention path. Without the hook,
using `isolation: "worktree"` creates the harness's own temp worktree at an uncontrolled
path — the two would conflict.

**`hook-post-agent.py`** (PostToolUse):
- Fires after every Agent tool call
- Runs `git worktree prune` to clean up any stale refs
- Never force-removes worktrees — cleanup of the convention-path worktree is Claude's
  responsibility (the pre-hook instructs Claude to do this after the agent finishes)

### Setting up hooks via the update-config skill

Instead of editing settings.json manually, invoke the `update-config` skill:

> "Set up worktree hooks — run `hook-pre-agent.py` before Agent tool calls and
> `hook-post-agent.py` after, from path `<skill-path>/scripts/`"

### Path helper script

`scripts/worktree-path.py <name-or-branch>` computes the convention path for any
name without creating the worktree — useful for scripting or dry-runs:

```bash
python3 scripts/worktree-path.py feat/auth-flow
# → /path/to/org/repo.worktrees/feat-auth-flow
```

## Safety rules

- Never `--force` remove a worktree without confirming uncommitted changes with the user.
- Never remove the main working tree.
- Always `git worktree prune` after manual directory deletions.
- When unsure which branch a worktree is on, run `git worktree list` first.
