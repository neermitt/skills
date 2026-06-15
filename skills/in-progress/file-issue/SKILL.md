---
name: file-issue
description: >
  Convert session-detected issues into well-structured tickets in whatever issue
  tracker the project uses — GitHub Issues, Jira, Linear, GitLab Issues, or others.
  Use this skill whenever you notice bugs, tech debt, security concerns, or test/docs
  gaps while working on something else — even if the user hasn't asked yet.
  Trigger proactively at task end when out-of-scope issues were spotted, or when
  the user says things like "file those issues", "log what you found", "create a
  ticket for that", "track this in Jira/Linear/GitHub", "let's not forget about X",
  or "raise an issue for this". Works for bugs, tech debt, security concerns, and
  missing tests or documentation.
---

# File Issue

Convert issues spotted during a session into well-structured tickets — clear enough for both a human teammate and an AI agent to act on, in whichever issue tracker the project uses.

## When to offer proactively

While working on the current task, mentally note any out-of-scope issues (bugs, tech debt, security concerns, missing tests/docs). Don't interrupt the flow — but at a natural break or after the main task completes, surface them:

> "While working on this, I noticed a few things that are outside our current scope — want me to file them as tickets so they don't get lost?"

For **security concerns**, don't wait — mention them right away.

---

## Step 1: Detect the issue tracker

Check for signals in this order. Stop at the first clear match.

```bash
# GitHub Issues
ls .github/ 2>/dev/null && gh repo view --json nameWithOwner 2>/dev/null

# GitLab Issues
ls .gitlab/ 2>/dev/null || git remote -v | grep gitlab

# Linear
cat .linear.yml 2>/dev/null || cat linear.config.json 2>/dev/null
grep -i '"linear"' package.json 2>/dev/null

# Jira
cat .jira.yml 2>/dev/null || cat .jira/config.yml 2>/dev/null
grep -iE "JIRA_URL|JIRA_PROJECT" .env 2>/dev/null || env | grep -i jira
```

If you can't auto-detect, ask:
> "Which issue tracker does this project use — GitHub Issues, Jira, Linear, GitLab, or something else?"

Once identified, **read the corresponding reference file** for system-specific commands and metadata concepts:
- GitHub Issues → `references/github.md`
- Jira → `references/jira.md`
- Linear → `references/linear.md`
- GitLab Issues → `references/gitlab.md`

For any other tracker, use the generic workflow in this file and adapt the filing step to the available CLI or API.

---

## Step 2: Surface and confirm the issue list

Present each spotted issue with:
- What's wrong / what's missing
- Where it lives (file, function, rough line)
- Why it matters
- **Type**: AFK (AI agent can fix unattended) or HITL (needs human decision first)

Ask: "Do these all look right, or anything to add or drop?"

---

## Step 3: Analyze grouping and propose a plan

Look for a shared root cause — the same wrong assumption, missing pattern, or systemic gap that explains multiple findings. Two issues with the same root cause are better filed together: the fixer gets full context and the tracker stays clean.

Present your proposal:

> **Option A — 2 tickets (recommended)**
> - Ticket 1: "Missing input validation on user endpoints" (covers `/register` and `/update-profile`)
> - Ticket 2: "N+1 query in order listing"
>
> **Option B — 3 separate tickets**
> - ...
>
> Option A makes sense because the validation gaps share the same root cause and fix. What do you prefer?

The user can always override.

---

## Step 4: Draft tickets for review

Write out each draft in full and show them before filing anything. Keep the language natural — these will be read by people, not just parsed by tools. See **Issue templates** below.

Ask:
- "Does the granularity feel right? (too coarse / too fine)"
- "Should any tickets be merged or split further?"
- "Are the HITL/AFK labels correct?"
- "Anything else to adjust before I file?"

Iterate until the user approves.

---

## Step 5: File the tickets

Refer to the system-specific reference file for exact commands, metadata fields, and how to map concepts like labels/tags, milestones/sprints, and projects/boards.

File in dependency order — blockers first — so you can reference real ticket IDs in the "Blocked by" field of dependent tickets.

After filing, share the ticket URL(s) or IDs so the user can see them immediately.

---

## Issue templates

Use the appropriate template based on issue type. Fill every section — if something genuinely doesn't apply, say "N/A" with a brief note. The "Notes for automated fixes" section is the one place to be precise and technical; the rest should read naturally.

Check whether the tracker has a configured template first (e.g. `.github/ISSUE_TEMPLATE/`, Jira issue type fields, Linear templates). If one exists, prefer it and map these sections into it.

### Bug or defect

```markdown
## Type

AFK / HITL

## Blocked by

- [ticket reference] or "None - can start immediately"

## What's happening

[Clear description of what's broken and how it manifests. Be specific — describe
what you'd observe, not just "it doesn't work".]

## Where it lives

- **File:** `path/to/file.ts`
- **Function / Component:** `functionName()`
- **Lines:** ~L42–L58

## How we found it

Noticed while working on [brief task description] — this is separate from that work
but worth tracking before it causes problems.

## Why it matters

[Impact: who gets affected, how often, what breaks. Even if it's currently minor,
explain what happens if it grows or hits production.]

## Steps to reproduce

1. [Step one]
2. [Step two]
3. Observe: [what you see]
Expected: [what should happen instead]

## Suggested fix

[Optional: rough approach or pointer to where the fix should go.]

## Acceptance criteria

- [ ] [Specific, testable thing that should be true when this is fixed]
- [ ] [Another criterion]
- [ ] Existing tests still pass

## Notes for automated fixes

[Technical context: exact error messages, relevant config values, related files,
API contracts — anything that helps an AI agent act on this without manual investigation.]
```

### Tech debt

```markdown
## Type

AFK / HITL

## Blocked by

- [ticket reference] or "None - can start immediately"

## What's the situation

[Describe the current state of the code and why it's getting in the way — slow to
change, hard to understand, duplicated logic, etc.]

## Where it lives

- **File(s):** `path/to/file.ts`, `path/to/other.ts`
- **Relevant sections:** [function names, class names, or rough line ranges]

## How we found it

Came up while working on [task] — had to navigate around this or noticed it would
complicate future changes.

## What good looks like

[Describe the target state specifically. What becomes easier once this is done?]

## Why now matters

[Cost of leaving it: slows feature work? Confuses new contributors? Risk of bugs?]

## Suggested approach

[How you'd tackle it — rough steps, patterns to introduce, code to delete.]

## Acceptance criteria

- [ ] [Specific measurable outcome]
- [ ] No behavior changes (unless explicitly intended)
- [ ] Tests updated to reflect refactored structure

## Notes for automated fixes

[Technical specifics that help an AI agent understand the refactor without
reverse-engineering intent from the code.]
```

### Security concern

```markdown
## Type

HITL (security issues require human review before acting)

## Blocked by

- [ticket reference] or "None - can start immediately"

## Summary

[One-sentence description of the concern. Avoid exploitation details in public
repos — describe the type of issue instead.]

## Where it lives

- **File:** `path/to/file.ts`
- **Function / Route:** `functionName()` or `POST /api/endpoint`
- **Lines:** ~L42–L58

## How we found it

Spotted while working on [task]. Flagging it here so it gets proper attention.

## What could go wrong

[Describe the risk proportionately — a minor input validation gap is different from
an auth bypass.]

## Suggested fix

[Recommended remediation. Link to OWASP or relevant guidance if helpful.]

## Acceptance criteria

- [ ] The vulnerability is closed
- [ ] A regression test covers this case (where appropriate)
- [ ] No new attack surface introduced by the fix

## Notes for automated fixes

[Input sources, trust boundaries, relevant framework security features, etc.]
```

### Missing tests or documentation

```markdown
## Type

AFK / HITL

## Blocked by

- [ticket reference] or "None - can start immediately"

## What's missing

[Describe the gap: what's not tested, what's not documented, and where.]

## Where it lives

- **File(s):** `path/to/file.ts`
- **Function / Component:** `functionName()`

## Why it matters

[What risk does the gap create? For tests: what regression could ship undetected?
For docs: what question does the missing content leave unanswered?]

## How we found it

Came up while working on [task] — [brief explanation of how the gap became apparent].

## What's needed

[Specific enough that someone could act on this without follow-up questions.]

## Acceptance criteria

- [ ] [Specific test case or doc section that should exist]
- [ ] [Another criterion]

## Notes for automated fixes

[For tests: scenarios to cover, edge cases, expected behavior.
For docs: audience, key questions to answer, format that fits existing docs.]
```

---

## Grouped ticket (multiple findings, one root cause)

```markdown
## Type

AFK / HITL

## Blocked by

- [ticket reference] or "None - can start immediately"

## Overview

[Explain the shared root cause. What's the underlying pattern or missing piece that
explains all of these findings?]

## Findings

### Finding 1: [Short title]
- **Where:** `path/to/file.ts` ~L42
- **What:** [Brief description]

### Finding 2: [Short title]
- **Where:** `path/to/other.ts` ~L88
- **What:** [Brief description]

## Why they're related

[Connect the dots — same missing abstraction, same wrong assumption, same systemic gap.]

## Suggested fix

[Unified approach, or separate steps if needed.]

## Acceptance criteria

- [ ] Finding 1 resolved
- [ ] Finding 2 resolved
- [ ] Tests cover the fixed behavior

## Notes for automated fixes

[Combined technical context for all findings.]
```

---

## Tone guidelines

Write like you're leaving a note for a teammate, not filling out a form.

- "What's happening" not "Description of defect"
- "Why it matters" not "Business impact"
- Be direct about severity — if something is risky, say so. If it's minor, say that too.
- The "Notes for automated fixes" section is the only place to be extra precise and technical.
