#!/usr/bin/env python3
"""
Task runner for hermes-model-bench: executes ONE (task x arm) real run and
emits a TaskRun-shaped JSON that scoring.py can consume directly.

REAL EXECUTOR, NOT A CHAT CALL. Every arm goes through a genuine coding-agent
CLI (Claude Code or OpenCode) with real filesystem/shell/git tool access --
never a single-shot API completion pretending to "do" the task. This matters
because most of the 6 seed tasks require actually running commands, editing
files, and calling `gh`/`docker`/`pytest` -- a plain chat completion cannot
attempt them at all, and scoring one as if it could would be exactly the
"scripted baseline" trap this project's own methodology explicitly guards
against (see benchmark-design-and-validation skill, Trap 1).

Two agentic CLIs cover all 14 arms:
  - `claude` (Claude Code)  -> Anthropic models (sonnet-5, opus-5, haiku-4.5)
  - `opencode`              -> everything else, via --model provider/slug
    (DeepSeek, GPT, Grok, GLM, Gemini -- all through OpenRouter or direct
    provider keys depending on what's configured)

For split (plan-model / work-model) arms, this script runs TWO passes:
  1. plan pass: the plan model, in a RESTRICTED read-only/no-tools mode,
     produces the structured plan JSON per harness/plan_schema.md.
  2. work pass: the work model executes with the plan handed to it as
     context (steps + risks_flagged only, NEVER the plan model's raw
     reasoning trace -- matches plan_schema.md's stated contract).
Both passes' real usage/cost are captured and summed for that arm's
TaskRun record (plan_model/work_model tracked separately per scoring.py's
existing dict-keyed input_tokens/output_tokens shape).

USAGE:
    python3 run_task.py --task ../tasks/T-INFRA-001-docker-network-relay.md \\
        --arm sonnet-5 --out ../results/runs/T-INFRA-001-sonnet-5.json

    python3 run_task.py --task ../tasks/T-GH-001-review-before-merge.md \\
        --arm sonnet5-plans-flash-works \\
        --out ../results/runs/T-GH-001-sonnet5-plans-flash-works.json

PREREQUISITES (checked at startup, exits with a clear message if missing):
  - `claude auth status` must show loggedIn:true for any arm using Claude
    Code (sonnet-5, opus-5, haiku-4.5, or a split arm with either as
    plan/work model). CONFIRMED WORKING 2026-08-13 via `claude auth login
    --console` (interactive OAuth -- needs a human to visit a URL and paste
    back a code once per machine). Hermes's own ANTHROPIC_API_KEY does NOT
    satisfy this -- it's a separate credential store.
  - REAL BLOCKER as of 2026-08-13: the console/API-billing account this
    logged into (org "gresearch") has $0 credit -- every real call fails
    with "Credit balance is too low". This is a billing gap, not a code
    gap. Fix is either (a) load API credits on that console account, or
    (b) `claude auth login` WITHOUT --console to use an actual claude.ai
    subscription (Pro/Max) instead of pay-per-token API billing. Ken is
    deciding between a $100 Claude Max (5x) subscription vs other options
    -- see docs/pricing.md's note on this. check_prereqs() below probes for
    this exact failure and fails fast with an actionable message rather
    than letting a real scored task burn a slot on it.
  - `opencode auth list` must show a credential for any arm using
    OpenCode. CONFIRMED WORKING 2026-08-13 for DeepSeek: OpenCode reads
    DEEPSEEK_API_KEY directly from the environment, no interactive login
    needed -- `deepseek/deepseek-v4-pro` and `deepseek/deepseek-v4-flash`
    both verified live. OpenRouter-routed arms (gpt-5.6-terra, grok-4.6,
    glm-5.2, gemini-3.6-flash) remain blocked -- no OPENROUTER_API_KEY
    configured anywhere in this profile as of 2026-08-13.
  - Each task's fixture (`## Setup` section) must be materialized BEFORE
    calling this script -- this script does NOT provision fixtures itself
    (see harness/fixtures/<task-id>/ once built; T-VERIFY-001's fixture
    does not exist yet as of 2026-08-13, see docs/methodology.md's open
    question and the TODO at the bottom of this file).

DEDICATED BENCH ENVIRONMENT (2026-08-13): this harness runs on its own
Proxmox LXC (VMID 112, "hermes-bench", pve2, 192.168.1.226, 1GB RAM/2
cores/8GB disk, Debian 13) rather than inside the main hermes-pve2 CT --
deliberately isolated so bench runs (which install arbitrary fixture repos,
dependencies, and run real agentic CLIs) can never touch live production
services, and so results are reproducible from a clean, documented base.
Provisioning steps are recorded in the homelab docs (see
`mkdocs-site/docs/sdlc/hermes-model-bench-lxc-setup.md` in the homelab repo).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# ---- Arm registry --------------------------------------------------------
# Mirrors README.md's arms table. `executor` picks which CLI drives this
# model; `cli_model` is the exact string passed to that CLI's --model flag
# (opencode wants "provider/slug"; claude wants its short alias).
ARMS: dict[str, dict] = {
    "sonnet-5":          {"executor": "claude",   "cli_model": "sonnet"},
    "opus-5":            {"executor": "claude",   "cli_model": "opus"},
    "haiku-4.5":         {"executor": "claude",   "cli_model": "haiku"},
    "deepseek-v4-pro":   {"executor": "opencode", "cli_model": "deepseek/deepseek-v4-pro"},
    "deepseek-v4-flash": {"executor": "opencode", "cli_model": "deepseek/deepseek-v4-flash"},
    "gpt-5.6-terra":     {"executor": "opencode", "cli_model": "openrouter/openai/gpt-5.6-terra"},
    "grok-4.6":          {"executor": "opencode", "cli_model": "openrouter/x-ai/grok-4.6"},
    "glm-5.2":           {"executor": "opencode", "cli_model": "openrouter/z-ai/glm-5.2"},
    "gemini-3.6-flash":  {"executor": "opencode", "cli_model": "openrouter/google/gemini-3.6-flash"},
}

# Split arms: (plan_arm_key, work_arm_key). Both must exist in ARMS above.
SPLIT_ARMS: dict[str, tuple[str, str]] = {
    "sonnet5-plans-flash-works":        ("sonnet-5", "deepseek-v4-flash"),
    "deepseekpro-plans-flash-works":    ("deepseek-v4-pro", "deepseek-v4-flash"),
    "sonnet5-plans-deepseekpro-works":  ("sonnet-5", "deepseek-v4-pro"),
    "opus5-plans-flash-works":          ("opus-5", "deepseek-v4-flash"),
    "haiku-plans-flash-works":          ("haiku-4.5", "deepseek-v4-flash"),
}

# Real pricing table key names must match scoring.py's PRICING_USD_PER_M
# exactly -- kept in sync manually since scoring.py is the scoring
# authority and this file is the execution authority; don't duplicate the
# numbers here, only the model-name keys need to line up.


@dataclass
class ExecResult:
    ok: bool
    input_tokens: int
    output_tokens: int
    cost_usd: float          # real cost as reported by the CLI, informational
    raw_output: str
    error: str = ""


def check_prereqs(arm: str) -> None:
    """Fail fast with an actionable message rather than a confusing mid-run
    crash -- this is exactly the class of gap Trap 11 warns about (never
    silently degrade to an empty/null execution)."""
    plan_arm, work_arm = SPLIT_ARMS.get(arm, (None, arm))
    needed = {a for a in (plan_arm, work_arm) if a}
    for a in needed:
        if a not in ARMS:
            print(f"FATAL: arm '{a}' not in ARMS registry -- add it to run_task.py's ARMS dict first", file=sys.stderr)
            sys.exit(2)
        executor = ARMS[a]["executor"]
        if executor == "claude":
            r = subprocess.run(["claude", "auth", "status"], capture_output=True, text=True, timeout=15)
            try:
                status = json.loads(r.stdout)
            except json.JSONDecodeError:
                status = {}
            if not status.get("loggedIn"):
                print(f"FATAL: Claude Code is not logged in (needed for arm '{a}').\n"
                      f"Fix: run `claude auth login --console` (interactive OAuth, needs a human to "
                      f"visit the URL and paste back the code -- confirmed working 2026-08-13). "
                      f"Hermes's own ANTHROPIC_API_KEY in /root/.hermes/.env is a SEPARATE credential "
                      f"store and does not satisfy this.",
                      file=sys.stderr)
                sys.exit(2)
            # Real gap hit 2026-08-13: login succeeded but landed on an
            # Anthropic CONSOLE/API-billing account with $0 credit balance
            # ("Credit balance is too low"), not a Claude subscription plan.
            # Do a cheap 1-token probe here rather than let a real task burn
            # a slot only to fail on this -- catches it in <1s.
            probe = subprocess.run(
                ["claude", "-p", "hi", "--output-format", "json", "--max-turns", "1"],
                capture_output=True, text=True, timeout=30)
            try:
                probe_data = json.loads(probe.stdout)
            except json.JSONDecodeError:
                probe_data = {}
            if probe_data.get("result") == "Credit balance is too low":
                print(f"FATAL: Claude Code is logged in but the account has $0 credit "
                      f"(needed for arm '{a}'). This is a real billing gap, not an auth bug -- "
                      f"either load credits on the console account, or log in with an actual "
                      f"claude.ai subscription instead (`claude auth login` without --console).",
                      file=sys.stderr)
                sys.exit(2)
        elif executor == "opencode":
            r = subprocess.run(["opencode", "auth", "list"], capture_output=True, text=True, timeout=15)
            if "0 credentials" in r.stdout:
                print(f"FATAL: OpenCode has no configured credentials (needed for arm '{a}').\n"
                      f"Fix: run `opencode auth login` interactively, or export OPENROUTER_API_KEY "
                      f"(or the specific provider key) into this shell's environment before running "
                      f"this script. Confirmed 2026-08-13: hermes status showed NO OpenRouter key set "
                      f"anywhere in this profile -- this is a genuine blocker until Ken adds one.",
                      file=sys.stderr)
                sys.exit(2)


def run_claude(prompt: str, cli_model: str, workdir: str, max_turns: int, allowed_tools: str | None) -> ExecResult:
    cmd = ["claude", "-p", prompt, "--model", cli_model, "--output-format", "json", "--max-turns", str(max_turns)]
    if allowed_tools:
        cmd += ["--allowedTools", allowed_tools]
    r = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=1200)
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return ExecResult(False, 0, 0, 0.0, r.stdout + r.stderr, error="claude CLI produced non-JSON output")
    usage = data.get("usage", {})
    ok = data.get("subtype") == "success" and not data.get("is_error", False)
    return ExecResult(
        ok=ok,
        input_tokens=usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0) + usage.get("cache_read_input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        cost_usd=data.get("total_cost_usd", 0.0),
        raw_output=data.get("result", ""),
        error="" if ok else data.get("result", "unknown claude error"),
    )


def run_opencode(prompt: str, cli_model: str, workdir: str) -> ExecResult:
    """OpenCode's `run` subcommand has no --output-format json flag as of
    v1.18.18 (confirmed live 2026-08-13) -- pull real usage from `opencode
    stats --models` (human-readable table) before/after and diff, since
    that's the only place real per-model token/cost numbers surface."""
    cmd = ["opencode", "run", prompt, "--model", cli_model]
    before = _opencode_stats_snapshot(cli_model)
    r = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=1200)
    after = _opencode_stats_snapshot(cli_model)
    delta = {
        "input_tokens": max(0, after["input_tokens"] - before["input_tokens"]),
        "output_tokens": max(0, after["output_tokens"] - before["output_tokens"]),
        "cost_usd": max(0.0, after["cost_usd"] - before["cost_usd"]),
    }
    ok = r.returncode == 0
    return ExecResult(
        ok=ok,
        input_tokens=delta["input_tokens"],
        output_tokens=delta["output_tokens"],
        cost_usd=delta["cost_usd"],
        raw_output=r.stdout,
        error="" if ok else r.stderr[-2000:],
    )


