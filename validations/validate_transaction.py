def validate_purchase(data):
    required_fields = [
        "item_sku", "warehouse_id", "customer_id", "date", "sales_uom",
        "transaction_quantity", "shipping_address", "shipping_city",
        "shipping_state", "shipping_zipcode", "shipping_country"
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {"error": True, "message": "Missing required fields", "fields": missing_fields}

    # Validate numeric fields
    if data.get("transaction_quantity") is not None and data["transaction_quantity"] <= 0:
        return {"error": True, "message": "Transaction quantity must be greater than 0"}

    if data.get("transaction_weight") is not None and data["transaction_weight"] < 0:
        return {"error": True, "message": "Transaction weight cannot be negative"}

    # Validate string length for tracking information
    if data.get("tracking_information") is not None and len(data["tracking_information"]) > 255:
        return {"error": True, "message": "Tracking information exceeds the maximum allowed length"}

    return {"error": False}


def validate_update_purchase(data):
    if not data:
        return {"error": True, "message": "No update fields provided"}

    valid_fields = [
        "date", "sales_uom", "transaction_quantity", "shipping_address",
        "shipping_city", "shipping_state", "shipping_zipcode", "shipping_country",
        "transaction_image", "transaction_barcode", "transaction_weight", "tracking_information"
    ]
    invalid_fields = [field for field in data.keys() if field not in valid_fields]

    if invalid_fields:
        return {"error": True, "message": "Invalid fields provided", "fields": invalid_fields}

    # Prevent updating immutable fields
    immutable_fields = ["item_sku", "warehouse_id", "customer_id"]
    if any(field in data for field in immutable_fields):
        return {"error": True, "message": "Fields item_sku, warehouse_id, and customer_id cannot be updated"}

    # Validate numeric fields
    if data.get("transaction_quantity") is not None and data["transaction_quantity"] <= 0:
        return {"error": True, "message": "Transaction quantity must be greater than 0"}

    if data.get("transaction_weight") is not None and data["transaction_weight"] < 0:
        return {"error": True, "message": "Transaction weight cannot be negative"}

    # Validate string length for tracking information
    if data.get("tracking_information") is not None and len(data["tracking_information"]) > 255:
        return {"error": True, "message": "Tracking information exceeds the maximum allowed length"}

    return {"error": False}


def validate_return(data):
    if "return_quantity" not in data:
        return {"error": True, "message": "Missing required field: return_quantity"}

    # Validate numeric fields
    if data["return_quantity"] <= 0:
        return {"error": True, "message": "Return quantity must be greater than 0"}

    # Check if return_quantity exceeds the transaction_quantity (this should be validated in the database logic)
    # Example (pseudo-code):
    # if data["return_quantity"] > current_transaction_quantity:
    #     return {"error": True, "message": "Return quantity cannot exceed transaction quantity"}

    return {"error": False}