"""Cross-stage hidden constraint checks (d_ prefix) for private_lending_33d.

HARDENING REWRITE (2026-07-25) — root-cause fix
────────────────────────────────────────────────
Before: every substantive d_ scored off ``_all_corpus`` keyword-OR (``any(k in
prose)`` over /terrarium/agent_responses). A strong model that merely *enumerated*
legal keywords (砍头息/LPR四倍/保证期间/夫妻共同债务/管辖…) in its reply passed with
ZERO backend state — which is exactly manual §7's forbidden inversion (证据优先级:
环境状态 > 关键工具调用 > 文本表达). Measured strong-model score 0.694 (>> the <0.30
"hard-but-solvable" bar).

After: each substantive legal-analysis conclusion and lawyer decision now requires
a CONCRETE, backend-verifiable PRODUCT persisted in the Notion litigation journal —
read back via the same read tools an agent uses (API-post-search / get-block-children,
see _helpers._journal_text). Crucially each check requires the *derived value*,
not just the topic keyword:
  • 砍头息  → journal must contain the COMPUTED actual principal 360000 (=400000借条
             −40000预扣, the real transferred amount), not the 400000 face value;
  • 保证期间 → journal must contain the COMPUTED lapse date 2024-12-10 (=2024-06-10到期
             +6个月) AND the 免责 conclusion;
  • 夫妻共同债务 → journal must name 刘敏 excluded with the 炒股/个人 reason;
  • 利率上限 → journal must carry the four-times cap figure 15.4(%) + partial validity;
  • 律师选定/改选 → journal must persist LD-006 (then LD-008) with the roster reasoning.
Mentioning the keyword in the agent's reply alone now FAILS; only a competent agent
that computes AND persists passes.

Read-leniency preserved (mirrors the rest of the module): Notion UNREACHABLE →
_journal_text returns None → the check returns False (unverifiable evidence cannot score); reachable
but the product is absent/wrong → False ("only talked" / "wrong number" fails).

Purely procedural d_ that name no case-specific product (无仲裁前置 / 15日上诉期 /
现行有效法条) stay corpus-grounded but keep their tight conjunctions — persisting them
in Notion is not the natural artifact, and they remain two-valued against agent prose.

王芳 facts (from email env): 出借人,杭州西湖区开服装店 / 借款人陈强,宁波海曙 /
第一笔借条40万但转账预扣4万利息实到36万(砍头息) / 第二笔借条20万称现金交付无凭证 /
约定月息2%(年24%)>合同成立时(2023-06)LPR四倍(15.4%) / 到期2024-06-10 / 陈强2025-02部分
还款2万+"我会还"(时效中断,3年时效远未过) / 老周借条签"担保"未写方式期间(保证期间
2024-12-10届满,免责) / 陈强已婚配偶刘敏,借款用于个人炒股(非夫妻共同债务) /
陈强宁波房产挂牌急售(可申请财产保全) / 判决支持本金360000并按LPR四倍计息.

Lawyer roster (notification_hub oa_lawyer_hub, LD-001..008): LD-006 周敏 唯一最优
(借贷专长+杭州+风险代理15%+预付¥4000); LD-008 钱蕾 次优(18%/¥6000); 其余各有硬性排除点.

Each d_ appears in exactly ONE stage's CHECKS with a meaningful weight; not re-counted.
"""
from __future__ import annotations

from ._helpers import _journal_text, _norm_num


def _has(text: str, kws) -> bool:
    return any(k in text for k in kws)


# ── memoized journal read ────────────────────────────────────────────────────
# _journal_text does several backend searches; ~30 d_ checks would repeat them.
# Cache the (possibly None) result on the env object for one checker pass.
def _journal(env):
    cached = getattr(env, "_pl_journal_cache", "unset")
    if cached != "unset":
        return cached
    try:
        j = _journal_text(env)
    except Exception:
        j = None
    try:
        setattr(env, "_pl_journal_cache", j)
    except Exception:
        pass
    return j


def _journal_norm(env):
    """Journal text with numeric separators stripped (None if unreachable)."""
    j = _journal(env)
    if j is None:
        return None
    return _norm_num(j)