def _opencode_stats_snapshot(cli_model: str) -> dict:
    """Parse `opencode stats --models` real table output for one model's
    row. VERIFIED live 2026-08-13 against a real deepseek/deepseek-v4-flash
    run -- table shape is:
        ...
        deepseek/deepseek-v4-flash
          Messages                          1
          Input Tokens                    7.4K
          Output Tokens                     19
          Cache Read                         0
          Cache Write                        0
          Cost                          $0.0010
    Values use K/M suffixes for thousands/millions -- must be expanded, not
    parsed as plain ints, or every non-trivial run silently truncates to 0.
    """
    r = subprocess.run(["opencode", "stats", "--models"], capture_output=True, text=True, timeout=15)
    lines = r.stdout.splitlines()
    result = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
    in_block = False
    for i, line in enumerate(lines):
        stripped = line.strip().strip("│").strip()
        if stripped == cli_model:
            in_block = True
            continue
        if in_block:
            if stripped.startswith("├") or stripped.startswith("└"):
                break
            if "Input Tokens" in stripped:
                result["input_tokens"] = _parse_suffixed_number(stripped)
            elif "Output Tokens" in stripped:
                result["output_tokens"] = _parse_suffixed_number(stripped)
            elif "Cost" in stripped:
                m = re.search(r"\$([\d.]+)", stripped)
                result["cost_usd"] = float(m.group(1)) if m else 0.0
    return result


