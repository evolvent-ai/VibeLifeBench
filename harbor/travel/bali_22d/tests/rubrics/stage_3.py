"""Stage 3: pregnancy activity advice must cover the requested risk dimensions."""
from __future__ import annotations

import re
from loguru import logger

from .shared._helpers import _agent_responses


def s3_hot_spring_temperature_stated(env) -> bool:
    resp = _agent_responses(env, 3).casefold()
    temperature = bool(re.search(r"(?:38\s*(?:°?c|deg)|100\s*°?f)", resp))
    diving = any(x in resp for x in ("scuba", "scuba")) and any(
        x in resp for x in ("avoid", "avoid", "not recommended")
    )
    snorkeling = any(x in resp for x in ("snorkel", "snorkel", "sea turtle")) and any(
        x in resp for x in ("on shore", "glass-bottom", "glass-bottom", "alternative", "avoid", "not recommended")
    )
    impact = any(x in resp for x in ("rafting", "rafting")) and any(
        x in resp for x in ("atv", "bumpy", "bumpy", "impact")
    )
    altitude = any(x in resp for x in ("2500", "2,500", "altitude", "altitude"))
    boundary = any(x in resp for x in ("doctor", "obstetric", "doctor", "clinician"))
    result = bool(resp and temperature and diving and snorkeling and impact and altitude and boundary)
    logger.info("s3_activity_safety_bundle: {}", "PASS" if result else "FAIL")
    return result


CHECKS = [("s3_hot_spring_temperature_stated", s3_hot_spring_temperature_stated, 2.0)]