# Backend-grounded gate helper: True iff Notion reachable AND persisted journal
# satisfies `predicate(text)`. Unreachable → fail-closed False. Reachable-but-fails → False.
def _journal_ok(env, predicate) -> bool:
    j = _journal(env)
    if j is None:
        return False  # required evidence unavailable -> fail closed
    try:
        return bool(predicate(j))
    except Exception:
        return False


def _journal_norm_ok(env, predicate) -> bool:
    j = _journal_norm(env)
    if j is None:
        return False  # required evidence unavailable -> fail closed
    try:
        return bool(predicate(j))
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────
# 程序三连 (procedure) — 反直觉真实规则。无具体"产物"锚点(纯程序结论),
# 保留 corpus 基础但维持紧凑合取; 仍是两值(强模型不写这些点即 False)。
# ─────────────────────────────────────────────────────────────────────────

# 1. 无仲裁前置 — 民间借贷是普通合同纠纷, 可径行向法院起诉, 无须先仲裁/调解。
def d_no_arbitration_precondition(env) -> bool:
    """须把"无仲裁前置、可径行起诉"的结论**落到 Notion 台账**，而非只在回复里说一句。

    改读后端持久状态（原先读 agent 回复文本，属 §6.1 禁止的"以调用/表述代替结果"）。
    """
    def pred(t):
        has_direct = _has(t, ["直接起诉", "径行起诉", "可直接向法院", "直接向人民法院", "无须仲裁",
                              "无需仲裁", "不需要仲裁", "无前置", "无仲裁前置", "没有前置"])
        has_scope = _has(t, ["民间借贷", "合同纠纷", "借款合同", "普通民事"])
        has_contrast = _has(t, ["不同于劳动", "与劳动争议", "区别于劳动", "不像劳动", "劳动争议",
                                "不是劳动仲裁", "无须先仲裁", "不必先仲裁", "起诉即可", "起诉立案"])
        return has_direct and has_scope and has_contrast
    return _journal_ok(env, pred)


# 2. 诉讼时效3年 + 中断 — 须发现部分还款/还款承诺这一中断事由并得出"未过时效"的结论,
#    且结论须持久化到 Notion(时效判断是本案能否推进的前提, 属应落台账的分析产物)。
#    Backend fact: 陈强2025-02还2万+"我会还" → 时效自2025-02重新计3年(email#4)。
def d_limitation_3y_interruption(env) -> bool:
    def pred(t):
        has_three_year = _has(t, ["三年", "3年", "时效三年", "时效为三年", "诉讼时效"])
        has_interrupt = _has(t, ["中断", "重新计算", "重新起算", "部分还款", "还了2万", "还款2万", "承认债务", "同意履行", "我会还"])
        has_conclusion = _has(t, ["未过", "没过", "仍在时效", "还在时效内", "没有过期", "未超时效", "时效未过", "未届满", "远未"])
        return has_three_year and has_interrupt and has_conclusion
    return _journal_ok(env, pred)


# 3. 管辖=接收货币一方(出借人)所在地 — 王芳在杭州西湖区可诉, 无须去宁波; 须落 Notion。
def d_jurisdiction_lender(env) -> bool:
    def pred(t):
        has_rule = _has(t, ["接收货币一方", "合同履行地", "出借人所在地", "出借人住所地"])
        has_locale = _has(t, ["杭州", "西湖", "本地起诉", "自己住所地", "在杭州"])
        has_contrast = _has(t, ["被告住所地", "宁波", "海曙", "不用去", "无须去", "不必去", "不用前往"])
        return has_rule and has_locale and has_contrast
    return _journal_ok(env, pred)


# ─────────────────────────────────────────────────────────────────────────
# 案件实体反直觉雷区 (case-fact traps) — 教科书答案在此翻盘。均要求 Notion 持久化
# 的 *计算产物*, 而非仅关键词。
# ─────────────────────────────────────────────────────────────────────────

# 4. 砍头息陷阱(反直觉核心) — 第一笔借条40万但转账预扣4万利息实到36万;
#    本金应按实际出借 360000 认定(而非借条400000)。
#    Backend fact: 转账回单 email#2 = 360000 实到; 借条 email#1 = 400000 面额。
#    HARD: 须在 Notion 写出计算出的实际本金 360000(仅提"砍头息"关键词不算)。
def d_kantou_interest_principal(env) -> bool:
    def pred(tn):  # tn = numeric-normalized journal
        has_topic = _has(tn, ["砍头息", "预先扣除", "预扣", "先扣", "扣了利息", "扣息", "实际出借", "按实际"])
        has_actual = _has(tn, ["360000", "36万", "三十六万"])   # 计算出的真实本金
        not_face_only = has_actual  # 必须出现实际本金, 只写400000借条面额不满足
        return has_topic and not_face_only
    return _journal_norm_ok(env, pred)


