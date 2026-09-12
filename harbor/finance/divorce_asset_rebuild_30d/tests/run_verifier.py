#!/usr/bin/env python3
"""Score this task from immutable Harbor stage evidence."""
from __future__ import annotations

import importlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from harbor_evidence import EvidenceError, HarborEvidence

RUBRICS_ROOT = ROOT / "rubrics"
EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path(os.environ.get("VERIFIER_REWARD_PATH", "/logs/verifier/reward.json"))
REPORT_PATH = Path(os.environ.get("VERIFIER_REPORT_PATH", "/logs/verifier/checks.json"))
STAGE_COUNT = 23
EXPECTED_CHECK_COUNT = 66

class VerifierInfrastructureError(RuntimeError):
    pass

def _load(name: str):
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path: sys.path.insert(0, parent)
    try: return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception as exc: raise VerifierInfrastructureError(f"rubric import {name}: {exc}") from exc

def _spec(row: Any, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3: raise VerifierInfrastructureError(f"invalid check spec in {tag}")
    name, fn, weight = row
    if isinstance(weight, bool) or not isinstance(weight, (int, float)) or not math.isfinite(float(weight)) or float(weight) <= 0: raise VerifierInfrastructureError(f"invalid weight for {name} in {tag}")
    return str(name), fn, float(weight)

def _modules() -> list[str]:
    names=[]
    for path in sorted(RUBRICS_ROOT.glob("*.py")):
        if path.stem.startswith("_") or path.stem in {"__init__", "stage_checks"} or path.stem.startswith("stage_"): continue
        try:
            if hasattr(_load(path.stem), "CHECKS"): names.append(path.stem)
        except VerifierInfrastructureError: raise
    return names

def _inventory() -> tuple[dict[str,float], int]:
    inv={}; count=0
    for stage in range(STAGE_COUNT):
        module=_load(f"stage_{stage}"); rows=getattr(module,"CHECKS",[]); total=0.0
        for row in rows: total += _spec(row,f"stage_{stage}")[2]
        inv[f"stage_{stage}"]=total; count += len(rows)
    for name in _modules():
        module=_load(name); rows=getattr(module,"CHECKS",[]); inv[{"cross_stage":"cross","final":"final"}.get(name,name)] = sum(_spec(r,name)[2] for r in rows); count += len(rows)
    return inv, count

def _run(spec: Any, env: HarborEvidence, tag: str) -> tuple[list[dict[str,Any]], dict[str,Any]]:
    reports=[]; earned=0.0; eligible=0.0
    for row in spec:
        name, fn, weight = _spec(row, tag)
        try: result=fn(env)
        except Exception as exc: raise VerifierInfrastructureError(f"check {name} ({tag}) raised {type(exc).__name__}: {exc}") from exc
        if type(result) is not bool: raise VerifierInfrastructureError(f"check {name} ({tag}) returned {type(result).__name__}")
        score=1.0 if result else 0.0; earned += score*weight; eligible += weight
        reports.append({"name":name,"check_id":name,"passed":result,"check_score":score,"weight":weight,"earned_score":score*weight,"pass_threshold":1.0,"applicable":True,"evidence":[f"checker:{name}"],"tags":[tag],"detail":""})
    if eligible < 0.0: raise VerifierInfrastructureError(f"negative eligible weight in {tag}")
    return reports,{"raw_earned_score":earned,"eligible_weight":eligible,"normalized_score":earned/eligible if eligible>0 else 0.0}

def _write(reward: float, report: dict[str,Any], ok: bool) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True); REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REWARD_PATH.write_text(json.dumps({"reward":float(reward),"verifier_ok":1.0 if ok else 0.0},allow_nan=False)+"\n",encoding="utf-8")
    REPORT_PATH.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")

def main() -> int:
    step=os.environ.get("HARBOR_STEP_NAME",""); stage=int(os.environ.get("VIRTUAL_STAGE","0")); include_all=os.environ.get("INCLUDE_ALL_BUCKETS") == "1"; run_stage=os.environ.get("RUN_STAGE_RUBRIC","1") == "1"; boundary=os.environ.get("STAGE_BOUNDARY") == "1"
    env=HarborEvidence(EVIDENCE_ROOT); checks=[]; buckets={}; errors=[]
    try: inventory, count = _inventory()
    except Exception as exc: inventory,count={},0; errors.append(f"inventory: {type(exc).__name__}: {exc}")
    pool=sum(inventory.values())
    try:
        if count != EXPECTED_CHECK_COUNT: raise VerifierInfrastructureError(f"check count {count} != {EXPECTED_CHECK_COUNT}")
        if pool <= 0: raise VerifierInfrastructureError("rubric pool is empty")
        if include_all:
            total_earned=0.0; total_eligible=0.0
            for idx in range(STAGE_COUNT):
                env.current_stage=idx; env.validate_stage(idx); module=_load(f"stage_{idx}"); rows, detail=_run(module.CHECKS,env,f"stage{idx}"); checks.extend(rows); buckets[f"stage_{idx}"]=detail; total_earned += detail["raw_earned_score"]; total_eligible += detail["eligible_weight"]
            env.current_stage=STAGE_COUNT-1
            for name in _modules():
                module=_load(name); rows,detail=_run(module.CHECKS,env,name); checks.extend(rows); buckets[{"cross_stage":"cross","final":"final"}.get(name,name)]=detail; total_earned += detail["raw_earned_score"]; total_eligible += detail["eligible_weight"]
            if not math.isclose(total_eligible,pool,abs_tol=1e-9): raise VerifierInfrastructureError(f"scored weight {total_eligible} != pool {pool}")
            reward=total_earned/pool
        elif run_stage:
            env.current_stage=stage; env.validate_stage(stage); module=_load(f"stage_{stage}"); rows,detail=_run(module.CHECKS,env,f"stage{stage}"); checks.extend(rows); buckets["stage"]={**detail,"current_stage":stage}; reward=detail["raw_earned_score"]/pool
        else: reward=0.0
    except Exception as exc: errors.append(f"stage {stage}: {type(exc).__name__}: {exc}"); reward=0.0
    report={"step":step,"virtual_stage":stage,"stage_boundary":boundary,"include_all_buckets":include_all,"verifier_mode":"immutable-sidecar-flat-pool","scoring":"global-weighted-flat-pool","pool_total_weight":pool,"weight_inventory":inventory,"check_count":count,"evidence_root":str(EVIDENCE_ROOT),"buckets":buckets,"reward":reward,"status":"infrastructure_error" if errors else "ok","errors":errors,"checks":checks}
    _write(reward,report,not errors)
    if errors:
        print("VERIFIER INFRASTRUCTURE ERROR: " + "; ".join(errors[:5]),file=sys.stderr); return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
