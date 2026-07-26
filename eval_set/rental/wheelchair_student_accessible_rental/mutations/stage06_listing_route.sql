UPDATE listings SET attrs_json=json_set(attrs_json,'$.night_access','south_gate_after_22_30_reroute') WHERE listing_id='wh09_listing_a';
