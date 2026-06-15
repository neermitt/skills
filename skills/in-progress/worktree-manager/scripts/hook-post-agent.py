#!/usr/bin/env python3
"""
Claude Code PostToolUse hook for the Agent tool.

Prunes stale worktree refs after any agent finishes.
Advisory only — never blocks.
"""
import subprocess
import sys

subprocess.run(["git", "worktree", "prune"], capture_output=True)
sys.exit(0)
