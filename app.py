from flask import Flask
from utility.db import get_db_connection
from routes.routes_item import item_routes
from routes.routes_user import user_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(item_routes, url_prefix="/items")
app.register_blueprint(user_routes, url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=True)
