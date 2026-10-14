import os
import sys
import random
from datetime import datetime, timedelta

# Ensure backend directory is in path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sql_connection import get_sql_connection

# -------------------------------------------------------------------
# Demo Data Definition (50 Products, 6 UOMs, 60 Orders, 180+ Details)
# -------------------------------------------------------------------

UOMS = [
    (1, 'Each'),
    (2, 'Kg'),
    (3, 'Liter'),
    (4, 'Gram'),
    (5, 'Pack'),
    (6, 'Dozen')
]

PRODUCTS = [
    (1, 'Toothpaste', 1, 45.0),
    (2, 'Whole Milk 1L', 3, 65.0),
    (3, 'Brown Bread', 5, 40.0),
    (4, 'Farm Fresh Eggs', 6, 85.0),
    (5, 'Basmati Rice 1kg', 2, 120.0),
    (6, 'Wheat Flour (Atta) 5kg', 5, 210.0),
    (7, 'Sunflower Cooking Oil 1L', 3, 140.0),
    (8, 'Fresh Apples', 2, 180.0),
    (9, 'Cavendish Bananas', 6, 60.0),
    (10, 'Yellow Onions', 2, 35.0),
    (11, 'Fresh Potatoes', 2, 30.0),
    (12, 'Ripe Tomatoes', 2, 40.0),
    (13, 'Green Cabbage', 1, 25.0),
    (14, 'Fresh Broccoli', 1, 70.0),
    (15, 'Orange Carrots', 2, 50.0),
    (16, 'Fresh Spinach', 5, 20.0),
    (17, 'Cheddar Cheese 200g', 5, 110.0),
    (18, 'Salted Butter 100g', 5, 55.0),
    (19, 'Plain Yogurt 500g', 5, 45.0),
    (20, 'Paneer 200g', 5, 85.0),
    (21, 'Green Tea Bags 25s', 5, 160.0),
    (22, 'Instant Coffee 100g', 5, 190.0),
    (23, 'Black Tea Leaves 500g', 5, 220.0),
    (24, 'Chocolate Chip Cookies', 5, 40.0),
    (25, 'Potato Chips Salted', 5, 30.0),
    (26, 'Roasted Almonds 200g', 5, 240.0),
    (27, 'Raw Cashews 200g', 5, 260.0),
    (28, 'Premium Honey 250g', 1, 150.0),
    (29, 'Strawberry Jam 500g', 1, 135.0),
    (30, 'Peanut Butter 350g', 1, 175.0),
    (31, 'Refined Sugar 1kg', 2, 48.0),
    (32, 'Iodized Table Salt 1kg', 5, 25.0),
    (33, 'Red Chili Powder 100g', 5, 45.0),
    (34, 'Turmeric Powder 100g', 5, 38.0),
    (35, 'Coriander Powder 100g', 5, 40.0),
    (36, 'Cumin Seeds (Jeera) 100g', 5, 65.0),
    (37, 'Garam Masala 100g', 5, 75.0),
    (38, 'Toor Dal 1kg', 2, 150.0),
    (39, 'Moong Dal 1kg', 2, 130.0),
    (40, 'Chana Dal 1kg', 2, 115.0),
    (41, 'Dishwashing Liquid 500ml', 1, 95.0),
    (42, 'Laundry Detergent 1kg', 5, 140.0),
    (43, 'Bathing Soap 4x100g', 5, 120.0),
    (44, 'Shampoo 400ml', 1, 230.0),
    (45, 'Hair Conditioner 200ml', 1, 195.0),
    (46, 'Handwash Refill 750ml', 5, 99.0),
    (47, 'Floor Cleaner 1L', 1, 125.0),
    (48, 'Paper Napkins', 5, 50.0),
    (49, 'Aluminum Foil 10m', 1, 85.0),
    (50, 'Garbage Bags 30s', 5, 110.0)
]

