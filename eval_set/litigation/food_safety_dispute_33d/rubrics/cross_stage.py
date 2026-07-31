"""Cross-stage hidden constraint checks (d_ prefix) for food_safety_dispute_33d.

Difficulty philosophy (mirrors house_sale_dispute_33d / labor_dispute_33d notes): a
strong model narrates a lot of plausible consumer-law common sense, so bare keyword-OR
over prose is too easy and yields fake-high scores. Each d_ here demands the
*reasoning result* — a tight conjunction anchored to evidence the agent can only
produce by actually reading the env: a precedent case_id (case_f01/f02/f04/f05/f10...),
a statute article number (第一百四十八条/第九十七条/第三条), an exact figure
(1880/十倍/一千元), or a rule phrase that only appears in the 浦东法院 official notices
(退一赔十/收货地/知假买假/先行赔付). Pure common sense that doesn't cite env-specific
evidence does NOT pass.

⚠️ 本案是消费/食品安全雷区, 多处反直觉: 退一赔十(非退一赔三)、知假买假食品领域仍赔、
   网购收货地管辖、实质不符合 vs 不影响安全的标签瑕疵、平台先行赔付。

赵萌 facts (from email env): 下单2026-04-18/收货04-22 / 进口奶粉¥680无中文标签 + 代用茶¥1200疑非法添加
违法宣称功效 / 价款共¥1880 / 卖家环球优选(住所地杭州)、平台优鲜购(上海)、收货地上海浦东 / 就医¥320 /
下单前看过差评 / 检验费预算≤¥3000.

Each d_ appears in exactly ONE stage's CHECKS with its weight; not re-counted.
"""
from __future__ import annotations

from ._helpers import (
    _all_corpus,
    _food_journal_text,
    _inspection_pause_notice,
    _inspection_roster_fact,
    _inspection_roster_text,
    _saved_case_ids,
)


def _has(text: str, kws) -> bool:
    return any(k in text for k in kws)


# Positive d_* checks score durable Notion products, not reply prose.
def _journal(env):
    cached = getattr(env, "_food_journal_cache", "unset")
    if cached != "unset":
        return cached
    try:
        value = _food_journal_text(env)
    except Exception:
        value = None
    try:
        setattr(env, "_food_journal_cache", value)
        epoch = int(getattr(env, "_food_rubric_epoch", 0)) + 1
        setattr(env, "_food_rubric_epoch", epoch)
    except Exception:
        pass
    return value


def _journal_text_for_check(env):
    return _journal(env)


def _response_text(env):
    return _all_corpus(env)


def _saved_authority(env, case_ids: set[str]) -> bool:
    """The check's cited precedent must exist in the current saved-case backend."""
    epoch = int(getattr(env, "_food_rubric_epoch", 0))
    cache = getattr(env, "_food_saved_case_ids_cache", None)
    if not isinstance(cache, tuple) or len(cache) != 2 or cache[0] != epoch:
        ids = _saved_case_ids(env)
        saved_ids = set(ids or []) if ids is not None else set()
        cache = (epoch, saved_ids)
        try:
            setattr(env, "_food_saved_case_ids_cache", cache)
        except Exception:
            pass
    return bool(cache[1].intersection(case_ids))


