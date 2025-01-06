from flask import Blueprint, request, jsonify
from validations.validate_user import validate_create_user, validate_update_user, validate_read_user_params, validate_delete_user
from utility.db import get_db_connection

user_routes = Blueprint("user_routes", __name__)

# Create a user
@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.json

    # Validate input
    validation_result = validate_create_user(data)
    if validation_result['error']:
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
            return jsonify({"message": "User already exists"}), 409

        # Insert the new user
        insert_query = """
            INSERT INTO User (user_id, user_name, user_role, pass_hash)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_query, (
            data['user_id'], data['user_name'], data['user_role'], data['pass_hash']
        ))
        conn.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Read users
@user_routes.route('/', methods=['GET'])
def read_users():
    params = request.args.to_dict()

    # Validate input
    validation_result = validate_read_user_params(params)
    if validation_result['error']:
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

        cur.execute(query, query_params)
        users = cur.fetchall()

        if not users:
            return jsonify({"message": "No users found"}), 404

        # Map results to a list of dictionaries
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, user)) for user in users]

        return jsonify(result), 200
    except Exception as e:
        print(f"Error reading users: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()

# Update a user
@user_routes.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    # Validate input
    validation_result = validate_update_user(data)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the user exists
        check_query = "SELECT user_id FROM User WHERE user_id = %s"
        cur.execute(check_query, (user_id,))
        if not cur.fetchone():
            return jsonify({"message": "User not found"}), 404

        # Build the update query dynamically
        update_fields = ", ".join([f"{field} = %s" for field in data.keys()])
        update_values = list(data.values()) + [user_id]

        update_query = f"UPDATE User SET {update_fields} WHERE user_id = %s"
        cur.execute(update_query, update_values)
        conn.commit()

        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close

# Delete a user
@user_routes.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Validate input
    validation_result = validate_delete_user(user_id)
    if validation_result['error']:
        return jsonify({"message": validation_result['message']}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the user exists
        check_query = "SELECT user_id FROM User WHERE user_id = %s"
        cur.execute(check_query, (user_id,))
        if not cur.fetchone():
            return jsonify({"message": "User not found"}), 404

        # Delete the user
        delete_query = "DELETE FROM User WHERE user_id = %s"
        cur.execute(delete_query, (user_id,))
        conn.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    finally:
        cur.close()
        conn.close()
