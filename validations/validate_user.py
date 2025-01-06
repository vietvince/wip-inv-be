def validate_create_user(data):
    required_fields = ["user_id", "user_name", "pass_hash"]

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return {"error": True, "message": "Missing required fields", "fields": missing_fields}

    # Validate field lengths
    if len(data.get("user_id", "")) > 50:
        return {"error": True, "message": "user_id exceeds maximum length of 50 characters"}
    if len(data.get("user_name", "")) > 100:
        return {"error": True, "message": "user_name exceeds maximum length of 100 characters"}
    if len(data.get("pass_hash", "")) > 255:
        return {"error": True, "message": "pass_hash exceeds maximum length of 255 characters"}

    # Validate user role
    allowed_roles = ["admin", "employee"]
    if "user_role" in data and data["user_role"] not in allowed_roles:
        return {"error": True, "message": f"Invalid user_role. Allowed values: {', '.join(allowed_roles)}"}

    # Ensure user_name is not empty or whitespace
    if not data["user_name"].strip():
        return {"error": True, "message": "user_name cannot be empty or whitespace"}

    return {"error": False}


def validate_read_user_params(params):
    if not params:
        return {"error": True, "message": "Provide at least one search parameter"}

    allowable_params = ["user_name", "user_role", "user_id"]
    invalid_params = [key for key in params if key not in allowable_params]
    if invalid_params:
        return {"error": True, "message": f"Invalid query parameter(s): {', '.join(invalid_params)}"}

    return {"error": False}


def validate_update_user(data):
    if not data:
        return {"error": True, "message": "No update fields provided"}

    for field, value in data.items():
        if field == "user_id":
            return {"error": True, "message": "user_id cannot be updated (immutable field)"}
        if field == "user_role" and value not in ["admin", "employee"]:
            return {"error": True, "message": "Invalid user_role. Allowed values: admin, employee"}
        if field == "user_name" and not value.strip():
            return {"error": True, "message": "user_name cannot be empty or whitespace"}
        if field == "pass_hash" and len(value) > 255:
            return {"error": True, "message": "pass_hash exceeds maximum length of 255 characters"}

    return {"error": False}


def validate_delete_user(user_id):
    if not user_id:
        return {"error": True, "message": "user_id is required"}
    return {"error": False}