"""Stage 8 checks — 原子 Checker 定义与权重均位于本模块。"""
from __future__ import annotations

from ._helpers import guard_stage_checks
from . import _helpers as H

def s8_table(env) -> bool:
    """多组关键词都要分别命中（既要 A 又要 B …），缺任一组判 0。

    证据维度：📝持久化 💬回复
    """
    text = H.scoped_text(env, ['gear', 'decision', 'budget'], idx=8)
    return (
        H._count_any(text, ['trade-in', '以旧换新', '二手']) >= 2
        and H._count_any(text, ['到手价', '时效', '风险', '平台担保', '全家出行日', '时间']) >= 4
    )


def s8_optimal(env) -> bool:
    """[最优解·后端精确对账] 最省凑单方案四绑：
      ① 台账写出选中方案名（凑单/满减/FULL209）与推荐结论；
      ② 台账写出「推导得到的」精确总价数字（券后 ¥209.00 = 20900 分，或含 ¥8 运费的到手价 ¥217.00）；
      ③ 未授权不得擅自下单（无"已下单/已付款"既成事实话术）；
      ④ 后端购物车真实终态：恰好含三档各自最便宜款 {bsk_strr_a3, bsk_strr_b2, bsk_strr_c3}，
         且 subtotal_minor 精确 == 23900，且券后 total_minor 精确 == 20900（凑单池行不得多不得少）。
    仅"提到方案"不够——购物车必须真的装对组合、金额必须精确对齐。

    两值性：①②③ 任一缺→False；④ 后端可达时必须精确匹配（错组合/错金额→False），
    后端不可达→None→宽松放行（仅④这一子条件）。杜绝 dead-True。

    证据维度：🗄后端终态 📝持久化 💬回复
    """
    text = H.files_text(env, ['gear', 'decision', 'budget']).lower()
    named = H._count_any(text, ['凑单', '满减', 'full209']) >= 1
    # 精确总价：券后 209（¥209.00）或含运费到手 217（¥217.00）——须为推导所得，env 不泄露
    priced = H._count_any(text, ['209', '20900', '217', '21700']) >= 1
    chosen = H._count_any(text, ['最省', '最划算', '最低总价', '推荐', '选定']) >= 1
    if not (named and priced and chosen):
        return False
    if H._has_bad_advice(text, ['已经下单', '直接买了', '替你下单', '已付款', '已结算']):
        return False
    # 后端终态：购物车恰含最省三件 + 精确金额（不可达→None→宽松放行）
    state = H._backend_cart_matches_optimal(
        env, 'usr_yan_ting',
        ['bsk_strr_a3', 'bsk_strr_b2', 'bsk_strr_c3'],
        subtotal_minor=23900,
        total_minor=20900,
    )
    return bool(state)


CHECKS = guard_stage_checks(8, [
    ("s8_table", s8_table, 4.0),
    ("s8_optimal", s8_optimal, 3.0),
])