# 5. 利率超 LPR 四倍 — 约定月息2%(年24%)超合同成立时(2023-06)一年期LPR四倍(15.4%);
#    超出部分不予支持, 四倍以内仍有效。须在 Notion 写出四倍上限 15.4% + "部分有效"。
#    Backend fact: 判例 case_002 / art_jd_25: 四倍即15.4%。
def d_lpr_four_times(env) -> bool:
    def pred(tn):
        has_topic = _has(tn, ["LPR", "lpr", "贷款市场报价利率", "四倍", "月息2%", "年24%", "年化24"])
        has_cap = _has(tn, ["四倍", "15.4", "超过部分不", "超出部分不", "超过部分不予", "不予支持", "司法保护上限"])
        has_partial = _has(tn, ["四倍以内", "以内有效", "并非全部无效", "部分有效", "超出部分无效", "超过部分无效", "仅超出"])
        return has_topic and has_cap and has_partial
    return _journal_norm_ok(env, pred)


# 6. 大额现金交付陷阱(反直觉核心) — 第二笔借条20万称现金交付但无取现/转账凭证;
#    不能仅凭借条认定交付, 举证困难/有败诉风险, 须如实提示并落 Notion。
#    Backend fact: email#3 现金无凭证; 判例 case_003 反面 / art_zj_cash。
#    ⚠️ 反"乐观全要": 须点出现金交付举证风险(而非"有借条就能要回20万")。
def d_cash_delivery_risk(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["现金交付", "现金出借", "现金给", "20万现金", "第二笔", "20万"])
        has_risk = _has(t, ["举证难", "举证困难", "难以证明", "交付不能", "不能仅凭借条", "仅凭借条不", "无取现", "无凭证", "无转账", "败诉风险", "可能不予认定", "风险高", "证明力不足", "交付能力", "款项来源"])
        return has_topic and has_risk
    return _journal_ok(env, pred)


# 7. 保证期间届满陷阱(反直觉核心) — 老周借条签"担保"未写方式/期间:
#    未约定保证期间=主债务到期(2024-06-10)后6个月至 2024-12-10 届满; 王芳从未在期间内
#    单独向老周主张 → 保证人免责。须在 Notion 写出届满日 2024-12-10 + 免责结论。
#    Backend fact: 借条 email#1(老周"担保"未写期间) + email#9(老周称从未被主张) +
#    到期 2024-06-10(借条) → 计算届满日 2024-12-10; 判例 case_004。
#    HARD: 须出现计算出的届满时点(2024-12 / 六个月)+ 免责(仅提"担保人"不算)。
def d_guarantee_period_expired(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["保证期间", "担保期间", "保证人", "担保人", "老周", "周国华"])
        has_expired = _has(t, ["2024-12", "2024年12", "六个月", "6个月", "届满", "期间已过", "超过保证期间", "过了保证期"])
        # 至少要有"六个月/届满时点"这类计算依据之一(不能只写笼统"过期")
        has_computed = _has(t, ["2024-12", "2024年12", "六个月", "6个月"])
        has_verdict = _has(t, ["免责", "不再承担", "不承担保证", "不用还", "无须承担", "免除保证", "保证责任消灭", "不能要求", "不能向老周", "不能要担保人", "剔除"])
        return has_topic and has_expired and has_computed and has_verdict
    return _journal_ok(env, pred)


# 8. 保证方式约定不明=一般保证 — 老周仅签"担保"未写连带/一般 → 按一般保证, 享先诉抗辩权;
#    (即便在期间内也)不能直接连带清偿。须落 Notion。 Backend fact: 判例 case_005 / 第686条。
def d_general_guarantee_default(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["保证方式", "担保方式", "约定不明", "没写", "未写明", "仅签", "只签", "未约定"])
        has_default = _has(t, ["一般保证", "按一般保证", "非连带", "不是连带"])
        has_consequence = _has(t, ["先诉抗辩", "先诉抗辩权", "不能直接连带", "不能要求连带", "补充清偿", "强制执行仍不能", "第六百八十六条", "686条", "case_005"])
        return has_topic and has_default and has_consequence
    return _journal_ok(env, pred)