def _parse_suffixed_number(line: str) -> int:
    """'Input Tokens    7.4K' -> 7400. Handles bare ints, K, M suffixes."""
    m = re.search(r"([\d.]+)\s*([KM]?)\s*$", line)
    if not m:
        return 0
    val = float(m.group(1))
    mult = {"K": 1_000, "M": 1_000_000, "": 1}[m.group(2)]
    return int(val * mult)


def run_plan_pass(task_context: str, prompt: str, plan_arm: str, workdir: str) -> tuple[dict, ExecResult]:
    """Plan model runs with NO write tools -- it must only produce the plan
    JSON per harness/plan_schema.md, never touch the fixture itself. This
    is enforced via --allowedTools for claude; for opencode there is no
    documented per-call tool restriction as of 2026-08-13, so a strong
    prompt instruction is the only guard until that's confirmed -- flagged
    as a real gap, not silently assumed safe."""
    plan_prompt = (
        f"{task_context}\n\nTASK PROMPT: {prompt}\n\n"
        "You are the PLAN model. Do NOT edit any files or run any mutating "
        "commands. Produce ONLY a JSON object matching this exact shape "
        "(see harness/plan_schema.md for the full contract):\n"
        '{"task_id": "...", "steps": [{"id": 1, "action": "...", '
        '"verification": "...", "depends_on": []}], "risks_flagged": ["..."]}\n'
        "Output ONLY the JSON, no prose before or after it."
    )
    arm = ARMS[plan_arm]
    if arm["executor"] == "claude":
        res = run_claude(plan_prompt, arm["cli_model"], workdir, max_turns=3, allowed_tools="")
    else:
        res = run_opencode(plan_prompt, arm["cli_model"], workdir)
    plan_match = re.search(r"\{.*\}", res.raw_output, re.DOTALL)
    plan = json.loads(plan_match.group(0)) if plan_match else {"steps": [], "risks_flagged": ["PLAN PARSE FAILED"]}
    return plan, res


