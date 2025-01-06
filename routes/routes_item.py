from flask import Blueprint, request, jsonify
from validations.validate_item import validate_create_item, validate_update_item, validate_read_params, validate_delete_item
from utility.db import get_db_connection

item_routes = Blueprint("item_routes", __name__)

# Create an item
@item_routes.route('/', methods=['POST'])
def create_item():
    data = request.json

    # Validate input
    validation_result = validate_create_item(data)
    if validation_result['error']:
        return jsonify({
            "message": validation_result['message'],
            "fields": validation_result.get('fields')
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the item already exists
        check_query = "SELECT item_sku FROM Item WHERE item_sku = %s"
        cur.execute(check_query, (data['item_sku'],))
        if cur.fetchone():
            return jsonify({"message": "Item already exists"}), 409

        # Insert the new item
        insert_query = """
            INSERT INTO Item (
                item_sku, item_name, item_uom, item_group, retail_price, purchase_price,
                warranty_period, is_stock_item, brand, description, single_unit_dimensions,
                single_unit_weight, weight_uom, country_of_origin, barcode, barcode_type
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        cur.execute(insert_query, (
            data['item_sku'], data['item_name'], data['item_uom'], data['item_group'], 
            data['retail_price'], data['purchase_price'], data['warranty_period'], 
            data['is_stock_item'], data['brand'], data['description'], 
            data['single_unit_dimensions'], data['single_unit_weight'], 
            data['weight_uom'], data['country_of_origin'], data['barcode'], data['barcode_type']
        ))
        conn.commit()

        return jsonify({"message": "Item created successfully"}), 201
    except Exception as e:
        print(f"Error creating item: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Read items
@item_routes.route('/', methods=['GET'])
def read_items():
    params = request.args.to_dict()

    # Validate input
    validation_result = validate_read_params(params)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Base query
        query = "SELECT * FROM Item WHERE 1=1"
        query_params = []

        if 'item_name' in params:
            query += " AND item_name LIKE %s"
            query_params.append(f"%{params['item_name']}%")
        if 'item_group' in params:
            query += " AND item_group LIKE %s"
            query_params.append(f"%{params['item_group']}%")
        if 'brand' in params:
            query += " AND brand LIKE %s"
            query_params.append(f"%{params['brand']}%")
        if 'item_sku' in params:
            query += " AND item_sku LIKE %s"
            query_params.append(f"%{params['item_sku']}%")

        cur.execute(query, query_params)
        items = cur.fetchall()

        if not items:
            return jsonify({"message": "No items found"}), 404

        # Map results to a list of dictionaries
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, item)) for item in items]

        return jsonify(result), 200
    except Exception as e:
        print(f"Error reading items: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Update an item
@item_routes.route('/<item_sku>', methods=['PUT'])
def update_item(item_sku):
    data = request.json

    # Validate input
    validation_result = validate_update_item(data)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the item exists
        check_query = "SELECT item_sku FROM Item WHERE item_sku = %s"
        cur.execute(check_query, (item_sku,))
        if not cur.fetchone():
            return jsonify({"message": "Item not found"}), 404

        # Build the update query dynamically
        update_fields = ", ".join([f"{field} = %s" for field in data.keys()])
        update_values = list(data.values()) + [item_sku]

        update_query = f"UPDATE Item SET {update_fields} WHERE item_sku = %s"
        cur.execute(update_query, update_values)
        conn.commit()

        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        print(f"Error updating item: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Delete an item
@item_routes.route('/<item_sku>', methods=['DELETE'])
def delete_item(item_sku):
    # Validate input
    validation_result = validate_delete_item(item_sku)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the item exists
        check_query = "SELECT item_sku FROM Item WHERE item_sku = %s"
        cur.execute(check_query, (item_sku,))
        if not cur.fetchone():
            return jsonify({"message": "Item not found"}), 404

        # Delete the item
        delete_query = "DELETE FROM Item WHERE item_sku = %s"
        cur.execute(delete_query, (item_sku,))
        conn.commit()

        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting item: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()
