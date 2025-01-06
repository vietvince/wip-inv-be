from flask import Blueprint, request, jsonify
from validations.validate_transaction import validate_purchase, validate_update_purchase, validate_return
from utility.db import get_db_connection

transaction_routes = Blueprint("transaction_routes", __name__)

# Purchase Route
@transaction_routes.route('/purchase', methods=['POST'])
def purchase():
    data = request.json

    # Validate input
    validation_result = validate_purchase(data)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the new transaction
        insert_query = """
            INSERT INTO Transaction (
                item_sku, warehouse_id, customer_id, date, sales_uom, transaction_quantity,
                shipping_address, shipping_city, shipping_state, shipping_zipcode,
                shipping_country, transaction_image, transaction_barcode, transaction_weight, tracking_information
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        cur.execute(insert_query, (
            data['item_sku'], data['warehouse_id'], data['customer_id'], data['date'],
            data['sales_uom'], data['transaction_quantity'], data['shipping_address'],
            data['shipping_city'], data['shipping_state'], data['shipping_zipcode'],
            data['shipping_country'], data.get('transaction_image'), data.get('transaction_barcode'),
            data.get('transaction_weight'), data.get('tracking_information')
        ))
        conn.commit()

        return jsonify({"message": "Transaction created successfully"}), 201
    except Exception as e:
        print(f"Error creating transaction: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Update Purchase Route
@transaction_routes.route('/purchase/<item_sku>/<warehouse_id>/<customer_id>', methods=['PUT'])
def update_purchase(item_sku, warehouse_id, customer_id):
    data = request.json

    # Validate input
    validation_result = validate_update_purchase(data)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the transaction exists
        check_query = """
            SELECT * FROM Transaction 
            WHERE item_sku = %s AND warehouse_id = %s AND customer_id = %s
        """
        cur.execute(check_query, (item_sku, warehouse_id, customer_id))
        if not cur.fetchone():
            return jsonify({"message": "Transaction not found"}), 404

        # Build the update query dynamically
        update_fields = ", ".join([f"{key} = %s" for key in data.keys()])
        update_query = f"""
            UPDATE Transaction
            SET {update_fields}
            WHERE item_sku = %s AND warehouse_id = %s AND customer_id = %s
        """
        cur.execute(update_query, list(data.values()) + [item_sku, warehouse_id, customer_id])
        conn.commit()

        return jsonify({"message": "Transaction updated successfully"}), 200
    except Exception as e:
        print(f"Error updating transaction: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Return Route
@transaction_routes.route('/return/<item_sku>/<warehouse_id>/<customer_id>', methods=['POST'])
def return_item(item_sku, warehouse_id, customer_id):
    data = request.json

    # Validate input
    validation_result = validate_return(data)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the transaction exists
        check_query = """
            SELECT transaction_quantity FROM Transaction 
            WHERE item_sku = %s AND warehouse_id = %s AND customer_id = %s
        """
        cur.execute(check_query, (item_sku, warehouse_id, customer_id))
        result = cur.fetchone()
        if not result:
            return jsonify({"message": "Transaction not found"}), 404

        current_quantity = result[0]
        if data['return_quantity'] > current_quantity:
            return jsonify({"message": "Return quantity cannot exceed transaction quantity"}), 400

        # Process the return
        update_query = """
            UPDATE Transaction
            SET transaction_quantity = transaction_quantity - %s
            WHERE item_sku = %s AND warehouse_id = %s AND customer_id = %s
        """
        cur.execute(update_query, (
            data['return_quantity'], item_sku, warehouse_id, customer_id
        ))
        conn.commit()

        return jsonify({"message": "Transaction return processed successfully"}), 200
    except Exception as e:
        print(f"Error processing return: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()