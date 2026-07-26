"""Stage 2 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s2_servers(env) -> bool:
    """L1 调用正确：stage 2 至少命中 2 个期望 MCP server（交叉查询，不靠记忆）。

    证据维度：🔧工具调用
    """
    if not H._stage_servers_correct(env, 2, min_count=2):
        return False
    return True


def s2_args(env) -> bool:
    """L2 参数正确：stage 2 的工具入参引用了正确的订单/卡/挂牌等实体。

    证据维度：🔧工具调用
    """
    return H._stage_tool_args_reference(env, 2, ['prod_strr_main', 'sku_strr_main', 'ord_strr_0001', 'oa_strr_brand'], min_count=2)


def s2_result(env) -> bool:
    """[后端锚定·批次核验] 线1安全核验必须写出「只有真读商城 SKU attrs 才知道」的具体
    生产批次号 GBS5-2026-03（+ 验证编号 VRF-STRR-3M6693），而不是泛泛写"召回/批次"关键词；
    并用 ecommerce get_product 后端核对该批次确实存在于 prod_strr_main 的 SKU attrs。

    两值性：workspace 必须含具体批次号（缺→False）；后端可达时批次须匹配（不匹配→False），
    后端不可达→宽松（None→放行该子条件）。杜绝"提到召回即得分"。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    text = H.scoped_text(env, ['tracker', 'decision', 'risk', 'gear'], idx=2)
    # 语义要素（安全标准/召回处置）——保留但降为门槛之一，不再是全部
    themes = H._count_any(text, ['召回', '批次', '制动', '安全带', '标准', '换新', '退货']) >= 3
    # 具体真值 token：批次号 + 验证编号（二者都要，强制真读 SKU attrs 逐字誊写）
    wrote_batch = H._count_any(text, ['gbs5-2026-03']) >= 1
    wrote_vcode = H._count_any(text, ['vrf-strr-3m6693']) >= 1
    if not (themes and wrote_batch and wrote_vcode):
        return False
    # 后端核对：商城真实 SKU attrs 里的 batch == GBS5-2026-03（不可达→None→宽松放行）
    verified = H._backend_batch_verified(env, 'prod_strr_main', 'GBS5-2026-03')
    return bool(verified)


def s2_options(env) -> bool:
    """多组关键词都要分别命中（既要 A 又要 B …），缺任一组判 0。

    证据维度：📝持久化 💬回复
    """
    text = H.scoped_text(env, ['gear', 'decision', 'tracker'], idx=2)
    return (
        H._count_any(text, ['召回换新', '加固制动', '退货', '免费换新']) >= 2
        and H._count_any(text, ['0', '120', '600', '免费']) >= 2
        and H._count_any(text, ['上门', '就近', '周期', '方便']) >= 2
    )


CHECKS = guard_stage_checks(2, [
    ("s2_servers", s2_servers, 0.5),
    ("s2_args", s2_args, 1.0),
    ("s2_result", s2_result, 2.0),
    ("s2_options", s2_options, 2.0),
])
