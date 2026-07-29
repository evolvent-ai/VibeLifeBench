#!/usr/bin/env python3
"""Run VibeLifeBench and report scores.

Generates a Terrarium run config for the tasks you select, executes it, and
prints a per-task score table.

    # the whole open subset: 20 tasks, 1 attempt each
    python3 scripts/run_eval.py --model anthropic/claude-opus-4-8

    # a smoke test first — one task, to prove the stack works end to end
    python3 scripts/run_eval.py --model anthropic/claude-opus-4-8 --tasks galapagos_no_us_transit

    # avg@3, the standard reporting protocol
    python3 scripts/run_eval.py --model anthropic/claude-opus-4-8 --attempts 3

    # re-print scores for a finished run, or watch one in progress
    python3 scripts/run_eval.py --report outputs/<job_name>

Prerequisites are checked before anything is launched; see README "Quickstart".
"""
from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_SET = REPO_ROOT / "eval_set"
DEFAULT_MODELS_JSON = REPO_ROOT / "models.json"

# Enough headroom for the longest task; trials are killed past this.
DEFAULT_TIMEOUT_SEC = 14400


def resolve_user_path(path: Path) -> Path:
    """Expand and resolve a CLI path relative to the caller's working directory."""
    return path.expanduser().resolve()


def config_path_value(path: Path) -> str:
    """Use portable repo-relative paths, while preserving external absolute paths."""
    resolved = resolve_user_path(path)
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return str(resolved)


def discover_tasks() -> dict[str, Path]:
    """Map task id -> task dir, for every task in the eval set."""
    return {
        d.name: d
        for d in sorted(EVAL_SET.glob("*/*"))
        if (d / "task.py").is_file()
    }


def select(all_tasks: dict[str, Path], wanted: list[str] | None,
           domains: list[str] | None) -> dict[str, Path]:
    if wanted:
        unknown = [t for t in wanted if t not in all_tasks]
        if unknown:
            print(f"ERROR: unknown task id(s): {', '.join(unknown)}", file=sys.stderr)
            print("\nAvailable tasks:", file=sys.stderr)
            for name, path in all_tasks.items():
                print(f"  {path.parent.name:20s} {name}", file=sys.stderr)
            raise SystemExit(2)
        return {t: all_tasks[t] for t in wanted}

    if domains:
        known = {p.parent.name for p in all_tasks.values()}
        unknown = [d for d in domains if d not in known]
        if unknown:
            print(f"ERROR: unknown domain(s): {', '.join(unknown)}", file=sys.stderr)
            print(f"Available domains: {', '.join(sorted(known))}", file=sys.stderr)
            raise SystemExit(2)
        return {n: p for n, p in all_tasks.items() if p.parent.name in domains}

    return all_tasks


def preflight(models_json: Path, tasks: dict[str, Path]) -> None:
    """Fail early, with the fix, rather than deep inside a trial."""
    problems: list[str] = []

    if not (REPO_ROOT / "envs").is_dir():
        problems.append(
            "Top-level envs/ is missing (the capability layer loads environments "
            "from it).\n    Fix: python3 scripts/materialize_envs.py"
        )

    if not models_json.is_file():
        problems.append(
            f"{models_json.name} not found.\n"
            f"    Fix: cp models.json.example {models_json.name} "
            f"&& chmod 600 {models_json.name}, then fill in your endpoint and key."
        )

    terrarium = REPO_ROOT / ".venv" / "bin" / "terrarium"
    if not terrarium.is_file():
        problems.append(
            "Terrarium is not installed in .venv.\n    Fix: uv sync"
        )

    if shutil.which("docker") is None:
        problems.append(
            "docker not found on PATH; the mock services run as containers."
        )
    else:
        try:
            out = subprocess.run(["docker", "images", "--format", "{{.Repository}}"],
                                 capture_output=True, text=True, timeout=30)
            built = {ln for ln in out.stdout.splitlines()
                     if ln.startswith("vibe-agent-benchmark/")}
            needed = {f"vibe-agent-benchmark/{d.name}"
                      for d in (REPO_ROOT / "servers").glob("*_mock")}
            if missing := needed - built:
                problems.append(
                    f"{len(missing)} of {len(needed)} mock service images are not built "
                    f"(e.g. {sorted(missing)[0]}).\n    Fix: ./build_images.sh"
                )
        except (subprocess.SubprocessError, OSError) as exc:
            problems.append(f"Could not query docker images: {exc}")

    if not tasks:
        problems.append("No tasks selected.")

    if problems:
        print("Preflight failed:\n", file=sys.stderr)
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}\n", file=sys.stderr)
        raise SystemExit(1)