def run_work_pass(task_context: str, plan: dict, work_arm: str, workdir: str, max_turns: int) -> ExecResult:
    work_prompt = (
        f"{task_context}\n\n"
        "You are the WORK model, executing a plan handed to you by a separate "
        "planning pass. Execute these steps in dependency order. You have NO "
        "planning authority -- do not re-scope, skip, or reorder steps on your "
        "own judgment; if a step is genuinely blocked, report back rather than "
        "silently improvising a different approach.\n\n"
        f"STEPS: {json.dumps(plan.get('steps', []), indent=2)}\n"
        f"RISKS FLAGGED BY THE PLANNER: {json.dumps(plan.get('risks_flagged', []), indent=2)}"
    )
    arm = ARMS[work_arm]
    if arm["executor"] == "claude":
        return run_claude(work_prompt, arm["cli_model"], workdir, max_turns=max_turns, allowed_tools=None)
    return run_opencode(work_prompt, arm["cli_model"], workdir)


def parse_task_file(path: Path) -> dict:
    text = path.read_text()
    def section(name: str) -> str:
        m = re.search(rf"## {re.escape(name)}.*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
        return m.group(1).strip() if m else ""
    verification_block = section("Objective verification (run after the agent finishes)")
    verification_cmds = re.findall(r"```(?:bash|python)?\n(.*?)\n```", verification_block, re.DOTALL)
    return {
        "task_id": path.stem.split("-", 1)[0] + "-" + "-".join(path.stem.split("-")[1:3]),
        "context": section("Context (given to the agent verbatim)"),
        "prompt": section("Prompt (given to the agent verbatim)"),
        "verification_cmds": verification_cmds,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True, help="Path to a task .md file")
    ap.add_argument("--arm", required=True, choices=list(ARMS.keys()) + list(SPLIT_ARMS.keys()))
    ap.add_argument("--workdir", required=True, help="Fixture directory this task operates on (must already be seeded per the task's ## Setup)")
    ap.add_argument("--calibrated-token-budget", type=int, required=True, help="From the task file's Token budget calibration section, once measured")
    ap.add_argument("--reusability-score", type=float, default=-1.0, help="Fill in from an independent reusability read; -1 marks it TODO in the output")
    ap.add_argument("--max-turns", type=int, default=20)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    check_prereqs(args.arm)
    task = parse_task_file(Path(args.task))

    if args.arm in SPLIT_ARMS:
        plan_arm, work_arm = SPLIT_ARMS[args.arm]
        plan, plan_res = run_plan_pass(task["context"], task["prompt"], plan_arm, args.workdir)
        work_res = run_work_pass(task["context"], plan, work_arm, args.workdir, args.max_turns)
        input_tokens = {"plan": plan_res.input_tokens, "work": work_res.input_tokens}
        output_tokens = {"plan": plan_res.output_tokens, "work": work_res.output_tokens}
        plan_model, work_model = plan_arm, work_arm
        exec_ok = work_res.ok
        notes = f"plan_ok={plan_res.ok} work_ok={work_res.ok} plan_error={plan_res.error!r} work_error={work_res.error!r}"
    else:
        arm = ARMS[args.arm]
        full_prompt = f"{task['context']}\n\nTASK: {task['prompt']}"
        if arm["executor"] == "claude":
            res = run_claude(full_prompt, arm["cli_model"], args.workdir, args.max_turns, allowed_tools=None)
        else:
            res = run_opencode(full_prompt, arm["cli_model"], args.workdir)
        input_tokens = {"work": res.input_tokens}
        output_tokens = {"work": res.output_tokens}
        plan_model, work_model = None, args.arm
        exec_ok = res.ok
        notes = f"exec_ok={res.ok} error={res.error!r}"

    # Run the task's OWN objective-verification command(s) fresh -- this is
    # the ONLY source of truth for correctness (scoring.py's own docstring
    # rule, enforced here at the point of data collection so a bad run.json
    # can never claim "verification_passed": true without this having
    # actually happened).
    verification_passed = exec_ok  # execution must have succeeded to even attempt verification
    verification_output = ""
    if exec_ok:
        for cmd in task["verification_cmds"]:
            r = subprocess.run(cmd, shell=True, cwd=args.workdir, capture_output=True, text=True, timeout=600)
            verification_output += f"$ {cmd}\n{r.stdout}\n{r.stderr}\n"
            if r.returncode != 0:
                verification_passed = False

    run_record = {
        "task_id": task["task_id"],
        "arm": args.arm,
        "plan_model": plan_model,
        "work_model": work_model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "verification_passed": verification_passed,
        "verification_output": verification_output[-4000:],
        "calibrated_token_budget": args.calibrated_token_budget,
        "reusability_score": args.reusability_score,
        "notes": notes,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(run_record, indent=2))
    print(f"wrote {args.out}")
    print(json.dumps({"verification_passed": verification_passed, "notes": notes}, indent=2))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# TODO / honest open gaps as of 2026-08-13 (do not silently paper over these
# when picking this up -- verify each one live before trusting a real run):
#
# 1. RESOLVED (was BLOCKED): Claude Code CLI login via `claude auth login
#    --console` works (needs a human OAuth step once per machine). BUT a
#    NEW real gap surfaced: the resulting account has $0 API credit
#    ("Credit balance is too low" on every real call). check_prereqs()
#    now probes for this exact failure and fails fast. Fix is either
#    loading credits on the console account, or logging in with an actual
#    claude.ai subscription (`claude auth login`, no --console) instead.
# 2. RESOLVED (was BLOCKED): DeepSeek arms fully work via OpenCode with
#    just DEEPSEEK_API_KEY in the environment -- no login, no OpenRouter
#    needed. Verified live: deepseek/deepseek-v4-pro and
#    deepseek/deepseek-v4-flash both smoke-tested successfully on the
#    dedicated hermes-bench LXC.
# 3. RESOLVED (was UNVERIFIED): `opencode stats --models` real table
#    format has been parsed and verified against a live run
#    (_opencode_stats_snapshot / _parse_suffixed_number). K/M-suffixed
#    values are expanded correctly (confirmed: "7.4K" -> 7400).
# 4. STILL BLOCKED: OpenRouter-routed arms (gpt-5.6-terra, grok-4.6,
#    glm-5.2, gemini-3.6-flash) -- no OPENROUTER_API_KEY configured
#    anywhere in this Hermes profile as of 2026-08-13.
# 5. NOT YET BUILT: fixture provisioning. This script assumes --workdir
#    already has the task's ## Setup state materialized. A companion
#    `harness/seed_fixture.py <task-id>` that actually runs each task's
#    Setup commands (docker containers, git repos, seeded bugs) does not
#    exist yet -- without it, this script can only be run against a
#    manually-prepared workdir.
# 6. NOT YET DECIDED (from docs/methodology.md's own open question):
#    reusability_score is currently a required CLI arg with no automated
#    path -- someone/something must read the artifact and score it
#    independently before this script can be run end-to-end unattended.
# ---------------------------------------------------------------------------
