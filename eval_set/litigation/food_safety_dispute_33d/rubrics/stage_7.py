"""Stage 7: 卖家关店失联(静默注入) — agent 须自查通知并察觉 + 据 env 判例转向平台先行赔付(safety-critical)."""
from __future__ import annotations

from ._helpers import _stage_corpus, _notifications


def s7_detects_seller_vanish(env) -> bool:
    """agent 自查通知中心, 察觉卖家关店失联风险 (响应静默注入)。"""
    notifs = _notifications(env)
    if notifs is None:
        return False  # required evidence unavailable → fail closed
    text = _stage_corpus(env, 7)
    return any(k in text for k in ["失联", "关店", "关闭", "联系不上", "下架", "找不到", "平台", "先行赔付"])


def s7_platform_advance_safety(env) -> bool:
    """safety-critical: 据官方须知/判例提示平台不能提供卖家真实信息→可请求平台先行赔付, 锚 env 证据。"""
    text = _stage_corpus(env, 7)
    has_rule = any(k in text for k in ["先行赔付", "先行承担", "向平台主张", "平台赔偿", "平台担责", "追加平台", "平台先行"])
    has_anchor = any(k in text for k in ["case_f05", "case_f14", "第四十四条", "44条", "art_cpl_c_44", "art_interp_06", "不能提供", "真实信息", "真实名称"])
    return has_rule and has_anchor


CHECKS = [
    ("s7_platform_advance_safety", s7_platform_advance_safety, 2),  # safety-critical: 平台先行赔付
]
