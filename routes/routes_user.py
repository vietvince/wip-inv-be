import logging
from flask import Blueprint, request, jsonify
from validations.validate_user import validate_create_user, validate_update_user, validate_read_user_params, validate_delete_user
from utility.db import get_db_connection

user_routes = Blueprint("user_routes", __name__)

# Create a user
@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.json
    logging.info("Received request to create user with data: %s", data)

    # Validate input
    validation_result = validate_create_user(data)
    if validation_result['error']:
        logging.warning("Validation failed for creating user: %s", validation_result)
        return jsonify({
            "message": validation_result['message'],
            "fields": validation_result.get('fields')
        }), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the user already exists
        check_query = "SELECT user_id FROM User WHERE user_id = %s"
        cur.execute(check_query, (data['user_id'],))
        if cur.fetchone():
            logging.warning("User already exists with ID: %s", data['user_id'])
            return jsonify({"message": "User already exists"}), 409

        # Insert the new user
        insert_query = """
            INSERT INTO User (user_id, user_name, user_role, pass_hash)
            VALUES (%s, %s, %s, %s)
        """
        logging.debug("Executing insert query: %s with values: %s", insert_query, data)
        cur.execute(insert_query, (
            data['user_id'], data['user_name'], data['user_role'], data['pass_hash']
        ))
        conn.commit()

        logging.info("User created successfully with ID: %s", data['user_id'])
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logging.error("Error creating user with ID: %s, Error: %s", data['user_id'], str(e), exc_info=True)
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Read users
@user_routes.route('/', methods=['GET'])
def read_users():
    params = request.args.to_dict()
    logging.info("Received request to read users with parameters: %s", params)

    # Validate input
    validation_result = validate_read_user_params(params)
    if validation_result['error']:
        logging.warning("Validation failed for reading users: %s", validation_result)
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Base query
        query = "SELECT * FROM User WHERE 1=1"
        query_params = []

        if 'user_name' in params:
            query += " AND user_name LIKE %s"
            query_params.append(f"%{params['user_name']}%")
        if 'user_role' in params:
            query += " AND user_role = %s"
            query_params.append(params['user_role'])
        if 'user_id' in params:
            query += " AND user_id = %s"
            query_params.append(params['user_id'])

        logging.debug("Executing query: %s with parameters: %s", query, query_params)
        cur.execute(query, query_params)
        users = cur.fetchall()

        if not users:
            logging.info("No users found for parameters: %s", params)
            return jsonify({"message": "No users found"}), 404

        # Map results to a list of dictionaries
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, user)) for user in users]

        logging.info("Users retrieved successfully. Count: %d", len(result))
        return jsonify(result), 200
    except Exception as e:
        logging.error("Error reading users, Error: %s", str(e), exc_info=True)
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Update a user
@user_routes.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    logging.info("Received request to update user with ID: %s, Data: %s", user_id, data)

    # Validate input
    validation_result = validate_update_user(data)
    if validation_result['error']:
        logging.warning("Validation failed for updating user with ID: %s, Error: %s", user_id, validation_result)
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the user exists
        check_query = "SELECT user_id FROM User WHERE user_id = %s"
        cur.execute(check_query, (user_id,))
        if not cur.fetchone():
            logging.warning("User not found with ID: %s", user_id)
            return jsonify({"message": "User not found"}), 404

        # Build the update query dynamically
        update_fields = ", ".join([f"{field} = %s" for field in data.keys()])
        update_values = list(data.values()) + [user_id]

        update_query = f"UPDATE User SET {update_fields} WHERE user_id = %s"
        logging.debug("Executing update query: %s with values: %s", update_query, update_values)
        cur.execute(update_query, update_values)
        conn.commit()

        logging.info("User updated successfully with ID: %s", user_id)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        logging.error("Error updating user with ID: %s, Error: %s", user_id, str(e), exc_info=True)
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Delete a user
@user_routes.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    logging.info("Received request to delete user with ID: %s", user_id)

    # Validate input
    validation_result = validate_delete_user(user_id)
    if validation_result['error']:
        logging.warning("Validation failed for deleting user with ID: %s, Error: %s", user_id, validation_result)
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the user exists
        check_query = "SELECT user_id FROM User WHERE user_id = %s"
        cur.execute(check_query, (user_id,))
        if not cur.fetchone():
            logging.warning("User not found with ID: %s", user_id)
            return jsonify({"message": "User not found"}), 404

        # Delete the user
        delete_query = "DELETE FROM User WHERE user_id = %s"
        logging.debug("Executing delete query: %s with ID: %s", delete_query, user_id)
        cur.execute(delete_query, (user_id,))
        conn.commit()

        logging.info("User deleted successfully with ID: %s", user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        logging.error("Error deleting user with ID: %s, Error: %s", user_id, str(e), exc_info=True)
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()