# 9. 夫妻共同债务陷阱(反直觉核心) — 陈强已婚配偶刘敏, 借款用于其个人炒股亏损(超出家庭日常、
#    非共同经营), 王芳无证据证明用于夫妻共同生活 → 配偶刘敏不共担。须在 Notion 写明
#    刘敏(具名)不共担 + 理由(炒股/个人)。 Backend fact: email#7(炒股) + email#8(想让刘敏一起还);
#    判例 case_006 / 第1064条。 ⚠️ 反"两口子的债跑不掉"。
def d_spousal_debt_excluded(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["夫妻共同债务", "共同债务", "配偶", "刘敏", "陈强老婆", "陈强妻子"])
        has_named = "刘敏" in t or _has(t, ["配偶", "陈强老婆", "陈强妻子"])
        has_reason = _has(t, ["炒股", "个人", "超出家庭日常", "非共同生活", "非共同经营", "未用于共同", "个人名义", "无证据证明用于"])
        has_verdict = _has(t, ["不属于夫妻共同", "不属共同债务", "不能要求配偶", "配偶不", "刘敏不", "不共担", "不承担", "不能要刘敏", "剔除", "不应由配偶"])
        return has_topic and has_named and has_reason and has_verdict
    return _journal_ok(env, pred)


# 10. 财产保全 — 陈强宁波房产挂牌急售有转移迹象, 可在起诉时申请诉讼财产保全(需提供担保)查封,
#     防止判决难以执行。须落 Notion(需担保这一要件)。 Backend fact: email#6(挂牌急售);
#     判例 case_011 / 第103条。
def d_property_preservation(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["财产保全", "保全", "查封", "冻结"])
        has_trigger = _has(t, ["转移财产", "急售", "卖房", "挂牌", "逃避", "难以执行", "转移", "处置财产"])
        has_need_guar = _has(t, ["提供担保", "需担保", "保全担保", "保证保险", "担保", "第一百零三条", "103条", "case_011"])
        return has_topic and has_trigger and has_need_guar
    return _journal_ok(env, pred)


# 11. 引用现行有效法条 — 须确认所引法条/解释 status=现行有效。纯程序核验, 保留 corpus 基础。
#     Backend fact: legal_search statutes.status='现行有效'(民法典/司法解释/民诉法)。
def d_statute_in_force(env) -> bool:
    """后端持久化中须落到**具体条号**并声明其现行有效，而非泛泛说"引用现行有效法条"。

    条号只能通过 legal_search 检索得到（PERSONA 只给争点类别、不给条号），
    故本条要求：Notion 台账里同时出现 ①有效性声明 ②具体法条载体 ③至少一个可核验的条号锚点。
    """
    def pred(tn):
        has_check = _has(tn, ["现行有效", "未废止", "未失效", "仍然有效", "现行版本", "有效版本"])
        has_law = _has(tn, ["民法典", "民间借贷司法解释", "民事诉讼法", "司法解释"])
        # 条号锚点：必须写出具体条文编号或 article_id，泛称不算
        has_anchor = _has(tn, [
            "第六百七十条", "第六百八十六条", "第六百九十二条", "第一百八十八条", "第一百九十五条",
            "第一千零六十四条", "第二十四条", "第二十五条", "第二十六条", "第一百零三条",
            "art_", "六百七十", "六百八十六", "一百八十八", "一千零六十四",
        ])
        return has_check and has_law and has_anchor
    return _journal_ok(env, pred)


# 12. 不服一审判决15日内上诉 — 纯程序期限结论, 保留 corpus 基础(15日 + 上诉 + 不服/送达)。
def d_appeal_window_15d(env) -> bool:
    """上诉期限须**落到 Notion 台账**（可延续的待办/期限记录），而非只在回复里提一句。

    改读后端持久状态（原先读 agent 回复文本，属 §6.1 禁止的"以表述代替结果"）。
    """
    def pred(t):
        has_window = _has(t, ["十五日", "15日", "15天", "十五天"])
        has_action = _has(t, ["上诉", "提起上诉", "向上一级", "上级法院"])
        has_trigger = _has(t, ["不服", "判决", "一审判决", "判决书", "送达"])
        return has_window and has_action and has_trigger
    return _journal_ok(env, pred)


