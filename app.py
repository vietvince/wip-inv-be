from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Database Configuration
db_config = {
    'host': 'localhost',  # Replace with your MariaDB host
    'user': 'root',  # Replace with your database username
    'password': 'root',  # Replace with your database password
    'database': 'inventory_database',  # Replace with your database name
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Establish a database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/users', methods=['GET'])
def get_users():
    """
    Fetch all users from the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")  # Replace `users` with your table name
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

@app.route('/user', methods=['POST'])
def add_user():
    """
    Add a new user to the database.
    """
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "User added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
