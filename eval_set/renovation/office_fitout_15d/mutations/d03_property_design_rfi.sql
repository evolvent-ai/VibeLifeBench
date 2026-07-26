-- D3 06:00 静安「一件事」平台对商业 fit-up 备案发出 RFI（补正要求）。
-- processing → rfi。decision_note 承载平台要求的补件清单；history_json 追加一条可审计轨迹。
UPDATE visa_applications
SET status = 'rfi',
    decision_day = 3,
    decision_note = 'RFI：平台要求 BIM 出图（二维 CAD 不足）、强弱电负荷计算书（≥4kW/100㎡ 须证明）、消防应急照明与疏散通道平面图、甲醛 ≤0.05 mg/m³ 主材声明。请于 2026-07-05 18:00 前补正提交，逾期将影响 fit-up 期开工。依据 rule_property_v3_005、rule_property_v3_013。',
    history_json = json_insert(
      CASE WHEN json_valid(history_json) THEN history_json ELSE '[]' END,
      '$[#]',
      json_object(
        'at', '2026-07-04T06:00:00+08:00',
        'status', 'rfi',
        'actor', 'jingan_one_stop_portal',
        'note', '备案初审提出补正要求：BIM 出图、负荷计算书、消防平面图、主材环保声明。'
      )
    ),
    updated_at = '2026-07-04T06:00:00+08:00'
WHERE application_id = 'commercial_fit_up_filing_001'
  AND updated_at < '2026-07-04T06:00:00+08:00';