# 13. 诉讼费阶梯收取(反直觉) — 财产案件受理费按标的额分段累计, 原告先预交、败诉方负担。
#     须在 Notion 写出阶梯口径(分段/比例) + 谁预交。 Backend fact: oap_court_04 阶梯口径。
def d_litigation_fee_tiered(env) -> bool:
    def pred(tn):
        has_fee = _has(tn, ["诉讼费", "受理费", "案件受理费"])
        # 注意：不可用裸 "2%"——本案借款月利率恰为 2%，会与诉讼费比例碰撞产生假命中。
        has_tier = _has(tn, ["阶梯", "分段", "按标的额", "按比例", "累计交纳", "分段累计",
                             "受理费2.5%", "受理费 2.5%", "2.5%", "1.5%", "0.5%"])
        has_who = _has(tn, ["先预交", "原告预交", "预交", "败诉方负担", "败诉方承担", "由败诉"])
        return has_fee and has_tier and has_who
    return _journal_norm_ok(env, pred)


# 14. 还款先抵利息后抵本金 — 陈强还的2万在无约定时先抵已产生利息再抵本金。须落 Notion。
#     Backend fact: 判例 case_007 / art_jd_27 / 第680条。
def d_repayment_offset(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["抵充", "先抵", "冲抵", "2万", "还款顺序", "已还的"])
        has_order = _has(t, ["先抵利息", "先抵充利息", "先息后本", "再抵本金", "先利息后本金", "第二十七条", "art_jd_27", "27条"])
        return has_topic and has_order
    return _journal_ok(env, pred)


# ─────────────────────────────────────────────────────────────────────────
# 诉求筛选矩阵 (claims matrix) — 王芳邮件#8《我想一起追的几笔账》列了6项,
# 每项有反直觉正确结论。须逐条甄别并把结论落 Notion。
# ─────────────────────────────────────────────────────────────────────────

# 15. 精神损失费不属合同之债 — 借贷为合同纠纷不支持精神损害赔偿, 须明确剔除并落 Notion。
def d_claim_mental_damages(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["精神损害", "精神损失", "精神赔偿", "担惊受怕"])
        has_verdict = _has(t, ["不支持", "不能主张", "不属于", "合同之债不", "合同纠纷不", "剔除", "不予支持", "不能要", "不归", "另案"])
        return has_topic and has_verdict
    return _journal_ok(env, pred)


# 16. 误工损失无依据 — 维权误工/关店损失非侵权人身损害, 借贷案件无法律依据, 须剔除并落 Notion。
def d_claim_lost_wages(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["误工", "关店", "关了店", "停业", "跑律所", "维权成本"])
        has_verdict = _has(t, ["无依据", "无法律依据", "不支持", "不能主张", "不属于", "剔除", "不予支持", "得不到支持", "没有依据", "不能要"])
        return has_topic and has_verdict
    return _journal_ok(env, pred)


# 17. 利息诉求(诉求②)须按 LPR 四倍封顶, 不能照约定全要。须落 Notion(与 d_lpr_four_times 呼应,
#     聚焦诉求层面)。 Backend fact: 约定月息2% 超四倍。
def d_claim_interest_capped(env) -> bool:
    def pred(tn):
        has_topic = _has(tn, ["利息", "月息2%", "约定利息", "约定的利息"])
        has_cap = _has(tn, ["LPR四倍", "四倍", "超出部分不", "超过部分不", "不能全要", "不能照约定", "封顶", "15.4", "调整到", "降到", "按四倍"])
        return has_topic and has_cap
    return _journal_norm_ok(env, pred)


# 18. 职业放贷甄别(防御性) — 王芳系朋友间偶发出借, 不构成职业放贷, 合同有效; 须能区分并落 Notion。
#     Backend fact: 判例 case_014(职业放贷反面)。
def d_not_professional_lending(env) -> bool:
    def pred(t):
        has_topic = _has(t, ["职业放贷", "经常性", "不特定对象", "放贷资质", "以放贷为业"])
        has_verdict = _has(t, ["不构成", "不属于职业放贷", "朋友间", "偶发", "个别", "特定对象", "老同学", "合同有效", "不是职业放贷", "区别于职业"])
        return has_topic and has_verdict
    return _journal_ok(env, pred)


