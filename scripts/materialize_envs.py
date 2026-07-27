#!/usr/bin/env python3
"""Materialise the top-level ``envs/`` tree the capabilities layer loads from.

Tasks ship their environments task-locally::

    eval_set/<domain>/<task>/envs/<service>/<env_name>/

but ``AgentMockServerCapability._resolve_env_dir`` resolves them from a single
top-level directory::

    <PROJECT_ROOT>/envs/<service>/<env_name>/

so the top-level tree has to exist before any task runs. Its presence is also
what ``capabilities/__init__.py`` walks parents to find when it discovers
PROJECT_ROOT, so a fresh clone cannot import ``capabilities`` until this has
been run once.

The 137 bindings in this release carry no conflicting ``(service, env_name)``
pairs, so the flattened layout is lossless. A pair contributed by more than one
task with differing content is a packaging error and aborts the run.

Usage:
    python3 scripts/materialize_envs.py            # build ./envs
    python3 scripts/materialize_envs.py --check    # verify only, exit 1 on drift
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import shutil
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_SET = REPO_ROOT / "eval_set"
TARGET = REPO_ROOT / "envs"


def _digest(env_dir: Path) -> str:
    """Content hash over a env directory's relative paths and bytes."""
    h = hashlib.sha256()
    for f in sorted(p for p in env_dir.rglob("*") if p.is_file()):
        h.update(f.relative_to(env_dir).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()


def discover() -> dict[tuple[str, str], Path]:
    """Map (service, env_name) -> source dir, aborting on conflicting duplicates."""
    seen: dict[tuple[str, str], tuple[Path, str]] = {}
    conflicts: dict[tuple[str, str], set[Path]] = defaultdict(set)

    for env_dir in sorted(EVAL_SET.glob("*/*/envs/*/*")):
        if not env_dir.is_dir():
            continue
        key = (env_dir.parent.name, env_dir.name)
        digest = _digest(env_dir)
        if key in seen:
            if seen[key][1] != digest:
                conflicts[key].update({seen[key][0], env_dir})
            continue
        seen[key] = (env_dir, digest)

    if conflicts:
        print("ERROR: same (service, env_name) shipped with differing content:", file=sys.stderr)
        for (svc, env), dirs in sorted(conflicts.items()):
            print(f"  {svc}/{env}", file=sys.stderr)
            for d in sorted(dirs):
                print(f"    {d.relative_to(REPO_ROOT)}", file=sys.stderr)
        raise SystemExit(1)

    return {k: v[0] for k, v in seen.items()}


def check(bindings: dict[tuple[str, str], Path]) -> int:
    missing, differing = [], []
    for (svc, env), src in sorted(bindings.items()):
        dst = TARGET / svc / env
        if not dst.is_dir():
            missing.append(f"{svc}/{env}")
            continue
        cmp = filecmp.dircmp(src, dst)
        if cmp.left_only or cmp.right_only or cmp.diff_files:
            differing.append(f"{svc}/{env}")

    if missing or differing:
        for name in missing:
            print(f"missing:   envs/{name}")
        for name in differing:
            print(f"differing: envs/{name}")
        print(f"\n{len(missing)} missing, {len(differing)} differing "
              f"of {len(bindings)} bindings — re-run without --check.")
        return 1

    print(f"envs/ is in sync with all {len(bindings)} task-local bindings.")
    return 0


def build(bindings: dict[tuple[str, str], Path]) -> int:
    if TARGET.exists():
        shutil.rmtree(TARGET)
    for (svc, env), src in sorted(bindings.items()):
        shutil.copytree(src, TARGET / svc / env)

    services = sorted({svc for svc, _ in bindings})
    print(f"Materialised {len(bindings)} env bindings across "
          f"{len(services)} services into {TARGET.relative_to(REPO_ROOT)}/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify envs/ matches the task-local sources; do not write")
    args = parser.parse_args()

    if not EVAL_SET.is_dir():
        print(f"ERROR: {EVAL_SET} not found; run from a full checkout.", file=sys.stderr)
        return 1

    bindings = discover()
    if not bindings:
        print(f"ERROR: no env bindings found under {EVAL_SET.relative_to(REPO_ROOT)}/"
              "*/*/envs/<service>/<env_name>/; refusing to report success on an "
              "empty tree.", file=sys.stderr)
        return 1

    return check(bindings) if args.check else build(bindings)


if __name__ == "__main__":
    raise SystemExit(main())
