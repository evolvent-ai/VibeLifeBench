-- D11 大堂安保升级：施工人员与配送员须提前 7 天报备办证。
UPDATE advisories
SET level = 3,
    text = '陆家嘴金融中心大堂安保通告（升级）：自即日起，施工人员与配送人员进入须凭实名门禁卡，名单需提前 7 个工作日提交物业办证，临时人员不予放行。管控期内货梯使用需随名单一并预约。排期时须为办证预留 7 天前置时间。依据 rule_property_015、rule_property_018。',
    updated_at = '2026-07-12T08:30:00+08:00'
WHERE country_code = 'CN'
  AND updated_at < '2026-07-12T08:30:00+08:00';
