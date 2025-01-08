import requests

BASE_URL = "http://127.0.0.1:5000"

def show_main_menu():
    print("\n=== Inventory Management ===")
    print("1. Item Management")
    print("2. User Management")
    print("3. Transaction Management")
    print("4. Exit")
    return input("Choose an option: ")

def show_item_menu():
    print("\n--- Item Management ---")
    print("1. Create Item")
    print("2. View Items")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Back to Main Menu")
    return input("Choose an option: ")

def show_user_menu():
    print("\n--- User Management ---")
    print("1. Create User")
    print("2. View Users")
    print("3. Update User")
    print("4. Delete User")
    print("5. Back to Main Menu")
    return input("Choose an option: ")

def show_transaction_menu():
    print("\n--- Transaction Management ---")
    print("1. Create Purchase")
    print("2. Update Purchase")
    print("3. Process Return")
    print("4. Back to Main Menu")
    return input("Choose an option: ")

### Item Management ###
def create_item():
    print("\n--- Create Item ---")
    data = {
        "item_sku": input("Item SKU: "),
        "item_name": input("Item Name: "),
        "item_uom": input("Unit of Measure: "),
        "item_group": input("Item Group: "),
        "retail_price": float(input("Retail Price: ")),
        "purchase_price": float(input("Purchase Price: ")),
        "warranty_period": int(input("Warranty Period (months): ")),
        "is_stock_item": input("Is Stock Item (true/false): ").lower() == "true",
        "brand": input("Brand: "),
        "description": input("Description: "),
        "single_unit_dimensions": input("Single Unit Dimensions (e.g., '10x10x10'): "),
        "single_unit_weight": float(input("Single Unit Weight (lbs): ")),
        "weight_uom": input("Weight Unit of Measure: "),
        "country_of_origin": input("Country of Origin: "),
        "barcode": input("Barcode: "),
        "barcode_type": input("Barcode Type: ")
    }

    response = requests.post(f"{BASE_URL}/items", json=data)
    if response.status_code == 201:
        print("Item created successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def view_items():
    print("\n--- View Items ---")
    params = {}
    while True:
        field = input("Enter search field (item_name, item_group, brand, item_sku) or 'done' to finish: ")
        if field.lower() == "done":
            break
        value = input(f"Enter value for {field}: ")
        params[field] = value

    response = requests.get(f"{BASE_URL}/items", params=params)
    if response.status_code == 200:
        items = response.json()
        for item in items:
            print(item)
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def update_item():
    print("\n--- Update Item ---")
    item_sku = input("Enter the Item SKU to update: ")
    data = {}
    while True:
        field = input("Field to update (or 'done' to finish): ")
        if field.lower() == "done":
            break
        value = input(f"New value for {field}: ")
        data[field] = value

    response = requests.put(f"{BASE_URL}/items/{item_sku}", json=data)
    if response.status_code == 200:
        print("Item updated successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def delete_item():
    print("\n--- Delete Item ---")
    item_sku = input("Enter the Item SKU to delete: ")
    response = requests.delete(f"{BASE_URL}/items/{item_sku}")
    if response.status_code == 200:
        print("Item deleted successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

### User Management ###
def create_user():
    print("\n--- Create User ---")
    data = {
        "user_id": input("User ID: "),
        "user_name": input("User Name: "),
        "user_role": input("User Role (admin/employee): "),
        "pass_hash": input("Password Hash: ")
    }

    response = requests.post(f"{BASE_URL}/users", json=data)
    if response.status_code == 201:
        print("User created successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def view_users():
    print("\n--- View Users ---")
    params = {}
    while True:
        field = input("Enter search field (user_name, user_role, user_id) or 'done' to finish: ")
        if field.lower() == "done":
            break
        value = input(f"Enter value for {field}: ")
        params[field] = value

    response = requests.get(f"{BASE_URL}/users", params=params)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(user)
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def update_user():
    print("\n--- Update User ---")
    user_id = input("Enter the User ID to update: ")
    data = {}
    while True:
        field = input("Field to update (or 'done' to finish): ")
        if field.lower() == "done":
            break
        value = input(f"New value for {field}: ")
        data[field] = value

    response = requests.put(f"{BASE_URL}/users/{user_id}", json=data)
    if response.status_code == 200:
        print("User updated successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def delete_user():
    print("\n--- Delete User ---")
    user_id = input("Enter the User ID to delete: ")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        print("User deleted successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

### Transaction Management ###
def create_purchase():
    print("\n--- Create Purchase ---")
    data = {
        "item_sku": input("Item SKU: "),
        "warehouse_id": input("Warehouse ID: "),
        "customer_id": input("Customer ID: "),
        "date": input("Transaction Date (YYYY-MM-DD): "),
        "sales_uom": input("Sales Unit of Measure: "),
        "transaction_quantity": int(input("Transaction Quantity: ")),
        "shipping_address": input("Shipping Address: "),
        "shipping_city": input("Shipping City: "),
        "shipping_state": input("Shipping State: "),
        "shipping_zipcode": input("Shipping Zipcode: "),
        "shipping_country": input("Shipping Country: "),
        "transaction_image": input("Transaction Image (optional): ") or None,
        "transaction_barcode": input("Transaction Barcode (optional): ") or None,
        "transaction_weight": float(input("Transaction Weight (optional): ") or 0),
        "tracking_information": input("Tracking Information (optional): ") or None
    }

    response = requests.post(f"{BASE_URL}/transactions/purchase", json=data)
    if response.status_code == 201:
        print("Purchase created successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def update_purchase():
    print("\n--- Update Purchase ---")
    item_sku = input("Enter the Item SKU: ")
    warehouse_id = input("Enter the Warehouse ID: ")
    customer_id = input("Enter the Customer ID: ")
    data = {}
    while True:
        field = input("Field to update (or 'done' to finish): ")
        if field.lower() == "done":
            break
        value = input(f"New value for {field}: ")
        data[field] = value

    response = requests.put(f"{BASE_URL}/transactions/purchase/{item_sku}/{warehouse_id}/{customer_id}", json=data)
    if response.status_code == 200:
        print("Purchase updated successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

def process_return():
    print("\n--- Process Return ---")
    item_sku = input("Enter the Item SKU: ")
    warehouse_id = input("Enter the Warehouse ID: ")
    customer_id = input("Enter the Customer ID: ")
    data = {"return_quantity": int(input("Return Quantity: "))}

    response = requests.post(f"{BASE_URL}/transactions/return/{item_sku}/{warehouse_id}/{customer_id}", json=data)
    if response.status_code == 200:
        print("Return processed successfully!")
    else:
        print(f"Error: {response.json().get('message', 'Unknown error')}")

### Main Execution ###
def main():
    while True:
        choice = show_main_menu()
        if choice == "1":
            while True:
                item_choice = show_item_menu()
                if item_choice == "1":
                    create_item()
                elif item_choice == "2":
                    view_items()
                elif item_choice == "3":
                    update_item()
                elif item_choice == "4":
                    delete_item()
                elif item_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "2":
            while True:
                user_choice = show_user_menu()
                if user_choice == "1":
                    create_user()
                elif user_choice == "2":
                    view_users()
                elif user_choice == "3":
                    update_user()
                elif user_choice == "4":
                    delete_user()
                elif user_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            while True:
                transaction_choice = show_transaction_menu()
                if transaction_choice == "1":
                    create_purchase()
                elif transaction_choice == "2":
                    update_purchase()
                elif transaction_choice == "3":
                    process_return()
                elif transaction_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
