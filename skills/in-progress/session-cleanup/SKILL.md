---
name: session-cleanup
description: >
  Archive or delete completed handover documents from .handovers/. Use when the
  user says "clean up handovers", "mark this done", "close out the handover", "archive
  the session", "we're finished", or after session-resume detects the work is complete.
  Also use when session-handover is about to create a new handover for the same branch
  and the old one should be removed first. Companion skills: session-handover (create),
  session-resume (pick up work).
argument-hint: "Which handover to clean up? (leave blank to list all completed)"
---

# Session Cleanup

Archive or remove handover files once the work is done. Keeps `.handovers/`
from accumulating stale context.

## Two modes

### A. Mark complete (called from session-resume after finishing work)

Update the handover file's frontmatter in place:

```yaml
status: completed
completed: 2026-06-15T16:45:00
```

This preserves the record without deleting it. The file is excluded from future
`session-resume` listings (which filter on `status: active`).

### B. Explicit cleanup (user asks to clean up / purge)

List all handovers with their status and age:

```
Handovers in .handovers/:

  ACTIVE
  1. feat/auth-flow — 2026-06-15 — "Wire up JWT refresh"

  COMPLETED
  2. fix/payment-race — 2026-06-14 — "Race condition in checkout" ✓
  3. chore/deps-update — 2026-06-10 — "Bump all dependencies" ✓
```

Ask:
> "Delete all completed handovers? Or pick specific ones? (or 'keep all')"

Delete only what the user confirms. Never delete `status: active` handovers without
explicit confirmation — active ones may still be needed.

## When called from session-handover (branch collision)

If `session-handover` detects an existing active handover for the same branch, it
delegates here. Present:

> "An active handover already exists for `feat/auth-flow` (2026-06-15 14:30).
> Update it in place, or archive it and create a fresh one?"

- **Update in place**: overwrite the existing file (default)
- **Archive and create fresh**: mark old one `completed`, create new file with new timestamp

## Safety rules

- Never auto-delete without confirmation.
- Never touch files outside `.handovers/`.
- If the directory is empty after cleanup, leave it in place (don't remove it).