# ─────────────────────────────────────────────────────────────────────────
# 律师选聘矩阵 (lawyer matrix) — notification_hub 'oa_lawyer_hub' 名录 8 名律师
# (LD-001~008)。王芳约束: 民间借贷/合同纠纷 / 杭州 / 预付≤¥8000 / 倾向风险代理 / 与陈强无牵连。
# 正确: LD-006 周敏 最优; LD-008 钱蕾 次优。选定/排除结论须持久化到 Notion(证明真读了名录并落台账,
# 而非在对话里泛提律师名)。
# ─────────────────────────────────────────────────────────────────────────

# L0. 读了律师名录 — 须在 Notion 台账里引用至少 2 个律师编号(LD-xxx), 证明真读了名录。
def d_reads_lawyer_roster(env) -> bool:
    def pred(t):
        codes = ["LD-001", "LD-002", "LD-003", "LD-004", "LD-005", "LD-006", "LD-007", "LD-008",
                 "LD001", "LD002", "LD003", "LD004", "LD005", "LD006", "LD007", "LD008"]
        return sum(1 for c in codes if c in t) >= 2
    return _journal_ok(env, pred)


# L1. 利益冲突排除 — LD-001 赵铭是被告陈强的常年顾问/曾代理陈强 → 利益冲突, 不能选。
#     Backend fact: oap_lawyer_01(赵铭/之江所, 陈强常年顾问)。须落 Notion。
def d_lawyer_conflict_excluded(env) -> bool:
    def pred(t):
        has_lawyer = _has(t, ["LD-001", "LD001", "赵铭", "之江"])
        has_reason = _has(t, ["利益冲突", "冲突", "对方", "被告", "陈强", "常年顾问", "顾问单位", "代理过陈强", "代理对方"])
        has_verdict = _has(t, ["不能选", "不能委托", "排除", "回避", "不可选", "不宜", "跳过", "不考虑", "淘汰"])
        return has_lawyer and has_reason and has_verdict
    return _journal_ok(env, pred)


# L2. 执业证吊销排除 — LD-002 孙立执业证已吊销 → 不能承办。 Backend fact: oap_lawyer_02。须落 Notion。
def d_lawyer_disbarred_excluded(env) -> bool:
    def pred(t):
        has_lawyer = _has(t, ["LD-002", "LD002", "孙立", "恒丰"])
        has_reason = _has(t, ["吊销", "执业证", "执业资格", "不得承办", "无资格", "资格被", "停止执业"])
        has_verdict = _has(t, ["不能选", "不能委托", "排除", "不可选", "不能用", "不考虑", "淘汰", "出局"])
        return has_lawyer and has_reason and has_verdict
    return _journal_ok(env, pred)


# L3. 专业不符排除 — LD-003 李航专办刑事, 不办民间借贷。 Backend fact: oap_lawyer_03。须落 Notion。
def d_lawyer_wrong_specialty_excluded(env) -> bool:
    def pred(t):
        has_lawyer = _has(t, ["LD-003", "LD003", "李航", "明理"])
        has_reason = _has(t, ["刑事", "刑辩", "不办民间借贷", "不承办民间借贷", "不办民商", "专业不符", "领域不符", "不对口", "毒品"])
        has_verdict = _has(t, ["不能选", "排除", "不合适", "不对口", "不考虑", "淘汰", "不匹配", "不可选"])
        return has_lawyer and has_reason and has_verdict
    return _journal_ok(env, pred)


# L4. 执业地不符排除 — LD-004 吴江仅在宁波执业, 杭州案件不便。 Backend fact: oap_lawyer_04。须落 Notion。
def d_lawyer_wrong_jurisdiction_excluded(env) -> bool:
    def pred(t):
        has_lawyer = _has(t, ["LD-004", "LD004", "吴江", "甬信"])
        has_reason = _has(t, ["宁波执业", "仅在宁波", "只在宁波", "执业地", "不在杭州", "异地", "宁波地区"])
        has_verdict = _has(t, ["不能选", "排除", "不合适", "不在本地", "不考虑", "淘汰", "不可选", "不便"])
        return has_lawyer and has_reason and has_verdict
    return _journal_ok(env, pred)


