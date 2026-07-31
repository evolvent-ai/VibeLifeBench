-- D5 暴雨橙色预警 + 物业进一步压缩噪音窗口。advisory 级别升至 3。
UPDATE advisories
SET level = 3,
    text = '陆家嘴金融中心写字楼装修合规通告（暴雨预警期）：气象部门发布暴雨橙色预警，货梯与卸货区在预警期间限用，材料进场需改约时段。噪音作业窗口进一步压缩为工作日 09:30-11:30 与 14:00-16:30；法定节假日全天禁止噪音作业。湿作业与外立面相关工序暂停。依据 rule_property_006、rule_property_015、rule_property_017。',
    updated_at = '2026-07-06T07:30:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-06T07:30:00+08:00';
