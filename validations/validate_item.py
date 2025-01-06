def validate_create_item(data):
    required_fields = [
        "item_sku", "item_name", "item_uom", "item_group", "retail_price", 
        "purchase_price", "warranty_period", "is_stock_item", "brand", 
        "description", "single_unit_dimensions", "single_unit_weight", 
        "weight_uom", "country_of_origin", "barcode", "barcode_type"
    ]

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return {"error": True, "message": "Missing required fields", "fields": missing_fields}

    # Validate data types and logical constraints
    if not isinstance(data.get('retail_price'), (int, float)) or data['retail_price'] <= 0:
        return {"error": True, "message": "Invalid retail price"}
    if not isinstance(data.get('purchase_price'), (int, float)) or data['purchase_price'] < 0:
        return {"error": True, "message": "Invalid purchase price"}
    if data['purchase_price'] > data['retail_price']:
        return {"error": True, "message": "Purchase price cannot exceed retail price"}
    if not isinstance(data.get('warranty_period'), int) or data['warranty_period'] < 0:
        return {"error": True, "message": "Invalid warranty period"}

    return {"error": False}  # Valid input


def validate_read_params(params):
    # Ensure at least one query parameter is provided
    if not params:
        return {"error": True, "message": "Provide at least one search parameter"}
    
    # Allowable parameters
    allowable_params = ["item_name", "item_group", "brand", "item_sku"]
    invalid_params = [key for key in params if key not in allowable_params]
    if invalid_params:
        return {"error": True, "message": f"Invalid query parameter(s): {', '.join(invalid_params)}"}

    return {"error": False}  # Valid input


def validate_update_item(data):
    if not data:
        return {"error": True, "message": "No update fields provided"}

    # Validate fields if present
    for field, value in data.items():
        if field in ['retail_price', 'purchase_price', 'warranty_period'] and (
            not isinstance(value, (int, float)) or value < 0
        ):
            return {"error": True, "message": f"Invalid value for {field}"}

    return {"error": False}  # Valid input


def validate_delete_item(item_sku):
    if not item_sku:
        return {"error": True, "message": "Item SKU is required"}
    return {"error": False}  # Valid input