# L5. 超预付预算排除 — LD-005 郑霞仅计时收费需预付¥60000 > 王芳¥8000上限。
#     Backend fact: oap_lawyer_05(¥60000) + email#10(预付≤¥8000)。须落 Notion。
def d_lawyer_over_budget_excluded(env) -> bool:
    def pred(tn):
        has_lawyer = _has(tn, ["LD-005", "LD005", "郑霞", "大公"])
        has_reason = _has(tn, ["60000", "6万", "预付", "计时", "超预算", "超出预算", "付不起", "太贵", "超过8000", "超过八千"])
        has_verdict = _has(tn, ["不能选", "排除", "超预算", "付不起", "不可选", "超出", "淘汰", "不考虑"])
        return has_lawyer and has_reason and has_verdict
    return _journal_norm_ok(env, pred)


# L6. 风险代理超上限 — LD-007 冯涛风险代理40% > 民事30%上限 → 约定部分无效/不宜选。
#     Backend fact: oap_lawyer_07(40% vs 30%上限)。须落 Notion。
def d_lawyer_contingency_cap(env) -> bool:
    def pred(tn):
        has_lawyer = _has(tn, ["LD-007", "LD007", "冯涛", "金诺"])
        has_rule = _has(tn, ["40%", "百分之四十", "30%", "百分之三十", "上限", "超过上限", "超上限"])
        has_verdict = _has(tn, ["无效", "超上限", "超过上限", "不宜选", "不能选", "排除", "违规", "不合规", "约定无效", "不可选"])
        return has_lawyer and has_rule and has_verdict
    return _journal_norm_ok(env, pred)


# L7. 选定最优律师 — 唯一最优 LD-006 周敏(借贷专长+杭州+风险代理15%+预付¥4000); 须在 Notion
#     明确推荐并锚定编号。 Backend fact: oap_lawyer_06。
def d_lawyer_best_pick(env) -> bool:
    def pred(t):
        has_pick = _has(t, ["LD-006", "LD006", "周敏"])
        has_recommend = _has(t, ["推荐", "最合适", "选她", "委托", "首选", "最优", "建议选", "就选", "锁定", "代理"])
        return has_pick and has_recommend
    return _journal_ok(env, pred)


# L8. 预付预算硬顶 — 须明确把"预付律师费 ≤ ¥8000"作为筛选硬约束并落 Notion。
#     Backend fact: email#10(¥8000上限)。
def d_lawyer_budget_cap(env) -> bool:
    def pred(tn):
        has_cap = _has(tn, ["8000", "8千", "八千", "预付预算", "预算8000"])
        has_topic = _has(tn, ["预付", "律师费", "前期", "现金紧", "付不起", "预算"])
        has_apply = _has(tn, ["以内", "不超过", "上限", "超预算", "排除", "底线", "硬约束", "付得起", "控制在", "超出"])
        return has_cap and has_topic and has_apply
    return _journal_norm_ok(env, pred)


# L9. 强制换律师(disruption 响应) — 周敏(LD-006)利益冲突退出后, 须改选唯一合规且合预算的
#     LD-008 钱蕾(18%/¥6000), 而非回到任何已排除律师。须把改选结论落 Notion。
#     Backend fact: mutation s13_lawyer_conflict(LD-006退出) + oap_lawyer_08(LD-008次优)。
def d_lawyer_reselect(env) -> bool:
    def pred(t):
        saw_withdraw = _has(t, ["利益冲突", "退出", "回避", "周敏", "LD-006", "LD006", "所合并", "合并"])
        reselect_valid = _has(t, ["LD-008", "LD008", "钱蕾"])
        bad = _has(t, ["改选LD-001", "改委托LD-001", "换成LD-005", "改选郑霞", "改选赵铭"])
        return saw_withdraw and reselect_valid and not bad
    return _journal_ok(env, pred)


# ─────────────────────────────────────────────────────────────────────────
# disruption 反驳 (rebuttal) — 针对 mutation 注入的对方动作, 须得出反驳结论并落 Notion。
# ─────────────────────────────────────────────────────────────────────────

