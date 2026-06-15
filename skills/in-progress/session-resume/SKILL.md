---
name: session-resume
description: >
  Resume work from a saved handover document. Lists available handovers in
  .handovers/, lets the user pick one (or auto-selects if only one is active),
  loads the context, and orients the agent to continue the work. Use when the user says
  "resume", "pick up where we left off", "load handover", "continue last session",
  "what was I working on", or starts a new session in a project that has handover files.
  Companion skills: session-handover (create one), session-cleanup (mark done when finished).
argument-hint: "Which handover to resume? (leave blank to list all)"
---

# Session Resume

Load a saved handover and orient the agent to continue the work. After resuming,
offer to run `session-cleanup` when the task is complete.

## Step 1: Find available handovers

```bash
ls -t .handovers/*.md 2>/dev/null
```

If the directory doesn't exist or is empty:
> "No handovers found in `.handovers/`. Use `session-handover` to create one."
Stop here.

## Step 2: Filter and present

Read the frontmatter of each file (just the `---` block — don't load full bodies yet).
Show only `status: active` handovers. If the user passed an argument, filter by branch name
or focus field matching the argument.

Present as a numbered list:

```
Available handovers:

1. feat/auth-flow — 2026-06-15 14:30 — "Wire up JWT refresh + fix token expiry"
2. fix/payment-race — 2026-06-14 09:15 — "Investigate race condition in checkout"
```

If only one active handover exists, skip the list and load it directly with a note:
> "One active handover found — loading `feat/auth-flow` (2026-06-15 14:30)."

If none are active (all completed), mention this and offer to show completed ones.

## Step 3: Load selected handover

Read the full body of the chosen file. Summarize the key context to the user:

- What was being worked on
- What's done vs. remaining
- Worktree path / branch to switch to (if applicable)
- Any blockers or decisions from the handover

Then confirm the starting point:
> "Ready to pick up from: `<first remaining task>`. Shall I start there?"

If the handover references a worktree path, remind the user:
> "This work is in worktree `<path>` on branch `<branch>`. Make sure you're working there."

## Step 4: On task completion — offer cleanup

When the remaining tasks from the handover are done (or the user says "we're done",
"that's finished", "close this out"), prompt:

> "Work looks complete. Want me to mark this handover as done and clean up?
> I'll call `session-cleanup` to archive it."

Don't call `session-cleanup` without confirmation.
