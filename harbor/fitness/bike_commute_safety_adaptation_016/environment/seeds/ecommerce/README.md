# Ecommerce fixture: commute equipment

Synthetic catalog, SKU, stock, cart and address data for urban cycling equipment. `sku_helmet_h2` and `sku_light_l1` are distinct products; rain gear, reflective gear and supplements remain separate catalog entries. Orders are intentionally absent at initialization and receive runtime-generated order IDs through `place_order`; later logistics mutations resolve the relevant order through `order_items.sku_id`.