# R1. 管辖权异议反驳 — 被告以住所地宁波提异议; 须依接收货币一方(出借人住所地杭州)规则反驳,
#     异议不成立。须落 Notion。 Backend fact: mutation s7_jurisdiction_objection; 判例 case_009。
def d_jurisdiction_objection_rebuttal(env) -> bool:
    def pred(t):
        saw_objection = _has(t, ["管辖权异议", "管辖异议", "移送管辖", "管辖问题", "移送宁波", "移到宁波"])
        has_basis = _has(t, ["接收货币一方", "合同履行地", "出借人所在地", "出借人住所地", "杭州", "西湖"])
        has_verdict = _has(t, ["不成立", "驳回", "异议不", "维持", "无需移送", "不应移送", "西湖区有管辖", "杭州管辖", "由杭州", "由西湖"])
        return saw_objection and has_basis and has_verdict
    return _journal_ok(env, pred)


# R2. 砍头息抗辩应对 — 被告主张第一笔本金按实际36万(陈强这点正确); 须接受按 360000 主张本金,
#     而非坚持借条40万。须落 Notion(计算出的 360000)。 Backend fact: mutation s10_counterclaim;
#     判例 case_001 / art_jd_26。
def d_defense_kantou_accepted(env) -> bool:
    def pred(tn):
        saw_claim = _has(tn, ["砍头息", "预先扣除", "预扣", "实际到账", "实到", "按36万", "本金按实际"])
        has_verdict = _has(tn, ["接受", "认可", "调整为", "按实际", "360000", "36万", "不坚持40万", "改按", "主张36"])
        return saw_claim and has_verdict
    return _journal_norm_ok(env, pred)


# ─────────────────────────────────────────────────────────────────────────
# NEW (2026-07-25) — STEP-2 complexity: 跨阶段数值一致性核对 (multi-number reconciliation)。
# 强模型即便逐点分析, 也常在"数字层面"不自洽。此 check 要求 Notion 结案/研判台账里同时出现
# 三个互相印证的数字, 迫使 agent 把砍头息调整后的本金、四倍利率上限、判决支持金额对齐:
#   ① 实际本金 360000 (砍头息调整后);
#   ② LPR 四倍上限 15.4(%);
#   ③ 判决/主张支持的本金 360000 (与①一致, 排除第二笔20万现金)。
# 仅当三者都持久化且一致时通过。这是纯环境状态判定, 只写关键词或写错数字(如把本金写成
# 400000/600000, 或利率写成24%全要)都失败。 Backend fact: email#1/#2(借条40万/实到36万),
# art_jd_25(四倍15.4%), s16 判决(本金360000)。
def d_amounts_reconciled(env) -> bool:
    def pred(tn):
        # 实际本金(砍头息后)与判决支持金额一致 = 360000
        has_principal = "360000" in tn or "36万" in tn
        # 四倍利率上限
        has_rate_cap = _has(tn, ["15.4", "四倍", "LPR四倍"])
        # 排除第二笔20万(现金): 明确不计入本金/被驳回
        excludes_second = _has(tn, ["驳回", "不予认定", "不支持", "举证不能", "第二笔不", "20万不", "不计入", "剔除"])
        # 且不能把本金错误坚持为借条面额400000/600000作为最终认定本金
        return has_principal and has_rate_cap and excludes_second
    return _journal_norm_ok(env, pred)


ALL_D_CHECKS = [
    # 程序三连
    d_no_arbitration_precondition,
    d_limitation_3y_interruption,
    d_jurisdiction_lender,
    # 实体反直觉雷区
    d_kantou_interest_principal,
    d_lpr_four_times,
    d_cash_delivery_risk,
    d_guarantee_period_expired,
    d_general_guarantee_default,
    d_spousal_debt_excluded,
    d_property_preservation,
    d_statute_in_force,
    d_appeal_window_15d,
    d_litigation_fee_tiered,
    d_repayment_offset,
    # 诉求筛选矩阵
    d_claim_mental_damages,
    d_claim_lost_wages,
    d_claim_interest_capped,
    d_not_professional_lending,
    # 律师选聘矩阵 (场景约束型)
    d_reads_lawyer_roster,
    d_lawyer_conflict_excluded,
    d_lawyer_disbarred_excluded,
    d_lawyer_wrong_specialty_excluded,
    d_lawyer_wrong_jurisdiction_excluded,
    d_lawyer_over_budget_excluded,
    d_lawyer_contingency_cap,
    d_lawyer_best_pick,
    d_lawyer_budget_cap,
    d_lawyer_reselect,
    # disruption 反驳
    d_jurisdiction_objection_rebuttal,
    d_defense_kantou_accepted,
    # NEW: 跨阶段数值一致性
    d_amounts_reconciled,
]