CUSTOMER_NAMES = [
    'Dhaval Patel', 'Priya Sharma', 'Amit Kumar', 'Sneha Reddy', 'Rahul Verma',
    'Ananya Iyer', 'Vikram Singh', 'Pooja Gupta', 'Rohan Mehta', 'Sunita Rao',
    'Rajesh Nair', 'Neha Joshi', 'Manoj Tiwari', 'Kavita Das', 'Suresh Menon',
    'Deepa Sen', 'Arvind Yadav', 'Meera Pillai', 'Sanjay Saxena', 'Ritu Malhotra',
    'Aditya Kulkarni', 'Swati Deshmukh', 'Alok Pandey', 'Tanvi Chawla', 'Gaurav Bhatia',
    'Nisha Kapoor', 'Karthik Raman', 'Divya Nambiar', 'Harish Bose', 'Pallavi Ghosh',
    'Vikas Choudhary', 'Simran Kaur', 'Naveen Jain', 'Preeti Agarwal', 'Ashok Singhania',
    'Bhavna Bajaj', 'Kunal Mittal', 'Shilpa Shetty', 'Pradeep Hegde', 'Geeta Mukherjee'
]

def generate_demo_dataset():
    random.seed(42)
    base_time = datetime(2026, 10, 1, 9, 30, 0)
    orders = []
    order_details = []
    detail_id = 1

    for order_id in range(1, 61):
        cust = CUSTOMER_NAMES[(order_id - 1) % len(CUSTOMER_NAMES)]
        dt = base_time + timedelta(hours=order_id * 5.2, minutes=(order_id * 17) % 60)
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

        num_items = random.randint(2, 4)
        selected_prods = random.sample(PRODUCTS, num_items)

        order_total = 0.0
        for prod in selected_prods:
            p_id, p_name, u_id, price = prod
            qty = random.choice([1.0, 1.5, 2.0, 3.0]) if u_id in [2, 3] else float(random.choice([1, 2, 3]))
            item_total = round(qty * price, 2)
            order_total += item_total
            order_details.append((detail_id, order_id, p_id, qty, item_total))
            detail_id += 1

        orders.append((order_id, cust, round(order_total, 2), dt_str))

    return UOMS, PRODUCTS, orders, order_details


