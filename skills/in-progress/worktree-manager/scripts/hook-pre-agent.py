#!/usr/bin/env python3
"""
Claude Code PreToolUse hook for the Agent tool.

When an agent is spawned with isolation: "worktree", intercept it:
  1. Create a convention-path worktree
  2. Block the original call (exit 2)
  3. Tell Claude to re-spawn the agent WITHOUT isolation, working in the convention path

Exit 0 → allow the tool call through
Exit 2 → block the call; stdout is returned to Claude as a message
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path


def slugify(name: str) -> str:
    slug = name.replace("/", "-").replace(" ", "-")
    slug = re.sub(r"[^a-zA-Z0-9\-.]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:40]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    if tool_input.get("isolation") != "worktree":
        sys.exit(0)

    # Derive a name from agent description or label
    label = (
        tool_input.get("description")
        or tool_input.get("label")
        or "agent"
    )
    slug = slugify(label)
    timestamp = int(time.time())
    worktree_name = f"{slug}-{timestamp}"

    # Compute convention path
    repo_root = Path(git("rev-parse", "--show-toplevel").stdout.strip())
    repo_name = repo_root.name
    worktrees_dir = repo_root.parent / f"{repo_name}.worktrees"
    worktree_path = worktrees_dir / worktree_name

    worktrees_dir.mkdir(parents=True, exist_ok=True)

    branch = f"worktree/{worktree_name}"
    git("worktree", "add", "-b", branch, str(worktree_path), "HEAD")

    print(
        f"Worktree created at: {worktree_path} (branch: {branch})\n"
        "\n"
        'Do NOT use isolation: "worktree" — the worktree already exists at the path above.\n'
        "Re-spawn the agent WITHOUT the isolation parameter. Instead, include this in the prompt:\n"
        "\n"
        f'  "Work exclusively inside the directory: {worktree_path}\n'
        '   Do not modify files outside of it."\n'
        "\n"
        "When the agent finishes, remove the worktree:\n"
        f"  git worktree remove {worktree_path!s} && git worktree prune"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
