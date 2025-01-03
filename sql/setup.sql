-- Create the Item table
CREATE TABLE Item (
    item_sku VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    item_uom VARCHAR(20),
    item_group VARCHAR(50),
    retail_price DECIMAL(10, 2),
    purchase_price DECIMAL(10, 2),
    warranty_period INT,
    is_stock_item BOOLEAN,
    brand VARCHAR(50),
    description TEXT,
    single_unit_dimensions VARCHAR(100),
    single_unit_weight DECIMAL(10, 2),
    weight_uom VARCHAR(20),
    country_of_origin VARCHAR(50),
    barcode VARCHAR(50),
    barcode_type VARCHAR(20)
);

-- Create the Warehouse table
CREATE TABLE Warehouse (
    warehouse_id VARCHAR(50) PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    warehouse_address TEXT,
    warehouse_city VARCHAR(50),
    warehouse_state VARCHAR(50),
    warehouse_zipcode VARCHAR(20),
    warehouse_country VARCHAR(50)
);

-- Create the In_Inventory table
CREATE TABLE In_Inventory (
    item_sku VARCHAR(50),
    warehouse_id VARCHAR(50),
    item_quantity INT,
    opening_stock INT,
    case_quantity INT,
    case_dimensions VARCHAR(100),
    case_weight DECIMAL(10, 2),
    PRIMARY KEY (item_sku, warehouse_id),
    FOREIGN KEY (item_sku) REFERENCES Item(item_sku),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
);

-- Create the Customer table
CREATE TABLE Customer (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_sku VARCHAR(50) UNIQUE,
    customer_name VARCHAR(100) NOT NULL,
    customer_address TEXT,
    customer_city VARCHAR(50),
    customer_state VARCHAR(50),
    customer_zipcode VARCHAR(20),
    customer_country VARCHAR(50)
);

-- Create the Transaction table
CREATE TABLE Transaction (
    item_sku VARCHAR(50),
    warehouse_id VARCHAR(50),
    customer_id VARCHAR(50),
    date DATE NOT NULL,
    sales_uom VARCHAR(20),
    transaction_quantity INT NOT NULL,
    shipping_address TEXT,
    shipping_city VARCHAR(50),
    shipping_state VARCHAR(50),
    shipping_zipcode VARCHAR(20),
    shipping_country VARCHAR(50),
    PRIMARY KEY (item_sku, warehouse_id, customer_id),
    FOREIGN KEY (item_sku) REFERENCES Item(item_sku),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Create the User table
CREATE TABLE User (
    user_id VARCHAR(50) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_role VARCHAR(50),
    pass_hash VARCHAR(255) NOT NULL
);