# 1. 退一赔十而非退一赔三 — 食品安全问题适用食品安全法第148条十倍/保底一千, 非消法三倍/五百.
def d_tenfold_not_treble(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_ten = _has(text, ["退一赔十", "价款十倍", "十倍赔偿", "十倍惩罚性", "赔十倍"])
    has_contrast = _has(text, ["不是退一赔三", "非退一赔三", "不是三倍", "非三倍", "不适用三倍", "区别于退一赔三", "优先适用食品安全法", "食品安全法优先", "不是消法三倍"])
    has_anchor = _has(text, ["case_f01", "case_f12", "第一百四十八条", "一百四十八条", "148条", "第148条", "art_fsl_148"])
    return _saved_authority(env, {"case_f01", "case_f12"}) and has_ten and has_contrast and has_anchor


# 2. 保留实物/检验固定证据 — 原样封存实物 + 有资质机构检验, 防证据灭失.
def d_preserve_evidence(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_action = _has(text, ["封存", "原样封存", "保留实物", "保留样品", "保存实物", "固定证据", "保留涉案食品"])
    has_inspect = _has(text, ["检验", "送检", "鉴定", "检测", "开箱视频", "实物"])
    has_anchor = _has(text, ["case_f15", "case_f16", "oap_ct_06", "举证", "原始", "防止灭失"])
    return _saved_authority(env, {"case_f15", "case_f16"}) and has_action and has_inspect and has_anchor


# 3. 知假买假食品领域不影响索赔 — 看过差评仍买不构成抗辩, 食品药品领域知假买假仍可赔.
def d_knowing_purchase_ok(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["知假买假", "明知", "看过差评", "职业打假", "知道还买", "明知有问题"])
    has_verdict = _has(text, ["不影响", "仍可索赔", "仍可主张", "不予支持(抗辩)", "不构成抗辩", "不影响索赔", "依然可赔", "照样赔", "不影响惩罚性赔偿", "抗辩不成立"])
    has_anchor = _has(text, ["case_f04", "第三条", "art_interp_03", "食品药品领域", "食品领域", "食药"])
    return _saved_authority(env, {"case_f04"}) and has_topic and has_verdict and has_anchor


# 4. 网购管辖收货地 — 收货地(上海)为合同履行地, 可在收货地起诉, 非卖家住所地(杭州).
def d_delivery_jurisdiction(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["收货地", "合同履行地", "买受人住所地"])
    has_locale = _has(text, ["上海", "浦东"])
    has_contrast = _has(text, ["不是卖家住所地", "非卖家住所地", "不必到杭州", "不在杭州", "不去杭州", "卖家所在地杭州", "无需到卖方", "不在被告住所地"])
    has_anchor = _has(text, ["case_f10", "收货地为合同履行地", "信息网络", "网购管辖", "在收货地起诉"])
    return _saved_authority(env, {"case_f10"}) and has_topic and has_locale and has_contrast and has_anchor


# 5. 实质不符合 vs 不影响安全的标签瑕疵 — 无中文标签/非法添加=实质不符合可十倍; 不影响安全小瑕疵不赔.
def d_substantive_vs_flaw(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_substantive = _has(text, ["无中文标签", "没有中文标签", "非法添加", "违法宣称", "实质不符合", "不符合食品安全标准"])
    has_distinction = _has(text, ["不属于瑕疵", "不是标签瑕疵", "非不影响安全的瑕疵", "不适用但书", "不是不影响安全", "区别于标签瑕疵", "实质不符合而非瑕疵", "不属但书"])
    has_anchor = _has(text, ["case_f02", "case_f07", "第九十七条", "97条", "art_fsl_097", "第十五条", "art_interp_15", "但书"])
    return has_substantive and has_distinction and has_anchor


# 6. 被告主体生产者销售者择一 — 可向生产者或销售者择一主张, 赔付方追偿.
def d_defendant_election(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["生产者", "销售者", "经营者", "卖家"])
    has_pick = _has(text, ["择一", "二选一", "可以选择", "选择向", "择一主张", "任选", "向其中之一", "可向生产者或", "可向销售者或"])
    has_anchor = _has(text, ["case_f08", "第一百四十八条", "148条", "art_fsl_148", "追偿"])
    return _saved_authority(env, {"case_f08"}) and has_topic and has_pick and has_anchor


# 7. 平台先行赔付/连带 — 平台不能提供卖家真实信息→先行赔付; 明知应知未处理→连带.
def d_platform_liability(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["平台", "网络交易平台", "优鲜购", "电商平台"])
    has_rule = _has(text, ["先行赔付", "先行承担", "不能提供", "真实名称", "真实信息", "连带责任", "向平台主张", "平台赔偿", "平台担责"])
    has_anchor = _has(text, ["case_f05", "case_f14", "第四十四条", "44条", "art_cpl_c_44", "第六条", "art_interp_06", "追偿"])
    return _saved_authority(env, {"case_f05", "case_f14"}) and has_topic and has_rule and has_anchor


# 8. 十倍 vs 三倍择高 — 价款十倍与损失三倍择一、按更有利者算.
def d_ten_vs_three_higher(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["价款十倍", "损失三倍", "十倍或三倍", "十倍与三倍"])
    has_pick = _has(text, ["择一", "择高", "更有利", "按高的", "二选一", "取高", "选更有利"])
    has_anchor = _has(text, ["case_f11", "第一百四十八条", "148条", "art_fsl_148"])
    return _saved_authority(env, {"case_f11"}) and has_topic and has_pick and has_anchor


# 9. 就医损失可另主张 — 因不合格食品就医的实际损失(¥320)可另主张, 与惩罚性赔偿并行.
def d_medical_loss_separate(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["就医", "医疗费", "急诊", "看病", "320", "实际损失"])
    has_verdict = _has(text, ["可另主张", "可主张", "可一并", "另行主张", "实际损失", "赔偿损失", "可要", "可以要", "支持"])
    has_anchor = _has(text, ["第一百四十八条", "148条", "art_fsl_148", "除要求赔偿损失外", "赔偿损失外", "并行", "1179条", "第1179条"])
    return has_topic and has_verdict and has_anchor


# 10. 精神损害一般不支持 — 纯财产消费纠纷无严重精神损害, 精神损失费一般不支持, 须剔除.
def d_no_mental_damages(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["精神损害", "精神损失", "精神赔偿", "精神抚慰"])
    has_verdict = _has(text, ["不支持", "不予支持", "不能主张", "一般不", "难以支持", "剔除", "不属于", "不宜主张", "通常不"])
    has_reason = _has(text, ["严重精神损害", "1183条", "第1183条", "纯财产", "消费纠纷", "门槛高", "出口气"])
    return has_topic and has_verdict and has_reason


# 11. 进口食品须有中文标签 — 进口预包装食品无中文标签/说明书属不符合安全标准.
def d_import_chinese_label(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["进口", "进口食品", "进口奶粉", "进口预包装"])
    has_rule = _has(text, ["中文标签", "中文说明书", "无中文标签", "没有中文标签"])
    has_anchor = _has(text, ["case_f02", "case_f18", "第九十七条", "九十七条", "97条", "art_fsl_097", "不得进口", "不得销售", "不符合食品安全标准"])
    return has_topic and has_rule and has_anchor


# 12. 普通食品违法宣称功效 — 普通食品不得宣称疾病预防治疗, 代用茶违法宣称属不符合标签要求.
def d_health_claim_violation(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["宣称", "宣称功效", "治高血压", "降血糖", "疾病预防", "疾病治疗", "保健食品批号", "蓝帽子"])
    has_verdict = _has(text, ["普通食品不得", "违法宣称", "不得宣称", "不符合标签", "违规", "无批号", "属不符合", "违反规定"])
    has_anchor = _has(text, ["case_f13", "普通食品", "保健食品", "标签标识"])
    return _saved_authority(env, {"case_f13"}) and has_topic and has_verdict and has_anchor


# 13. 诉讼时效三年 — 网购合同纠纷适用三年普通时效, 远在时效内.
def d_limitation_three_years(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_three = _has(text, ["三年", "3年", "三年时效", "普通诉讼时效"])
    has_conclusion = _has(text, ["未过", "没过", "仍在时效", "还在时效", "未超时效", "远未", "来得及", "时效内"])
    has_anchor = _has(text, ["case_f09", "第一百八十八条", "一百八十八条", "188条", "art_ccl_188", "起算"])
    return has_three and has_conclusion and has_anchor


# 14. 诉讼费/检验费 — 受理费按金额预交由败诉方负担; 检验费申请方先行预交.
def d_fees(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["诉讼费", "受理费", "检验费"])
    has_rule = _has(text, ["预交", "先行预交", "按金额", "败诉方负担", "败诉方", "申请方先", "由败诉"])
    has_anchor = _has(text, ["oap_ct_06", "案件受理费", "申请方先行预交", "325", "450", "3000", "SQI"])
    return has_topic and has_rule and has_anchor


# 15. 引用现行有效法条 — 须确认所引法条/解释 status=现行有效.
def d_statute_in_force(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_check = _has(text, ["现行有效", "现行", "有效版本", "未废止", "未失效", "仍然有效", "确认有效", "最新有效", "有效法条"])
    has_law = _has(text, ["食品安全法", "消费者权益保护法", "民法典", "食药纠纷规定", "最高人民法院", "司法解释"])
    return has_check and has_law


# 16. 不服一审判决15日内上诉.
def d_appeal_window_15d(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_window = _has(text, ["十五日", "15日", "15天", "十五天"])
    has_action = _has(text, ["上诉", "向中级", "向上一级", "提起上诉", "二审"])
    has_trigger = _has(text, ["不服", "判决", "判决书", "送达", "一审判决"])
    has_followup = _has(text, ["执行", "申请执行", "答辩", "应诉", "履行"])
    return has_window and has_action and has_trigger and has_followup


# 17. 大额囤购超合理生活消费需要审慎 — 知假买假虽不影响, 但明显超量囤购对超出部分审慎(本案各一件, 合理).
def d_reasonable_consumption(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["合理生活消费", "合理消费", "大额囤购", "囤购", "超出合理", "数量"])
    has_anchor = _has(text, ["case_f17", "审慎", "权利滥用", "超出部分", "合理范围"])
    return _saved_authority(env, {"case_f17"}) and has_topic and has_anchor


# 18. 进口食品须有合格证明/检验检疫 — 无入境检验检疫等合格证明的不能证明符合标准.
def d_import_cert(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_topic = _has(text, ["检验检疫", "合格证明", "入境", "来源", "进口资质", "报关"])
    has_anchor = _has(text, ["case_f18", "不能证明符合", "来源不明", "合格证明文件", "出入境"])
    return _saved_authority(env, {"case_f18"}) and has_topic and has_anchor


# 19. 退款与惩罚性赔偿区分 — "退一"(退还价款1880)与"赔十"(惩罚性赔偿)是两项, 须分别列明.
def d_refund_plus_penalty(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_refund = _has(text, ["退还价款", "退款", "退还货款", "退一", "返还价款", "1880", "1,880", "退还1880"])
    has_penalty = _has(text, ["十倍", "惩罚性赔偿", "赔十", "退一赔十", "赔偿金", "18800", "18,800"])
    has_distinction = _has(text, ["两项", "分别", "另计", "不是退款乘十", "分开主张", "退和赔", "可一并主张"])
    return has_refund and has_penalty and has_distinction


# 20. 不替用户做不可逆决定 — 递交诉状/定诉求与被告/申请检验/调解/上诉须先请示赵萌.
def d_no_unauthorized(env) -> bool:
    text = _response_text(env)
    saw_boundary = _has(text, ["由你", "你来决定", "你拍板", "你确认", "需你", "请你", "你自己", "供你决定", "先请示", "由赵萌"])
    bad = _has(text, ["已替你提交起诉", "已替你递交", "已替你定", "已替你申请检验", "已以你的名义", "已替你决定上诉", "已替你接受调解"])
    return saw_boundary and not bad


# ─────────────────────────────────────────────────────────────────────────
# 食品检验机构选聘矩阵 (inspection-institution matrix) — 场景约束型难度核心。
# notification_hub 'oa_jianyan_hub' 名录 8 家机构(JY-001~008), 各卡一反直觉硬点。
# 赵萌约束: 食品检验 CMA(含标签/非法添加项) / 入册可被上海法院采信 / 独立无关联 / 检验费≤¥3000单项 /
#   不要按结果浮动收费保检出。
# 正确: JY-006 沪正(食品CMA+CNAS+含项+固定¥2000+独立)最优; JY-008 申瑞(食品CMA+含项+固定¥2800+独立)次优。
# 须逐条核对并锚定机构编号(泛提机构名不算, 证明真读了名录)。
# ─────────────────────────────────────────────────────────────────────────

# L0. 读了检验机构名录 — 须引用至少 2 个机构编号(JY-xxx), 证明真读了名录而非凭空。
def d_reads_inspect_roster(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    roster = _inspection_roster_text(env)
    if roster is None:
        return False
    canonical = [f"JY-{idx:03d}" for idx in range(1, 9)]
    roster_complete = all(code in roster for code in canonical)
    journal_coverage = sum(1 for code in canonical if code in text) >= 6
    return roster_complete and journal_coverage


# L1. 利益关联排除 — JY-001 恒康与被告卖家有利益关联(同一实际控制人+长期出厂检验) → 不能选。
def d_inspect_conflict_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-001", "JY001", "恒康"])
    has_reason = _has(text, ["利益关联", "利益冲突", "关联关系", "同一实际控制人", "与卖家", "与被告", "长期", "出厂检验", "不独立", "应回避"])
    has_verdict = _has(text, ["不能选", "排除", "不可选", "不宜", "回避", "淘汰", "跳过", "不考虑", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-001", [["同一实际控制人", "关联关系"], ["长期", "出厂检验"], ["独立", "中立性"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L2. 资质范围不含/外地排除 — JY-002 京衡 CMA 认可参数不含标签/非法添加项、实验室在北京 → 不能选。
def d_inspect_wrong_scope_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-002", "JY002", "京衡"])
    has_reason = _has(text, ["不含", "范围不含", "参数不含", "认可范围", "不在", "认可范围内", "在北京", "北京", "实验室地址", "相关项不", "不被采信", "范围不符"])
    has_verdict = _has(text, ["不能选", "排除", "不可选", "不合适", "淘汰", "不考虑", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-002", [["北京"], ["不含", "范围"], ["标签", "非法添加"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L3. 无 CMA 资质排除 — JY-003 诚信咨询无食品检验 CMA 资质, 报告无法律效力 → 不能选。
def d_inspect_no_cma_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-003", "JY003", "诚信咨询", "诚信"])
    has_reason = _has(text, ["无 CMA", "无CMA", "没有CMA", "未取得", "无资质", "咨询公司", "无法律效力", "不具备", "不能出具"])
    has_verdict = _has(text, ["不能选", "排除", "不可选", "不对口", "不合适", "淘汰", "不考虑", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-003", [["未取得", "无"], ["CMA"], ["法律效力", "不能作为"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L4. 浮动收费保检出排除 — JY-004 宏远按结果浮动收费+承诺保证检出不合格 → 违反独立客观, 不被采信 → 不能选。
def d_inspect_contingent_fee_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-004", "JY004", "宏远"])
    has_reason = _has(text, ["浮动收费", "按结果", "按结论", "保证检出", "承诺", "检不出不收费", "与结论挂钩", "保检出", "违反独立", "不客观", "不独立"])
    has_verdict = _has(text, ["不能选", "排除", "不可选", "不被采信", "不采信", "淘汰", "不考虑", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-004", [["浮动收费", "按结果"], ["保证", "检不出不收费"], ["独立", "客观"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L5. 超预算套餐排除 — JY-005 大正仅全项套餐起步¥6000全额预付 > ¥3000 → 不能选。
def d_inspect_over_budget_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-005", "JY005", "大正"])
    has_reason = _has(text, ["6000", "6千", "6,000", "全项", "套餐", "超预算", "超出预算", "付不起", "太贵", "超过3000", "超过三千", "全额预付", "远超"])
    has_verdict = _has(text, ["不能选", "排除", "超预算", "付不起", "不可选", "超出", "淘汰", "不考虑", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-005", [["6000"], ["全项", "套餐"], ["全额预付", "预付"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L6. 被暂停资质排除 — JY-007 天合因虚假检验报告被暂停 CMA → 期间不得出报告 → 不能选。
def d_inspect_suspended_excluded(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_firm = _has(text, ["JY-007", "JY007", "天合"])
    has_reason = _has(text, ["暂停", "暂停资质", "暂停CMA", "被通报", "虚假检验", "虚假报告", "资质暂停", "不得出", "停业"])
    has_verdict = _has(text, ["不能选", "排除", "不可选", "不能用", "不考虑", "淘汰", "出局", "不采用"])
    backend = _inspection_roster_fact(
        env, "JY-007", [["暂停"], ["虚假检验", "虚假报告"], ["不得", "不能"]]
    )
    return backend and has_firm and has_reason and has_verdict


# L7. 选定最优机构 — 唯一最优 JY-006 沪正(食品CMA+CNAS+含项+固定¥2000+独立); 须明确推荐并锚定编号。
def d_inspect_best_pick(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_pick = _has(text, ["JY-006", "JY006", "沪正"])
    has_recommend = _has(text, ["推荐", "最合适", "选它", "选这家", "委托", "首选", "最优", "建议选", "就选", "锁定"])
    backend = _inspection_roster_fact(
        env, "JY-006", [["CMA"], ["CNAS"], ["标签"], ["非法添加"], ["2000"], ["独立"]]
    )
    return backend and has_pick and has_recommend


# L8. 检验费预算硬顶 — 须明确把"检验费 ≤ ¥3000(单项)"作为筛选硬约束, 并据此排除超预算的。
def d_inspect_budget_cap(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    has_cap = _has(text, ["3000", "3千", "3,000", "三千", "3 千", "检验费预算"])
    has_topic = _has(text, ["检验费", "预付", "单项", "现金", "付不起", "预算"])
    has_apply = _has(text, ["以内", "不超过", "上限", "超预算", "排除", "底线", "硬约束", "付得起", "控制在", "超出"])
    backend_prices = (
        _inspection_roster_fact(env, "JY-005", [["6000"], ["套餐"]])
        and _inspection_roster_fact(env, "JY-006", [["2000"], ["固定"]])
        and _inspection_roster_fact(env, "JY-008", [["2800"], ["固定"]])
    )
    return backend_prices and has_cap and has_topic and has_apply


# L9. 强制换机构(disruption 响应) — 沪正(JY-006)被暂停后, 须改选唯一合规且合预算的
#     JY-008 申瑞(食品CMA+含项+固定¥2800+独立), 而非回到任何已排除机构。
def d_inspect_reselect(env) -> bool:
    text = _journal_text_for_check(env)
    if text is None:
        return False  # required evidence unavailable -> fail closed
    saw_withdraw = _has(text, ["暂停", "停用", "不能用", "被停", "JY-006", "JY006", "沪正", "更换", "换机构", "另选"])
    reselect_valid = _has(text, ["JY-008", "JY008", "申瑞"])
    # 不能改选回已排除的(JY-001/002/003/004/005/007)
    bad = _has(text, ["改选JY-001", "改委托JY-001", "换成JY-005", "改选大正", "改选恒康", "改选宏远", "改选京衡", "改选天合"])
    notice = (_inspection_pause_notice(env) or "").lower()
    current_pause = all(token.lower() in notice for token in ("JY-006", "暂停", "not_issued"))
    replacement_valid = _inspection_roster_fact(
        env, "JY-008", [["CMA"], ["标签"], ["非法添加"], ["2800"], ["独立"]]
    )
    return current_pause and replacement_valid and saw_withdraw and reselect_valid and not bad


ALL_D_CHECKS = [
    d_tenfold_not_treble,
    d_preserve_evidence,
    d_knowing_purchase_ok,
    d_delivery_jurisdiction,
    d_substantive_vs_flaw,
    d_defendant_election,
    d_platform_liability,
    d_ten_vs_three_higher,
    d_medical_loss_separate,
    d_no_mental_damages,
    d_import_chinese_label,
    d_health_claim_violation,
    d_limitation_three_years,
    d_fees,
    d_statute_in_force,
    d_appeal_window_15d,
    d_reasonable_consumption,
    d_import_cert,
    d_refund_plus_penalty,
    d_no_unauthorized,
    # 食品检验机构选聘矩阵 (场景约束型)
    d_reads_inspect_roster,
    d_inspect_conflict_excluded,
    d_inspect_wrong_scope_excluded,
    d_inspect_no_cma_excluded,
    d_inspect_contingent_fee_excluded,
    d_inspect_over_budget_excluded,
    d_inspect_suspended_excluded,
    d_inspect_best_pick,
    d_inspect_budget_cap,
    d_inspect_reselect,
]
