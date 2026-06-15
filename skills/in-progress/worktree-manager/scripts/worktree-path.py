#!/usr/bin/env python3
"""
Compute the convention-compliant worktree path for a given name or branch.

Usage: worktree-path.py <name-or-branch> [repo-root]

Output: absolute path for the worktree directory
  e.g. /path/to/org/repo.worktrees/feat-auth-flow
"""
import re
import subprocess
import sys
from pathlib import Path


def slugify(name: str) -> str:
    slug = name.replace("/", "-").replace(" ", "-")
    slug = re.sub(r"[^a-zA-Z0-9\-.]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: worktree-path.py <name-or-branch> [repo-root]", file=sys.stderr)
        sys.exit(1)

    name = sys.argv[1]
    if len(sys.argv) >= 3:
        repo_root = Path(sys.argv[2])
    else:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        repo_root = Path(result.stdout.strip())

    repo_name = repo_root.name
    slug = slugify(name)
    worktrees_dir = repo_root.parent / f"{repo_name}.worktrees"
    print(worktrees_dir / slug)


if __name__ == "__main__":
    main()
