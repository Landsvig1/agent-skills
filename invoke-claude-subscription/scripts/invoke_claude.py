#!/usr/bin/env python3
"""
Shell out to the Claude Code CLI, billing against a Claude Pro/Max
subscription (via CLAUDE_CODE_OAUTH_TOKEN) instead of metered API tokens.

Usable as a library (import invoke_claude) or standalone:
    python invoke_claude.py "Fix the failing test in src/auth.py" --cwd /path/to/repo
"""
import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass


class SubscriptionAuthError(RuntimeError):
    """Raised when the environment would silently fall back to API-key billing."""


@dataclass
class ClaudeResult:
    success: bool
    result: str | None
    cost_usd: float | None
    session_id: str | None
    error: str | None
    raw: dict | None


def invoke_claude(
    prompt: str,
    cwd: str | None = None,
    allowed_tools: list[str] | None = None,
    resume_session_id: str | None = None,
    timeout: int = 600,
    claude_bin: str = "claude",
    model: str | None = None,
) -> ClaudeResult:
    """
    Run a single Claude Code turn and return the parsed result.

    Raises SubscriptionAuthError up front if ANTHROPIC_API_KEY is set --
    that env var silently overrides subscription billing with metered API
    billing, which defeats the entire point of this script existing.
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        raise SubscriptionAuthError(
            "ANTHROPIC_API_KEY is set in this environment. That takes priority "
            "over CLAUDE_CODE_OAUTH_TOKEN and will bill the API, not the "
            "subscription. Unset it before calling invoke_claude()."
        )

    cmd = [claude_bin, "-p", "--dangerously-skip-permissions", "--output-format", "json"]
    if allowed_tools:
        # --allowedTools takes a variadic list (<tools...>) and will greedily
        # swallow the next argv token(s) -- including the prompt -- if passed
        # as two separate list elements. The `=` form binds the value to the
        # flag unambiguously regardless of what follows.
        cmd.append(f"--allowedTools={','.join(allowed_tools)}")
    if resume_session_id:
        cmd += ["--resume", resume_session_id]
    if model:
        # Same greedy-parsing caution as --allowedTools: bind with `=`.
        cmd.append(f"--model={model}")
    cmd.append(prompt)

    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return ClaudeResult(False, None, None, None, f"timed out after {timeout}s", None)
    except FileNotFoundError:
        return ClaudeResult(
            False, None, None, None,
            f"'{claude_bin}' not found on PATH -- is Claude Code installed?", None,
        )

    if proc.returncode != 0:
        return ClaudeResult(False, None, None, None, proc.stderr.strip() or proc.stdout.strip(), None)

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return ClaudeResult(False, None, None, None, f"non-JSON output: {proc.stdout[:500]}", None)

    if data.get("is_error"):
        return ClaudeResult(False, None, data.get("total_cost_usd"), data.get("session_id"),
                             data.get("result") or "unknown error", data)

    return ClaudeResult(
        success=True,
        result=data.get("result"),
        cost_usd=data.get("total_cost_usd"),
        session_id=data.get("session_id"),
        error=None,
        raw=data,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="The task to hand to Claude Code")
    parser.add_argument("--cwd", default=None, help="Working directory for the task")
    parser.add_argument("--allowed-tools", default=None,
                         help="Comma-separated tool allowlist, e.g. 'Bash,Read,Edit'")
    parser.add_argument("--resume", default=None, help="Session ID to resume a prior conversation")
    parser.add_argument("--model", default=None,
                        help="Claude model alias or id (e.g. fable, claude-fable-5); omit for CLI default")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    allowed = args.allowed_tools.split(",") if args.allowed_tools else None
    try:
        result = invoke_claude(
            args.prompt, cwd=args.cwd, allowed_tools=allowed,
            resume_session_id=args.resume, timeout=args.timeout,
            model=args.model,
        )
    except SubscriptionAuthError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    if not result.success:
        print(f"ERROR: {result.error}", file=sys.stderr)
        sys.exit(1)

    print(result.result)
    print(f"\n[session_id={result.session_id} cost_usd={result.cost_usd}]", file=sys.stderr)


if __name__ == "__main__":
    main()
