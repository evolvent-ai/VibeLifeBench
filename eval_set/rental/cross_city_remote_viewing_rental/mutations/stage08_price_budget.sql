UPDATE listings SET price_minor=630000, attrs_json=json_set(attrs_json,'$.cleaning_fee_minor',180000) WHERE listing_id='rs005_listing_b';