def write_config(path: Path, job_name: str, job_dir: Path, tasks: dict[str, Path],
                 model: str, models_json: Path, attempts: int, concurrent: int,
                 timeout_sec: int, think: str) -> None:
    rel = [str(p.relative_to(REPO_ROOT)) for p in tasks.values()]
    task_lines = ",\n  ".join(f'"{r}"' for r in rel)
    path.write_text(
        f'# Generated by scripts/run_eval.py — safe to edit and re-run with:\n'
        f'#   .venv/bin/terrarium run -c {path.relative_to(REPO_ROOT)}\n'
        f'job_name = "{job_name}"\n'
        f'job_dir = "{job_dir.relative_to(REPO_ROOT)}"\n'
        f'tasks = [\n  {task_lines},\n]\n'
        f'n_attempts = {attempts}\n'
        f'n_concurrent_trials = {concurrent}\n'
        f'agent_exec_timeout_sec = {timeout_sec}\n'
        f'resume = false\n'
        f'\n'
        f'[[agents]]\n'
        f'name = "openclaw"\n'
        f'model_name = "{model}"\n'
        f'\n'
        f'[agents.kwargs]\n'
        f'models_config_path = "{config_path_value(models_json)}"\n'
        f'think = "{think}"\n',
        encoding="utf-8",
    )


