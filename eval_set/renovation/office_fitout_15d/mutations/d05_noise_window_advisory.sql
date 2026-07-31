-- D5 物业确认暴雨期后的受限噪音与材料进场窗口。
UPDATE advisories
SET level = 3,
    text = '陆家嘴金融中心写字楼装修合规通告（D5 物业确认）：噪音作业仅限工作日 09:30-11:30 与 14:00-16:30；其余时段仅可安排无噪音工序。材料进场须提前预约货梯，暴雨预警期间服从卸货区临时关闭安排。依据 rule_property_006、rule_property_015、rule_property_017。',
    updated_at = '2026-07-06T12:00:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-06T12:00:00+08:00';
