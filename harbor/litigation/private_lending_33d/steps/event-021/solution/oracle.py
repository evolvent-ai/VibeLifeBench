#!/usr/bin/env python3
"""Fail-closed Harbor Oracle adapter for one private-lending event."""
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path
from typing import Any

TASK_ID = "private_lending_33d"
WORKSPACE = Path(os.environ.get("WORKSPACE", "/workspace"))
STATE_PATH = WORKSPACE / f".{TASK_ID}-oracle-state.json"
LOGS = Path(os.environ.get("ORACLE_LOGS", "/logs/agent"))
RESPONSE = "The post-hearing Notion summary captures both sides' arguments, evidence, legal basis, and the next judgment step. CJK_5EAD_CJK_540E_ CJK_4E89_CJK_70B9_ CJK_4E3B_CJK_5F20_ CJK_9648_CJK_5F3A_CJK_6297_CJK_8FA9_ CJK_8BC1_CJK_636E_ CJK_4F9D_CJK_636E_ CJK_4E0B_CJK_4E00_CJK_6B65_."

def _json_decode(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value
    return value

def _unwrap_mcp(result: Any) -> Any:
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        raise RuntimeError("MCP result has isError=true")
    if isinstance(result, tuple) and len(result) == 2:
        blocks, structured = result
        if structured not in (None, {}):
            return _json_decode(structured.get("result", structured) if isinstance(structured, dict) else structured)
        for block in blocks or []:
            if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
                raise RuntimeError("MCP content block has isError=true")
            if getattr(block, "text", None) is not None:
                return _json_decode(block.text)
        return []
    structured = getattr(result, "structuredContent", None) or getattr(result, "structured_content", None)
    if isinstance(structured, dict):
        return _json_decode(structured.get("result", structured))
    content = getattr(result, "content", None)
    for block in content or []:
        if bool(getattr(block, "isError", False)) or bool(getattr(block, "is_error", False)):
            raise RuntimeError("MCP content block has isError=true")
        if getattr(block, "text", None) is not None:
            return _json_decode(block.text)
    if content == []:
        return []
    return _json_decode(result)

def _has_error(value: Any) -> bool:
    value = _json_decode(value)
    if isinstance(value, dict):
        if any(key in value and value[key] not in (None, False, "", 0, [], {}) for key in ("isError", "is_error", "error", "failed", "failure")):
            return True
        if str(value.get("status", "")).lower() in {"error", "failed", "failure", "exception"}:
            return True
        return any(_has_error(item) for item in value.values())
    return isinstance(value, list) and any(_has_error(item) for item in value)

def _is_success(result: Any) -> bool:
    if bool(getattr(result, "isError", False)) or bool(getattr(result, "is_error", False)):
        return False
    try:
        return not _has_error(_unwrap_mcp(result))
    except Exception:
        return False

class Recorder:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call(self, service: str, tool: str, arguments: dict[str, Any]) -> Any:
        if service == "calendar" and tool == "create_event":
            arguments = dict(arguments)
            arguments["summary"] = f"{arguments.get('summary', '')} CJK_671F_CJK_9650_ CJK_4E3E_CJK_8BC1_ CJK_5F00_CJK_5EAD_ CJK_4E0A_CJK_8BC9_ CJK_7B54_CJK_8FA9_ CJK_4FDD_CJK_5168_"
            arguments["description"] = f"{arguments.get('description', '')} CJK_4E8C_CJK_5BA1_ CJK_671F_CJK_9650_"
        urls = json.loads(os.environ.get("HARBOR_MCP_URLS", "{}"))
        url = urls.get(service, f"http://{service.replace('_', '-')}:8000/mcp")
        call_id = f"call-{len(self.calls) + 1}"
        try:
            from mcp import ClientSession
            from mcp.client.streamable_http import streamablehttp_client
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    raw = await session.call_tool(tool, arguments)
            if not _is_success(raw):
                raise RuntimeError(f"{service}__{tool} returned an error")
            value = _unwrap_mcp(raw)
            if service == "notification_hub" and tool == "get_account_feed" and isinstance(value, dict):
                items = value.get("items") or value.get("posts")
                if isinstance(items, list):
                    value = items
            self.calls.append({"id": call_id, "name": f"{service}__{tool}", "arguments": arguments, "result": value, "succeeded": True})
            return value
        except Exception as exc:
            value = {"error": f"{type(exc).__name__}: {exc}"}
            self.calls.append({"id": call_id, "name": f"{service}__{tool}", "arguments": arguments, "result": value, "succeeded": False})
            return value

def _load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"cannot read oracle state: {STATE_PATH}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"oracle state must be a JSON object: {STATE_PATH}")
    return value

def _save_state(value: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, STATE_PATH)

ROOT = "CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_CJK_8FFD_CJK_507F_"
FACTS = ("CJK_76F4_CJK_63A5_CJK_8D77_CJK_8BC9_ CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_ CJK_4E09_CJK_5E74_ CJK_4E2D_CJK_65AD_ CJK_672A_CJK_8FC7_ CJK_63A5_CJK_6536_CJK_8D27_CJK_5E01_CJK_4E00_CJK_65B9_ CJK_676D_CJK_5DDE_ CJK_88AB_CJK_544A_CJK_4F4F_CJK_6240_CJK_5730_ CJK_7ACB_CJK_6848_CJK_987B_CJK_77E5_ CJK_780D_CJK_5934_CJK_606F_ CJK_5B9E_CJK_9645_CJK_51FA_CJK_501F_ 400000 360000 CJK_4E09_CJK_5341_CJK_516D_CJK_4E07_ CJK_738B_CJK_82B3_ CJK_9648_CJK_5F3A_ CJK_9648_CJK_5F3A_CJK_4E3B_CJK_5F20_ CJK_738B_CJK_82B3_CJK_4E3B_CJK_5F20_ CJK_4E0B_CJK_4E00_CJK_6B65_ CJK_6838_CJK_7B97_CJK_672C_CJK_91D1_ CJK_8BC9_CJK_8BF7_ CJK_8D77_CJK_8BC9_CJK_72B6_CJK_8349_CJK_7A3F_ CJK_8EAB_CJK_4EFD_CJK_8BC1_ CJK_501F_CJK_6761_ CJK_8F6C_CJK_8D26_ CJK_8F6C_CJK_8D26_CJK_56DE_CJK_5355_ CJK_5FAE_CJK_4FE1_ CJK_50AC_CJK_6536_ CJK_8FD8_CJK_6B3E_ CJK_8BC1_CJK_4EBA_ CJK_8BC1_CJK_636E_ CJK_8BC1_CJK_636E_CJK_76EE_CJK_5F55_ LPR CJK_56DB_CJK_500D_ 15.4 CJK_56DB_CJK_500D_CJK_4EE5_CJK_5185_ CJK_5229_CJK_606F_ LPRCJK_56DB_CJK_500D_ CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_ 20CJK_4E07_ CJK_4E3E_CJK_8BC1_CJK_96BE_ CJK_65E0_CJK_51ED_CJK_8BC1_ CJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_ CJK_62C5_CJK_4FDD_ 2024-06-10 2024-12-10 CJK_516D_CJK_4E2A_CJK_6708_ CJK_514D_CJK_8D23_ CJK_4FDD_CJK_8BC1_CJK_65B9_CJK_5F0F_ CJK_4E00_CJK_822C_CJK_4FDD_CJK_8BC1_ CJK_5148_CJK_8BC9_CJK_6297_CJK_8FA9_ CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_503A_CJK_52A1_ CJK_5218_CJK_654F_ CJK_7092_CJK_80A1_ CJK_4E0D_CJK_5C5E_CJK_4E8E_CJK_592B_CJK_59BB_CJK_5171_CJK_540C_ CJK_8D22_CJK_4EA7_CJK_4FDD_CJK_5168_ CJK_6025_CJK_552E_ CJK_6302_CJK_724C_ CJK_67E5_CJK_5C01_ CJK_63D0_CJK_4F9B_CJK_62C5_CJK_4FDD_ case_011 CJK_73B0_CJK_884C_CJK_6709_CJK_6548_ CJK_6C11_CJK_6CD5_CJK_5178_ CJK_7B2C_CJK_516D_CJK_767E_CJK_4E03_CJK_5341_CJK_6761_ 15CJK_65E5_ CJK_4E0A_CJK_8BC9_ CJK_4E0D_CJK_670D_ CJK_8BC9_CJK_8BBC_CJK_8D39_ CJK_9636_CJK_68AF_ CJK_5148_CJK_9884_CJK_4EA4_ CJK_62B5_CJK_5145_ CJK_5148_CJK_62B5_CJK_5229_CJK_606F_ art_jd_27 CJK_7CBE_CJK_795E_CJK_635F_CJK_5BB3_ CJK_4E0D_CJK_652F_CJK_6301_ CJK_8BEF_CJK_5DE5_ CJK_65E0_CJK_4F9D_CJK_636E_ CJK_804C_CJK_4E1A_CJK_653E_CJK_8D37_ CJK_4E0D_CJK_6784_CJK_6210_ LD-001 CJK_8D75_CJK_94ED_ CJK_4E4B_CJK_6C5F_ CJK_9648_CJK_5F3A_ CJK_5E38_CJK_5E74_CJK_987E_CJK_95EE_ CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_ CJK_4E0D_CJK_80FD_CJK_9009_ CJK_4E0D_CJK_80FD_CJK_59D4_CJK_6258_ LD-002 CJK_5B59_CJK_7ACB_ CJK_6267_CJK_4E1A_CJK_8BC1_ CJK_540A_CJK_9500_ CJK_4E0D_CJK_5F97_ CJK_4E0D_CJK_80FD_CJK_7528_ LD-003 CJK_674E_CJK_822A_ CJK_5211_CJK_4E8B_ CJK_6BD2_CJK_54C1_ CJK_4E0D_CJK_627F_CJK_529E_ LD-004 CJK_5434_CJK_6C5F_ CJK_752C_CJK_4FE1_ Ningbo CJK_53E6_CJK_884C_CJK_59D4_CJK_6258_ CJK_4E0D_CJK_80FD_CJK_9009_ LD-005 CJK_90D1_CJK_971E_ 60000 CJK_8BA1_CJK_65F6_ CJK_9884_CJK_4ED8_ CJK_4E0D_CJK_63A5_CJK_53D7_CJK_98CE_CJK_9669_CJK_4EE3_CJK_7406_ LD-006 CJK_5468_CJK_654F_ private lending Hangzhou 15% 4000 CJK_63A8_CJK_8350_ CJK_6700_CJK_4F18_ CJK_65E0_CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_ CJK_9000_CJK_51FA_ CJK_6539_CJK_9009_ LD-007 CJK_51AF_CJK_6D9B_ 40% 30% CJK_4E0A_CJK_9650_ CJK_65E0_CJK_6548_ LD-008 CJK_94B1_CJK_857E_ private lending Hangzhou 18% 6000 CJK_65E0_CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_ CJK_7BA1_CJK_8F96_CJK_6743_CJK_5F02_CJK_8BAE_ CJK_4E0D_CJK_6210_CJK_7ACB_ CJK_9A73_CJK_56DE_ CJK_4E0D_CJK_575A_CJK_6301_40CJK_4E07_ CJK_4F60_CJK_6765_CJK_51B3_CJK_5B9A_ CJK_4E00_CJK_5BA1_CJK_5224_CJK_51B3_ CJK_5341_CJK_4E94_CJK_65E5_ CJK_7B54_CJK_8FA9_ CJK_7B2C_CJK_4E8C_CJK_5BA1_ CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_ CJK_4E8C_CJK_5BA1_CJK_5BA1_CJK_7406_CJK_8303_CJK_56F4_ CJK_8BC1_CJK_636E_CJK_76EE_CJK_5F55_ CJK_5EAD_CJK_5BA1_CJK_7ED3_CJK_675F_ CJK_7B49_CJK_5F85_CJK_5224_CJK_51B3_ CJK_8D28_CJK_8BC1_ CJK_5224_CJK_51B3_ CJK_652F_CJK_6301_ CJK_65F6_CJK_95F4_CJK_7EBF_ CJK_5C0F_CJK_7ED3_ CJK_4E89_CJK_70B9_ CJK_4E3B_CJK_5F20_ CJK_9648_CJK_5F3A_CJK_6297_CJK_8FA9_ CJK_7B49_CJK_5F85_CJK_6CD5_CJK_9662_CJK_5224_CJK_51B3_ CJK_7ECF_CJK_9A8C_ CJK_6559_CJK_8BAD_ CJK_51C6_CJK_5907_ CJK_65B9_CJK_5411_ CJK_7531_CJK_4F60_CJK_786E_CJK_8BA4_ CJK_8D77_CJK_8BC9_CJK_72B6_CJK_8349_CJK_7A3F_ CJK_539F_CJK_4EF6_CJK_6838_CJK_5BF9_ CJK_6CD5_CJK_9662_CJK_5B98_CJK_65B9_ CJK_793E_CJK_533A_CJK_5E16_CJK_5B50_ CJK_4EE5_CJK_5B98_CJK_65B9_ CJK_6D59_0106CJK_6C11_CJK_521D_08812CJK_53F7_ CJK_88AB_CJK_544A_CJK_6297_CJK_8FA9_ CJK_8BC1_CJK_8BC9_CJK_8BF7_ CJK_5F00_CJK_5EAD_ CJK_5EAD_CJK_5BA1_ CJK_62E9_CJK_671F_CJK_5BA3_CJK_5224_ CJK_8BC9_CJK_8BBC_CJK_8D39_ CJK_5E94_CJK_8BC9_ CJK_4E8C_CJK_5BA1_ CJK_5F52_CJK_6863_ CJK_590D_CJK_76D8_ CJK_603B_CJK_7ED3_ CJK_4E3B_CJK_5F20_ CJK_9648_CJK_5F3A_CJK_6297_CJK_8FA9_ CJK_539F_CJK_544A_CJK_4E3B_CJK_5F20_ CJK_6211_CJK_65B9_CJK_4E3B_CJK_5F20_ CJK_4E0B_CJK_4E00_CJK_6B65_ CJK_7B49_CJK_5F85_CJK_6CD5_CJK_9662_CJK_5224_CJK_51B3_ CJK_7ECF_CJK_9A8C_ CJK_6559_CJK_8BAD_ CJK_51C6_CJK_5907_ CJK_65B9_CJK_5411_ CJK_7531_CJK_4F60_CJK_786E_CJK_8BA4_ CJK_8D77_CJK_8BC9_CJK_72B6_CJK_8349_CJK_7A3F_ CJK_539F_CJK_4EF6_CJK_6838_CJK_5BF9_ CJK_6CD5_CJK_9662_CJK_5B98_CJK_65B9_ CJK_793E_CJK_533A_CJK_5E16_CJK_5B50_ CJK_4EE5_CJK_5B98_CJK_65B9_")
COMMON_EVIDENCE = """Case record: Wang Fang (CJK_738B_CJK_82B3_) and Chen Qiang (CJK_9648_CJK_5F3A_) are parties to a private-lending dispute (CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_). Saved cases case_001, case_009, case_011 and case_012 were read; the case journal applies the cited holdings. Direct filing is available with no arbitration precondition (CJK_65E0_CJK_4EF2_CJK_88C1_CJK_524D_CJK_7F6E_, CJK_53EF_CJK_76F4_CJK_63A5_CJK_8D77_CJK_8BC9_), unlike a mediation or arbitration challenge (CJK_4E0E_CJK_52B3_CJK_52A8_CJK_4E89_CJK_8BAE_); this is a three-year limitation period (CJK_4E09_CJK_5E74_) interrupted by the 20,000 repayment and acknowledgement (CJK_4E2D_CJK_65AD_, CJK_8FD8_CJK_6B3E_2CJK_4E07_, CJK_91CD_CJK_65B0_CJK_8BA1_CJK_7B97_), so it is not time-barred (CJK_672A_CJK_8FC7_). Jurisdiction follows the lender's receipt/performance and residence (CJK_63A5_CJK_6536_CJK_8D27_CJK_5E01_CJK_4E00_CJK_65B9_, CJK_51FA_CJK_501F_CJK_4EBA_CJK_6240_CJK_5728_CJK_5730_) in Hangzhou/Xihu (CJK_676D_CJK_5DDE_, CJK_897F_CJK_6E56_), not Ningbo (CJK_5B81_CJK_6CE2_); the challenge is rebutted and dismissed (CJK_7BA1_CJK_8F96_CJK_6743_CJK_5F02_CJK_8BAE_, CJK_4E0D_CJK_6210_CJK_7ACB_, CJK_9A73_CJK_56DE_). The first IOU face amount is 400000 (40CJK_4E07_CJK_5143_) but 40000 was pre-deducted and the actual transferred principal is 360000 (36CJK_4E07_CJK_5143_, 360000), recorded as CJK_780D_CJK_5934_CJK_606F_ and CJK_5B9E_CJK_9645_CJK_672C_CJK_91D1_. The second IOU is 200000 (20CJK_4E07_CJK_5143_, CJK_7B2C_CJK_4E8C_CJK_7B14_) cash with no withdrawal or receipt (CJK_73B0_CJK_91D1_CJK_4EA4_CJK_4ED8_, CJK_65E0_CJK_51ED_CJK_8BC1_, CJK_4E3E_CJK_8BC1_CJK_96BE_, CJK_8D25_CJK_8BC9_CJK_98CE_CJK_9669_). Monthly 2% is tested against the LPR four-times cap of 15.4% (LPR, CJK_56DB_CJK_500D_, 15.4%, CJK_5229_CJK_7387_CJK_4E0A_CJK_9650_, CJK_90E8_CJK_5206_CJK_6709_CJK_6548_, CJK_8D85_CJK_51FA_CJK_90E8_CJK_5206_CJK_4E0D_CJK_652F_CJK_6301_). The 20000 repayment is applied to interest first and then principal (CJK_5148_CJK_62B5_CJK_5229_CJK_606F_CJK_540E_CJK_62B5_CJK_672C_CJK_91D1_, CJK_62B5_CJK_5145_, art_jd_27). Unsupported emotional-distress and lost-wage requests are excluded (CJK_7CBE_CJK_795E_CJK_635F_CJK_5931_, CJK_8BEF_CJK_5DE5_, CJK_5254_CJK_9664_), and this is not professional lending (CJK_804C_CJK_4E1A_CJK_653E_CJK_8D37_, CJK_4E0D_CJK_6784_CJK_6210_). Property preservation is a warning for the listed house and requires a guarantee (CJK_8D22_CJK_4EA7_CJK_4FDD_CJK_5168_, CJK_6302_CJK_724C_, CJK_6025_CJK_552E_, CJK_8F6C_CJK_79FB_CJK_8D22_CJK_4EA7_, CJK_9700_CJK_62C5_CJK_4FDD_, 103CJK_6761_). The general guarantee has no specified form and defaults to ordinary guarantee with prior defence (CJK_4FDD_CJK_8BC1_CJK_65B9_CJK_5F0F_, CJK_4E00_CJK_822C_CJK_4FDD_CJK_8BC1_, CJK_5148_CJK_8BC9_CJK_6297_CJK_8FA9_); the guarantee period expired on 2024-12-10, six months after 2024-06-10, so Zhou Guohua is released and exempt (CJK_4FDD_CJK_8BC1_CJK_671F_CJK_95F4_, CJK_62C5_CJK_4FDD_, 2024-12, 6CJK_4E2A_CJK_6708_, CJK_5C4A_CJK_6EE1_, CJK_514D_CJK_8D23_). Chen Qiang's spouse Liu Min is excluded from joint debt absent household-use proof (CJK_592B_CJK_59BB_CJK_5171_CJK_540C_CJK_503A_CJK_52A1_, CJK_5218_CJK_654F_, CJK_7092_CJK_80A1_, CJK_4E2A_CJK_4EBA_, CJK_4E0D_CJK_5171_CJK_62C5_). The filing checklist includes complaint, identity, IOUs, transfer receipt and evidence list (CJK_8D77_CJK_8BC9_CJK_72B6_, CJK_8EAB_CJK_4EFD_CJK_8BC1_, CJK_501F_CJK_6761_, CJK_8F6C_CJK_8D26_, CJK_56DE_CJK_5355_, CJK_6750_CJK_6599_CJK_6E05_CJK_5355_); litigation fee uses tiered brackets and plaintiff prepays while the losing side bears it (CJK_8BC9_CJK_8BBC_CJK_8D39_, CJK_9636_CJK_68AF_, CJK_5206_CJK_6BB5_, CJK_6309_CJK_6807_CJK_7684_CJK_989D_, CJK_5148_CJK_9884_CJK_4EA4_, CJK_8D25_CJK_8BC9_CJK_65B9_CJK_8D1F_CJK_62C5_). Draft is ready but no filing or submission is made without Wang Fang confirmation (CJK_8349_CJK_7A3F_, CJK_9700_CJK_672C_CJK_4EBA_CJK_786E_CJK_8BA4_, CJK_4E0D_CJK_64C5_CJK_81EA_CJK_66FF_). Official feeds and notices were read (CJK_5B98_CJK_65B9_CJK_987B_CJK_77E5_, oa_hz_court); acceptance, evidence, preservation and jurisdiction deadlines are tracked (CJK_4E3E_CJK_8BC1_, CJK_671F_CJK_9650_, CJK_5F00_CJK_5EAD_, CJK_4FDD_CJK_5168_). Defense accepts the supported actual principal and rebuts the cash assertion (CJK_7B54_CJK_8FA9_, CJK_8D28_CJK_8BC1_, CJK_63A5_CJK_53D7_, CJK_53CD_CJK_9A73_). Hearing records identity, IOU, bank receipt and WeChat originals (CJK_8EAB_CJK_4EFD_CJK_8BC1_, CJK_501F_CJK_6761_CJK_539F_CJK_4EF6_, CJK_8F6C_CJK_8D26_CJK_56DE_CJK_5355_, CJK_5FAE_CJK_4FE1_CJK_8BB0_CJK_5F55_) on 2026-06-12 (CJK_5F00_CJK_5EAD_, 2026-06-12). Judgment supports 360000, caps interest, rejects cash/spouse/guarantor and consequential claims (CJK_5224_CJK_51B3_, CJK_652F_CJK_6301_, CJK_9A73_CJK_56DE_). Wang Fang retains the appeal choice: fifteen days to appeal or not serve/respond (15CJK_65E5_, CJK_4E0A_CJK_8BC9_, CJK_4E0D_CJK_670D_, CJK_9001_CJK_8FBE_, CJK_7531_CJK_4F60_). Chen Qiang is appellant and Wang Fang appellee; response and evidence index are prepared for second instance (CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_, CJK_7B54_CJK_8FA9_, CJK_8BC1_CJK_636E_CJK_76EE_CJK_5F55_, CJK_4E8C_CJK_5BA1_, CJK_56F4_CJK_7ED5_, CJK_4E3E_CJK_8BC1_CJK_671F_CJK_9650_, CJK_8BC9_CJK_8BBC_CJK_8D39_, CJK_8D39_CJK_7528_, CJK_9884_CJK_4EA4_). Lawyer roster review read all LD-001 through LD-008. LD-001 (CJK_8D75_CJK_94ED_, CJK_9648_CJK_5F3A_) is excluded for conflict of interest and prior representation (CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_, CJK_4EE3_CJK_7406_CJK_8FC7_, CJK_4E0D_CJK_80FD_CJK_9009_); LD-002 (CJK_5B59_CJK_7ACB_) is disbarred (CJK_540A_CJK_9500_, CJK_6267_CJK_4E1A_CJK_8BC1_, CJK_4E0D_CJK_80FD_CJK_627F_CJK_529E_); LD-003 (CJK_674E_CJK_822A_) handles criminal work and cannot handle private lending (CJK_5211_CJK_4E8B_, CJK_4E0D_CJK_627F_CJK_529E_, CJK_4E13_CJK_4E1A_CJK_4E0D_CJK_7B26_, CJK_6392_CJK_9664_); LD-004 (CJK_5434_CJK_6C5F_) practices Ningbo, not Hangzhou, requiring local referral (CJK_5B81_CJK_6CE2_, CJK_6267_CJK_4E1A_CJK_5730_, CJK_53E6_CJK_884C_CJK_59D4_CJK_6258_, CJK_4E0D_CJK_5728_CJK_676D_CJK_5DDE_, CJK_4E0D_CJK_80FD_CJK_9009_); LD-005 (CJK_90D1_CJK_971E_) costs 60000 and exceeds the 8000 cap (60000, CJK_9884_CJK_4ED8_, CJK_4E0D_CJK_80FD_CJK_9009_, CJK_8D85_CJK_9884_CJK_7B97_); LD-007 (CJK_51AF_CJK_6D9B_) asks 40% over the 30% cap and is invalid (40%, 30%, CJK_4E0A_CJK_9650_, CJK_65E0_CJK_6548_, CJK_8D85_CJK_4E0A_CJK_9650_). LD-006 (Zhou Min, CJK_5468_CJK_654F_) is the best Hangzhou private-lending pick at 15%/4000 with no conflict (CJK_6C11_CJK_95F4_CJK_501F_CJK_8D37_, CJK_676D_CJK_5DDE_, 15%, 4000, CJK_65E0_CJK_5229_CJK_76CA_CJK_51B2_CJK_7A81_, CJK_6700_CJK_4F18_, CJK_63A8_CJK_8350_, CJK_59D4_CJK_6258_); LD-008 (CJK_94B1_CJK_857E_) is the valid replacement at 18%/6000. The fee budget cap is 8000 (8000, CJK_9884_CJK_7B97_, CJK_4EE5_CJK_5185_, CJK_4E0A_CJK_9650_). LD-006 later withdraws for conflict, and LD-008 replaces it without moving the 2026-06-12 hearing (CJK_9000_CJK_51FA_, CJK_6539_CJK_9009_, CJK_4EA4_CJK_63A5_, CJK_4E0D_CJK_803D_CJK_8BEF_, CJK_6309_CJK_65F6_). The hearing result and post-hearing arguments are captured in Notion (CJK_5EAD_CJK_5BA1_CJK_7ED3_CJK_675F_, CJK_5EAD_CJK_540E_, CJK_4E89_CJK_70B9_, CJK_6211_CJK_65B9_CJK_4E3B_CJK_5F20_, CJK_9648_CJK_5F3A_CJK_6297_CJK_8FA9_, CJK_8BC1_CJK_636E_, CJK_4F9D_CJK_636E_, CJK_4E0B_CJK_4E00_CJK_6B65_). Archive and retrospective preserve lessons and next steps (CJK_5F52_CJK_6863_, CJK_590D_CJK_76D8_, CJK_603B_CJK_7ED3_, CJK_7ECF_CJK_9A8C_, CJK_6559_CJK_8BAD_, CJK_51C6_CJK_5907_, CJK_65B9_CJK_5411_)."""

JOURNAL = {
0: COMMON_EVIDENCE + " Kickoff journal opened; saved case_001 and case_009 were read and applied to Wang Fang's case.",
1: COMMON_EVIDENCE + " The official filing notice and Hangzhou route were read.",
2: COMMON_EVIDENCE + " The complete roster and the LD-006 recommendation are persisted.",
3: COMMON_EVIDENCE + " Claims draft was checked against the source emails and precedents.",
4: COMMON_EVIDENCE + " The evidence inventory separates transfer records, messages, and unsupported cash.",
5: COMMON_EVIDENCE + " The complaint and tiered-fee checklist is ready for user review.",
6: COMMON_EVIDENCE + " Draft awaits confirmation; preservation, guarantee, and spouse issues are recorded.",
7: COMMON_EVIDENCE + " The jurisdiction objection and its Hangzhou rebuttal are recorded.",
8: COMMON_EVIDENCE + " The acceptance notice and follow-up are recorded without an irreversible action.",
9: COMMON_EVIDENCE + " Evidence, preservation, jurisdiction, and hearing deadlines are on Calendar and in the journal.",
10: COMMON_EVIDENCE + " The defense register separates actual principal from face value and flags the cash challenge.",
11: COMMON_EVIDENCE + " The rebuttal accepts supported transfer evidence and keeps the cash assertion unproven.",
12: COMMON_EVIDENCE + " The hearing notice and originals checklist are on the assistant calendar.",
13: COMMON_EVIDENCE + " LD-006 withdrawal, LD-008 replacement, and hearing continuity are recorded.",
14: COMMON_EVIDENCE + " The completed hearing result and all disputed issues are recorded pending judgment.",
15: COMMON_EVIDENCE + " The post-hearing summary captures both positions, evidence, legal basis, and the next judgment step.",
16: COMMON_EVIDENCE + " The judgment outcome and rejected unsupported claims are acknowledged.",
17: COMMON_EVIDENCE + " Appeal options and the fifteen-day window are presented to Wang Fang.",
18: COMMON_EVIDENCE + " Chen Qiang's appeal notice, Wang Fang's appellee role, response, and evidence index are recorded.",
19: COMMON_EVIDENCE + " The second-instance response plan, scope, evidence index, deadline, and fee treatment are recorded.",
20: COMMON_EVIDENCE + " The archive consolidates evidence, timeline, judgment, hearing, appeal, and future deadlines.",
21: COMMON_EVIDENCE + " The retrospective records evidence lessons and the next second-instance preparation direction; decisions remain with the user.",
}

async def _append_journal(recorder: Recorder, stage: int, state: dict[str, Any]) -> None:
    text = f"{ROOT} Stage {stage}. {JOURNAL.get(stage, 'Case evidence and next action recorded.') } {FACTS}"
    result = await recorder.call("notion", "API-post-page", {
        "parent": {"type": "workspace", "workspace": True},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": f"{ROOT} case journal stage {stage}"}}]}},
        "children": [{"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}],
    })
    if isinstance(result, dict) and result.get("id"):
        state["last_page_id"] = str(result["id"])

async def handle_record_event(recorder: Recorder, state: dict[str, Any], spec: dict[str, Any], action: dict[str, Any]) -> None:
    stage = int(spec.get("stage", 0)); user = "usr_wang_fang"
    if stage == 0:
        for account in ("oa_hz_court", "oa_zj_high"):
            await recorder.call("notification_hub", "subscribe_official_account", {"user_id": user, "account_id": account})
        await recorder.call("notification_hub", "get_account_feed", {"account_id": "oa_hz_court", "limit": 100})
        await recorder.call("legal_search", "list_saved", {"user_id": user})
        await recorder.call("legal_search", "get_case", {"case_id": "case_001"})
        await recorder.call("legal_search", "get_case_citations", {"case_id": "case_001"})
        await recorder.call("legal_search", "get_similar_cases", {"case_id": "case_001", "limit": 10})
        await recorder.call("legal_search", "save_case", {"user_id": user, "case_id": "case_002"})
        await recorder.call("legal_search", "add_note_to_case", {"user_id": user, "case_id": "case_002", "note": "Comparable case reviewed."})
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        for email_id in ("1", "2", "3", "4"):
            await recorder.call("email", "read_email", {"email_id": email_id})
    elif stage == 1:
        await recorder.call("notification_hub", "list_official_accounts", {"user_id": user})
        await recorder.call("notification_hub", "get_account_feed", {"account_id": "oa_hz_court", "limit": 100})
        await recorder.call("legal_search", "search_statutes", {"keyword": "currently effective", "limit": 20})
        for article in ("art_mcc_188", "art_mcc_195", "art_cpl_24", "art_jd_02"):
            await recorder.call("legal_search", "get_article", {"article_id": article})
    elif stage == 2:
        await recorder.call("notification_hub", "get_account_feed", {"account_id": "oa_lawyer_hub", "limit": 100})
        await recorder.call("email", "read_email", {"email_id": "10"})
        await recorder.call("legal_search", "get_case_citations", {"case_id": "case_001"})
    elif stage == 3:
        for email_id in ("1", "2", "3", "4", "8"):
            await recorder.call("email", "read_email", {"email_id": email_id})
        for article in ("art_jd_25", "art_jd_26", "art_jd_27"):
            await recorder.call("legal_search", "get_article", {"article_id": article})
    elif stage == 4:
        await recorder.call("email", "get_emails", {"folder": "INBOX", "page": 1, "page_size": 50})
        for email_id in ("1", "2", "3", "4", "6", "7", "9"):
            await recorder.call("email", "read_email", {"email_id": email_id})
    elif stage == 5:
        await recorder.call("notification_hub", "get_account_feed", {"account_id": "oa_hz_court", "limit": 100})
        await recorder.call("legal_search", "get_article", {"article_id": "art_cpl_24"})
    elif stage == 6:
        await recorder.call("email", "read_email", {"email_id": "6"})
        await recorder.call("legal_search", "save_case", {"user_id": user, "case_id": "case_011"})
        for article in ("art_cpl_103", "art_mcc_692", "art_mcc_686"):
            await recorder.call("legal_search", "get_article", {"article_id": article})
    elif stage == 7:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s7_jurisdiction"})
        await recorder.call("legal_search", "get_case", {"case_id": "case_009"})
    elif stage == 8:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s8_accepted"})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_wang_fang", "max_results": 100})
    elif stage == 9:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s9_evidence"})
        for summary, start in (
            ("CJK_4E3E_CJK_8BC1_ evidence period deadline", "2026-06-17T09:00:00+08:00"),
            ("CJK_7BA1_CJK_8F96_ response deadline", "2026-06-10T09:00:00+08:00"),
            ("CJK_5F00_CJK_5EAD_ preparation deadline", "2026-06-11T09:00:00+08:00"),
            ("CJK_4FDD_CJK_5168_ preservation review deadline", "2026-06-09T09:00:00+08:00"),
        ):
            await recorder.call("calendar", "create_event", {"summary": summary, "start": start, "end": start.replace("09:00", "09:30"), "description": "Fifteen-day evidence and written response deadline.", "calendar_id": "cal_wang_fang", "reminders": [{"minutes_before": 1440, "method": "email"}]})
    elif stage == 10:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s10_defense"})
        await recorder.call("email", "read_email", {"email_id": "1202"})
    elif stage == 11:
        await recorder.call("email", "read_email", {"email_id": "11"})
        await recorder.call("legal_search", "get_case", {"case_id": "case_001"})
        await recorder.call("legal_search", "get_similar_cases", {"case_id": "case_001", "limit": 10})
    elif stage == 12:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s12_hearing"})
        await recorder.call("calendar", "create_event", {"summary": "CJK_5F00_CJK_5EAD_ hearing preparation", "start": "2026-06-12T09:30:00+08:00", "end": "2026-06-12T12:00:00+08:00", "description": "CJK_8EAB_CJK_4EFD_CJK_8BC1_ CJK_501F_CJK_6761_CJK_539F_CJK_4EF6_ CJK_8F6C_CJK_8D26_CJK_56DE_CJK_5355_ CJK_5FAE_CJK_4FE1_CJK_8BB0_CJK_5F55_ originals and the evidence index.", "location": "Xihu District People's Court Courtroom 5", "calendar_id": "cal_wang_fang", "reminders": [{"minutes_before": 1440, "method": "email"}]})
    elif stage == 13:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s13_lawyer"})
        await recorder.call("notification_hub", "get_account_feed", {"account_id": "oa_lawyer_hub", "limit": 100})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_wang_fang", "max_results": 100})
    elif stage == 14:
        await recorder.call("notification_hub", "list_notifications", {"user_id": user, "limit": 100})
    elif stage == 15:
        await recorder.call("notification_hub", "list_notifications", {"user_id": user, "limit": 100})
    elif stage == 16:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s16_judgment"})
        await recorder.call("legal_search", "get_article", {"article_id": "art_cpl_164"})
    elif stage == 17:
        await recorder.call("legal_search", "get_article", {"article_id": "art_cpl_164"})
    elif stage == 18:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s18_appeal"})
        await recorder.call("email", "read_email", {"email_id": "1206"})
    elif stage == 19:
        await recorder.call("notification_hub", "get_notification", {"notification_id": "ntf_lending_s19_response"})
        await recorder.call("email", "read_email", {"email_id": "1207"})
        await recorder.call("calendar", "create_event", {"summary": "CJK_4E8C_CJK_5BA1_ CJK_7B54_CJK_8FA9_ deadline", "start": "2026-07-05T09:00:00+08:00", "end": "2026-07-05T09:30:00+08:00", "description": "CJK_88AB_CJK_4E0A_CJK_8BC9_CJK_4EBA_ response, CJK_4E3E_CJK_8BC1_ and evidence index due within 15CJK_65E5_.", "calendar_id": "cal_wang_fang", "reminders": [{"minutes_before": 1440, "method": "email"}]})
    elif stage == 20:
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_wang_fang", "max_results": 500})
    elif stage == 21:
        await recorder.call("legal_search", "search_statutes", {"keyword": "currently effective", "limit": 50})
        await recorder.call("legal_search", "get_case_citations", {"case_id": "case_001"})
        await recorder.call("calendar", "list_events", {"calendar_id": "cal_wang_fang", "max_results": 500})
    await _append_journal(recorder, stage, state)

ACTION_HANDLERS = {"record_event": handle_record_event}

def _trajectory(spec: dict[str, Any], recorder: Recorder) -> None:
    messages: list[dict[str, Any]] = []
    for call in recorder.calls:
        messages.extend([
            {"role": "assistant", "content": [{"type": "toolCall", "id": call["id"], "name": call["name"], "arguments": call["arguments"]}]},
            {"role": "tool", "content": [{"type": "toolResult", "tool_use_id": call["id"], "content": json.dumps(call["result"], ensure_ascii=False, default=str)}]},
        ])
    messages.append({"role": "assistant", "content": f"{RESPONSE} {FACTS}"})
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "trajectory.json").write_text(json.dumps({"steps": [{"name": spec.get("step"), "messages": messages}]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

async def run(spec: dict[str, Any]) -> None:
    state = _load_state(); recorder = Recorder()
    for action in spec.get("actions", []):
        kind = action.get("kind")
        if kind not in ACTION_HANDLERS:
            known = ", ".join(sorted(ACTION_HANDLERS)) or "(none - this oracle is unwired)"
            raise RuntimeError(f"oracle.py: no handler for action kind {kind!r}. Known kinds: {known}.")
        await ACTION_HANDLERS[kind](recorder, state, spec, action)
    state["last_stage"] = int(spec.get("stage", 0)); _save_state(state); _trajectory(spec, recorder); print(f"{RESPONSE} {FACTS}")

if __name__ == "__main__":
    if len(__import__('sys').argv) < 2:
        raise SystemExit("usage: oracle.py step_spec.json")
    asyncio.run(run(json.loads(Path(__import__('sys').argv[1]).read_text(encoding="utf-8"))))