def collect(job_dir: Path) -> list[dict]:
    """One row per trial. Crashed trials keep score=None."""
    rows = []
    for f in sorted(job_dir.glob("*/result.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        # Trial dirs are <agent>__<model>__adhoc__<task id>.
        task = f.parent.name.split("adhoc__")[-1]
        if d.get("exception_info"):
            rows.append({"task": task, "score": None, "passed": 0, "total": 0, "sec": 0.0})
            continue
        cr = d.get("checker_result") or {}
        checks = cr.get("checks") or []
        rows.append({
            "task": task,
            "score": cr.get("score"),
            "passed": sum(1 for c in checks if c.get("passed")),
            "total": len(checks),
            "sec": (d.get("timing") or {}).get("duration_sec") or 0.0,
        })
    return rows


def report(job_dir: Path) -> int:
    rows = collect(job_dir)
    if not rows:
        print(f"No trial results under {job_dir}.")
        print("A run in progress writes result.json only as each trial finishes.")
        return 1

    # Several attempts of one task share a task id; average them per task.
    by_task: dict[str, list[dict]] = {}
    for r in rows:
        by_task.setdefault(r["task"], []).append(r)

    print(f"\n{job_dir.name}  —  {len(by_task)} tasks, {len(rows)} trials\n")
    print(f"{'task':52s} {'score':>7s} {'checks':>11s} {'min':>6s}")
    print("-" * 80)

    task_scores: list[float] = []
    crashed = 0
    for task in sorted(by_task):
        trials = by_task[task]
        done = [t for t in trials if t["score"] is not None]
        crashed += len(trials) - len(done)
        if not done:
            print(f"{task:52s} {'CRASH':>7s}")
            continue
        mean = statistics.mean(t["score"] for t in done)
        task_scores.append(mean)
        passed = sum(t["passed"] for t in done) / len(done)
        total = done[0]["total"]
        minutes = sum(t["sec"] for t in done) / len(done) / 60
        n = f" (n={len(done)})" if len(trials) > 1 else ""
        print(f"{task:52s} {mean:7.4f} {passed:5.0f}/{total:<5d} {minutes:6.0f}{n}")

    if task_scores:
        label = "avg@n" if any(len(v) > 1 for v in by_task.values()) else "score"
        print("-" * 80)
        print(f"{'OVERALL (' + label + ', mean over tasks)':52s} "
              f"{statistics.mean(task_scores):7.4f}")
        print(f"\n  tasks={len(task_scores)}  "
              f"median={statistics.median(task_scores):.4f}  "
              f"min={min(task_scores):.4f}  max={max(task_scores):.4f}"
              + (f"  crashed_trials={crashed}" if crashed else ""))
    if crashed:
        print(f"\n  {crashed} trial(s) crashed — see {job_dir}/*/trial.log")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", help='model as "<provider>/<id>", matching models.json')
    p.add_argument("--tasks", nargs="+", metavar="ID", help="task ids (default: every task in eval_set)")
    p.add_argument("--domains", nargs="+", metavar="D", help="whole domains, e.g. travel finance")
    p.add_argument("--attempts", type=int, default=1,
                   help="attempts per task; 3 gives the standard avg@3 (default: 1)")
    p.add_argument("--concurrent", type=int, default=4,
                   help="trials in parallel; each runs its own containers (default: 4)")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SEC,
                   help=f"per-trial timeout in seconds (default: {DEFAULT_TIMEOUT_SEC})")
    p.add_argument("--think", default="xhigh",
                   help="OpenClaw thinking level: off|minimal|low|medium|high|xhigh (default: xhigh)")
    p.add_argument("--models-json", type=Path, default=DEFAULT_MODELS_JSON,
                   help="path to the OpenClaw model config (default: models.json)")
    p.add_argument("--job-name", help="output dir name (default: derived from model and time)")
    p.add_argument("--report", metavar="JOB_DIR",
                   help="print the score table for an existing job and exit")
    p.add_argument("--list", action="store_true", help="list task ids and exit")
    p.add_argument("--dry-run", action="store_true", help="write the run config, do not execute")
    args = p.parse_args()

    all_tasks = discover_tasks()

    if args.list:
        print(f"{len(all_tasks)} tasks:\n")
        for name, path in all_tasks.items():
            print(f"  {path.parent.name:20s} {name}")
        return 0

    if args.report:
        return report(Path(args.report))

    if not args.model:
        p.error("--model is required (or use --report / --list)")

    tasks = select(all_tasks, args.tasks, args.domains)
    models_json = resolve_user_path(args.models_json)
    preflight(models_json, tasks)

    job_name = args.job_name or (
        f"{args.model.replace('/', '_')}_{len(tasks)}tasks_"
        f"{time.strftime('%Y%m%d_%H%M%S')}"
    )
    job_dir = REPO_ROOT / "outputs" / job_name
    cfg = REPO_ROOT / "outputs" / f"{job_name}.toml"
    cfg.parent.mkdir(parents=True, exist_ok=True)
    write_config(cfg, job_name, job_dir, tasks, args.model, models_json,
                 args.attempts, args.concurrent, args.timeout, args.think)

    print(f"model      {args.model}")
    print(f"tasks      {len(tasks)} × {args.attempts} attempt(s) "
          f"= {len(tasks) * args.attempts} trials")
    print(f"config     {cfg.relative_to(REPO_ROOT)}")
    print(f"output     {job_dir.relative_to(REPO_ROOT)}")

    if args.dry_run:
        print("\n--dry-run: config written, nothing executed.")
        return 0

    print(f"\nA full run takes many hours; each trial is a multi-week "
          f"simulated timeline.\nProgress: tail -f {job_dir.relative_to(REPO_ROOT)}/job.log\n")

    terrarium = REPO_ROOT / ".venv" / "bin" / "terrarium"
    proc = subprocess.run([str(terrarium), "run", "-c", str(cfg)], cwd=REPO_ROOT)
    if proc.returncode != 0:
        print(f"\nterrarium exited {proc.returncode}. Partial results, if any:",
              file=sys.stderr)

    report(job_dir)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