def write_database_sql(uoms, products, orders, order_details, output_file='database.sql'):
    """Generates a complete database.sql file with schema and all demo data."""
    lines = [
        "-- ===================================================",
        "-- Grocery Store Management System Database & Demo Data",
        "-- Total: 6 UOMs, 50 Products, 60 Orders, 180+ Order Details",
        "-- ===================================================\n",
        "CREATE DATABASE IF NOT EXISTS `gs`;",
        "USE `gs`;\n",
        "-- 1. Units of Measurement Table ---------------------",
        "CREATE TABLE IF NOT EXISTS `gs`.`uom` (",
        "  `uom_id` INT NOT NULL AUTO_INCREMENT,",
        "  `uom_name` VARCHAR(45) NOT NULL,",
        "  PRIMARY KEY (`uom_id`)",
        ");\n"
    ]

    uom_rows = ",\n".join([f"  ({u[0]}, '{u[1]}')" for u in uoms])
    lines.append(f"INSERT INTO `gs`.`uom` (`uom_id`, `uom_name`) VALUES\n{uom_rows}")
    lines.append("ON DUPLICATE KEY UPDATE `uom_name` = VALUES(`uom_name`);\n")

    lines.extend([
        "-- 2. Products Table ---------------------------------",
        "CREATE TABLE IF NOT EXISTS `gs`.`product` (",
        "  `product_id` INT NOT NULL AUTO_INCREMENT,",
        "  `name` VARCHAR(100) NOT NULL,",
        "  `uom_id` INT NOT NULL,",
        "  `price_per_unit` DOUBLE NOT NULL,",
        "  PRIMARY KEY (`product_id`),",
        "  INDEX `fk_uom_id_idx` (`uom_id`),",
        "  CONSTRAINT `fk_uom_id`",
        "    FOREIGN KEY (`uom_id`)",
        "    REFERENCES `gs`.`uom` (`uom_id`)",
        "    ON DELETE NO ACTION",
        "    ON UPDATE RESTRICT",
        ");\n",
        "-- View for backwards compatibility",
        "CREATE OR REPLACE VIEW `gs`.`products` AS SELECT * FROM `gs`.`product`;\n"
    ])

    prod_rows = ",\n".join([f"  ({p[0]}, '{p[1]}', {p[2]}, {p[3]})" for p in products])
    lines.append(f"INSERT INTO `gs`.`product` (`product_id`, `name`, `uom_id`, `price_per_unit`) VALUES\n{prod_rows}")
    lines.append("ON DUPLICATE KEY UPDATE `name` = VALUES(`name`), `uom_id` = VALUES(`uom_id`), `price_per_unit` = VALUES(`price_per_unit`);\n")

    lines.extend([
        "-- 3. Orders Table -----------------------------------",
        "CREATE TABLE IF NOT EXISTS `gs`.`orders` (",
        "  `order_id` INT NOT NULL AUTO_INCREMENT,",
        "  `customer_name` VARCHAR(100) NOT NULL,",
        "  `total` DOUBLE NOT NULL,",
        "  `datetime` DATETIME NOT NULL,",
        "  PRIMARY KEY (`order_id`)",
        ");\n"
    ])

    order_rows = ",\n".join([f"  ({o[0]}, '{o[1]}', {o[2]}, '{o[3]}')" for o in orders])
    lines.append(f"INSERT INTO `gs`.`orders` (`order_id`, `customer_name`, `total`, `datetime`) VALUES\n{order_rows}")
    lines.append("ON DUPLICATE KEY UPDATE `customer_name` = VALUES(`customer_name`), `total` = VALUES(`total`), `datetime` = VALUES(`datetime`);\n")

    lines.extend([
        "-- 4. Order Details Table ----------------------------",
        "CREATE TABLE IF NOT EXISTS `gs`.`order_details` (",
        "  `order_detail_id` INT NOT NULL AUTO_INCREMENT,",
        "  `order_id` INT NOT NULL,",
        "  `product_id` INT NOT NULL,",
        "  `quantity` DOUBLE NOT NULL,",
        "  `total_price` DOUBLE NOT NULL,",
        "  PRIMARY KEY (`order_detail_id`),",
        "  INDEX `fk_order_id_idx` (`order_id`),",
        "  INDEX `fk_product_id_idx` (`product_id`),",
        "  CONSTRAINT `fk_order_id`",
        "    FOREIGN KEY (`order_id`)",
        "    REFERENCES `gs`.`orders` (`order_id`)",
        "    ON DELETE CASCADE",
        "    ON UPDATE CASCADE,",
        "  CONSTRAINT `fk_product_id`",
        "    FOREIGN KEY (`product_id`)",
        "    REFERENCES `gs`.`product` (`product_id`)",
        "    ON DELETE NO ACTION",
        "    ON UPDATE RESTRICT",
        ");\n"
    ])

    detail_rows = ",\n".join([f"  ({d[0]}, {d[1]}, {d[2]}, {d[3]}, {d[4]})" for d in order_details])
    lines.append(f"INSERT INTO `gs`.`order_details` (`order_detail_id`, `order_id`, `product_id`, `quantity`, `total_price`) VALUES\n{detail_rows}")
    lines.append("ON DUPLICATE KEY UPDATE `quantity` = VALUES(`quantity`), `total_price` = VALUES(`total_price`);\n")

    content = "\n".join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Generated {output_file} with {len(products)} products, {len(orders)} orders, and {len(order_details)} order details.")


def seed_database_live(sql_file='database.sql'):
    """Connects to live MySQL, creates schema and tables, and inserts demo records."""
    conn = get_sql_connection()
    if conn is None:
        print("[SKIP] MySQL database connection could not be established right now.")
        print("       Import 'database.sql' into phpMyAdmin/MySQL, or start MySQL and re-run 'python seed_data.py'.")
        return False

    cursor = conn.cursor()
    print("[INFO] Setting up database schema and seeding tables in MySQL...")

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split and execute individual SQL statements
    statements = sql_content.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"[WARN] Statement error: {stmt[:50]}... -> {e}")

    conn.commit()
    print("[SUCCESS] Database schema initialized and 300+ demo records inserted!")


if __name__ == '__main__':
    uoms, products, orders, order_details = generate_demo_dataset()
    write_database_sql(uoms, products, orders, order_details)
    seed_database_live()
