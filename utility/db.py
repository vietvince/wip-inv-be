import mysql.connector

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'inventory_database',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection
