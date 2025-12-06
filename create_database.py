"""
Database initialization script with realistic, comprehensive data.
Creates tables for: employees, departments, products, customers, orders, order_items,
customer_notes, and chat_history.
"""
import sqlite3
from datetime import datetime, timedelta
import random


def create_comprehensive_database(db_path: str = "database/test_db.sqlite"):
    """
    Create a comprehensive database with realistic business data.
    
    Tables:
    - employees: Company staff information
    - departments: Department structure
    - products: Product catalog
    - customers: Customer information
    - orders: Order transactions
    - order_items: Order line items
    - customer_notes: Customer interaction notes
    - chat_history: Customer service chat logs
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS chat_history")
    cursor.execute("DROP TABLE IF EXISTS customer_notes")
    cursor.execute("DROP TABLE IF EXISTS order_items")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS departments")
    
    print("🗑️  Dropped existing tables...")
    
    # ========================================================================
    # DEPARTMENTS TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            budget REAL NOT NULL,
            manager_id INTEGER,
            location TEXT,
            created_date TEXT NOT NULL
        )
    """)
    
    departments_data = [
        (1, "Engineering", 750000, 1, "San Francisco", "2018-01-15"),
        (2, "Sales", 450000, 4, "New York", "2018-01-15"),
        (3, "Marketing", 350000, 7, "Austin", "2018-06-01"),
        (4, "Customer Support", 280000, 10, "Remote", "2019-03-15"),
        (5, "Product Management", 420000, 13, "San Francisco", "2019-08-01"),
        (6, "Human Resources", 220000, 16, "New York", "2018-01-15"),
        (7, "Finance", 320000, 18, "New York", "2018-01-15")
    ]
    
    cursor.executemany("""
        INSERT INTO departments VALUES (?, ?, ?, ?, ?, ?)
    """, departments_data)
    
    print("✅ Created departments table (7 departments)")
    
    # ========================================================================
    # EMPLOYEES TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            hire_date TEXT NOT NULL,
            manager_id INTEGER,
            status TEXT DEFAULT 'active'
        )
    """)
    
    employees_data = [
        # Engineering
        (1, "Alice Johnson", "alice.j@company.com", "Engineering", "Senior Software Engineer", 145000, "2019-01-15", None, "active"),
        (2, "Bob Smith", "bob.s@company.com", "Engineering", "Software Engineer", 115000, "2020-03-20", 1, "active"),
        (3, "Carol Davis", "carol.d@company.com", "Engineering", "DevOps Engineer", 125000, "2019-11-10", 1, "active"),
        (4, "David Brown", "david.b@company.com", "Engineering", "Frontend Developer", 105000, "2021-06-15", 1, "active"),
        (5, "Eve Wilson", "eve.w@company.com", "Engineering", "Backend Developer", 118000, "2020-09-01", 1, "active"),
        (6, "Frank Miller", "frank.m@company.com", "Engineering", "QA Engineer", 95000, "2021-02-12", 1, "active"),
        
        # Sales
        (7, "Grace Lee", "grace.l@company.com", "Sales", "Sales Director", 135000, "2018-04-10", None, "active"),
        (8, "Henry Taylor", "henry.t@company.com", "Sales", "Account Executive", 92000, "2019-08-20", 7, "active"),
        (9, "Iris Anderson", "iris.a@company.com", "Sales", "Sales Representative", 78000, "2020-11-05", 7, "active"),
        (10, "Jack Thomas", "jack.t@company.com", "Sales", "Business Development", 88000, "2021-01-18", 7, "active"),
        
        # Marketing
        (11, "Karen Martinez", "karen.m@company.com", "Marketing", "Marketing Manager", 108000, "2019-05-15", None, "active"),
        (12, "Leo Garcia", "leo.g@company.com", "Marketing", "Content Specialist", 72000, "2020-07-22", 11, "active"),
        (13, "Maya Robinson", "maya.r@company.com", "Marketing", "Social Media Manager", 68000, "2021-03-10", 11, "active"),
        
        # Customer Support
        (14, "Nathan Clark", "nathan.c@company.com", "Customer Support", "Support Manager", 95000, "2019-09-01", None, "active"),
        (15, "Olivia Lewis", "olivia.l@company.com", "Customer Support", "Support Specialist", 58000, "2020-04-15", 14, "active"),
        (16, "Paul Walker", "paul.w@company.com", "Customer Support", "Support Specialist", 56000, "2020-12-01", 14, "active"),
        (17, "Quinn Hall", "quinn.h@company.com", "Customer Support", "Technical Support", 65000, "2021-05-20", 14, "active"),
        
        # Product Management
        (18, "Rachel Young", "rachel.y@company.com", "Product Management", "Product Manager", 128000, "2019-10-10", None, "active"),
        (19, "Steve King", "steve.k@company.com", "Product Management", "Product Owner", 112000, "2020-08-15", 18, "active"),
        
        # Human Resources
        (20, "Tina Wright", "tina.w@company.com", "Human Resources", "HR Director", 105000, "2018-02-01", None, "active"),
        (21, "Uma Scott", "uma.s@company.com", "Human Resources", "HR Specialist", 68000, "2020-06-10", 20, "active"),
        
        # Finance
        (22, "Victor Green", "victor.g@company.com", "Finance", "Finance Director", 135000, "2018-03-15", None, "active"),
        (23, "Wendy Adams", "wendy.a@company.com", "Finance", "Financial Analyst", 82000, "2020-10-05", 22, "active"),
        (24, "Xavier Baker", "xavier.b@company.com", "Finance", "Accountant", 72000, "2021-04-12", 22, "active"),
    ]
    
    cursor.executemany("""
        INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees_data)
    
    print("✅ Created employees table (24 employees)")
    
    # ========================================================================
    # PRODUCTS TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            supplier TEXT,
            created_date TEXT NOT NULL,
            last_updated TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    """)
    
    products_data = [
        # Electronics
        (1, "Wireless Bluetooth Headphones", "Electronics", "Premium noise-cancelling headphones with 30-hour battery", 149.99, 65.00, 245, "ELEC-WBH-001", "AudioTech Ltd", "2023-01-15", "2024-11-20", "active"),
        (2, "USB-C Fast Charger", "Electronics", "65W fast charging adapter with multiple ports", 39.99, 15.00, 580, "ELEC-UFC-002", "PowerCo", "2023-02-10", "2024-12-01", "active"),
        (3, "Wireless Mouse", "Electronics", "Ergonomic wireless mouse with precision tracking", 29.99, 12.00, 432, "ELEC-WMS-003", "TechGear Inc", "2023-03-05", "2024-11-15", "active"),
        (4, "4K Webcam", "Electronics", "Professional 4K webcam with auto-focus", 89.99, 38.00, 156, "ELEC-4KW-004", "VisionTech", "2023-04-20", "2024-10-30", "active"),
        (5, "Portable SSD 1TB", "Electronics", "Ultra-fast portable solid state drive", 119.99, 52.00, 298, "ELEC-SSD-005", "StoragePro", "2023-05-12", "2024-11-25", "active"),
        
        # Office Supplies
        (6, "Standing Desk Converter", "Office Supplies", "Adjustable height desk converter for ergonomic working", 199.99, 85.00, 87, "OFFC-SDC-006", "ErgoWorks", "2023-01-20", "2024-09-15", "active"),
        (7, "Ergonomic Office Chair", "Office Supplies", "Lumbar support office chair with adjustable armrests", 349.99, 145.00, 64, "OFFC-EOC-007", "ComfortSeating", "2023-02-15", "2024-10-20", "active"),
        (8, "Desk Organizer Set", "Office Supplies", "5-piece bamboo desk organizer set", 34.99, 14.00, 215, "OFFC-DOS-008", "OrganizeIt", "2023-03-10", "2024-11-30", "active"),
        (9, "LED Desk Lamp", "Office Supplies", "Dimmable LED desk lamp with USB charging port", 45.99, 19.00, 178, "OFFC-LDL-009", "BrightLite", "2023-04-05", "2024-12-02", "active"),
        (10, "Wireless Keyboard", "Office Supplies", "Mechanical wireless keyboard with backlight", 79.99, 34.00, 203, "OFFC-WKB-010", "KeyMaster", "2023-05-18", "2024-11-18", "active"),
        
        # Home & Living
        (11, "Smart LED Light Bulbs (4-pack)", "Home & Living", "WiFi-enabled color-changing LED bulbs", 49.99, 21.00, 342, "HOME-SLB-011", "SmartHome Co", "2023-06-01", "2024-11-22", "active"),
        (12, "Air Purifier", "Home & Living", "HEPA filter air purifier for large rooms", 159.99, 68.00, 125, "HOME-APR-012", "CleanAir Inc", "2023-06-15", "2024-10-25", "active"),
        (13, "Robot Vacuum", "Home & Living", "Smart robot vacuum with app control", 299.99, 125.00, 93, "HOME-RBV-013", "AutoClean", "2023-07-10", "2024-11-10", "active"),
        (14, "Electric Kettle", "Home & Living", "1.7L stainless steel electric kettle", 39.99, 16.00, 267, "HOME-EKT-014", "KitchenPro", "2023-08-05", "2024-12-03", "active"),
        (15, "Memory Foam Pillow", "Home & Living", "Contoured memory foam pillow for neck support", 44.99, 18.00, 198, "HOME-MFP-015", "SleepWell", "2023-09-12", "2024-11-28", "active"),
        
        # Sports & Fitness
        (16, "Yoga Mat Premium", "Sports & Fitness", "Non-slip eco-friendly yoga mat with carrying strap", 34.99, 14.00, 312, "SPRT-YMP-016", "FitGear", "2023-07-20", "2024-11-15", "active"),
        (17, "Resistance Bands Set", "Sports & Fitness", "5-piece resistance band set with handles", 24.99, 10.00, 445, "SPRT-RBS-017", "FitGear", "2023-08-15", "2024-12-01", "active"),
        (18, "Water Bottle 32oz", "Sports & Fitness", "Insulated stainless steel water bottle", 27.99, 11.00, 523, "SPRT-WBT-018", "HydratePro", "2023-09-01", "2024-11-20", "active"),
        (19, "Fitness Tracker Watch", "Sports & Fitness", "Heart rate and activity tracking smartwatch", 89.99, 38.00, 187, "SPRT-FTW-019", "HealthTech", "2023-10-10", "2024-10-30", "active"),
        (20, "Dumbbells Set 20lb", "Sports & Fitness", "Adjustable dumbbell set with storage rack", 149.99, 62.00, 76, "SPRT-DBS-020", "IronFit", "2023-11-05", "2024-09-25", "active"),
    ]
    
    cursor.executemany("""
        INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products_data)
    
    print("✅ Created products table (20 products)")
    
    # ========================================================================
    # CUSTOMERS TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT DEFAULT 'USA',
            registration_date TEXT NOT NULL,
            last_purchase_date TEXT,
            total_spent REAL DEFAULT 0,
            loyalty_points INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active'
        )
    """)
    
    customers_data = [
        (1, "Emma", "Williams", "emma.williams@email.com", "555-0101", "123 Maple Street", "Los Angeles", "CA", "90001", "USA", "2023-01-15", "2024-11-28", 1247.50, 1248, "active"),
        (2, "Liam", "Johnson", "liam.j@email.com", "555-0102", "456 Oak Avenue", "New York", "NY", "10001", "USA", "2023-02-20", "2024-12-01", 892.30, 892, "active"),
        (3, "Olivia", "Brown", "olivia.brown@email.com", "555-0103", "789 Pine Road", "Chicago", "IL", "60601", "USA", "2023-03-10", "2024-11-15", 2156.75, 2157, "active"),
        (4, "Noah", "Davis", "noah.davis@email.com", "555-0104", "321 Elm Street", "Houston", "TX", "77001", "USA", "2023-03-25", "2024-10-20", 645.20, 645, "active"),
        (5, "Ava", "Miller", "ava.miller@email.com", "555-0105", "654 Birch Lane", "Phoenix", "AZ", "85001", "USA", "2023-04-12", "2024-11-30", 1523.90, 1524, "active"),
        (6, "Ethan", "Wilson", "ethan.w@email.com", "555-0106", "987 Cedar Drive", "Philadelphia", "PA", "19101", "USA", "2023-05-08", "2024-12-02", 478.65, 479, "active"),
        (7, "Sophia", "Moore", "sophia.moore@email.com", "555-0107", "147 Spruce Court", "San Antonio", "TX", "78201", "USA", "2023-06-15", "2024-11-10", 1834.40, 1834, "active"),
        (8, "Mason", "Taylor", "mason.taylor@email.com", "555-0108", "258 Willow Way", "San Diego", "CA", "92101", "USA", "2023-07-20", "2024-11-25", 956.80, 957, "active"),
        (9, "Isabella", "Anderson", "isabella.a@email.com", "555-0109", "369 Ash Boulevard", "Dallas", "TX", "75201", "USA", "2023-08-05", "2024-10-15", 1289.55, 1290, "active"),
        (10, "Lucas", "Thomas", "lucas.thomas@email.com", "555-0110", "741 Redwood Place", "San Jose", "CA", "95101", "USA", "2023-09-12", "2024-11-18", 723.45, 723, "active"),
        (11, "Mia", "Jackson", "mia.jackson@email.com", "555-0111", "852 Poplar Street", "Austin", "TX", "78701", "USA", "2023-10-01", "2024-12-03", 2045.90, 2046, "active"),
        (12, "Aiden", "White", "aiden.white@email.com", "555-0112", "963 Magnolia Avenue", "Jacksonville", "FL", "32099", "USA", "2023-10-18", "2024-11-05", 534.25, 534, "active"),
        (13, "Charlotte", "Harris", "charlotte.h@email.com", "555-0113", "159 Hickory Road", "Fort Worth", "TX", "76101", "USA", "2023-11-10", "2024-11-22", 876.30, 876, "active"),
        (14, "Logan", "Martin", "logan.martin@email.com", "555-0114", "357 Walnut Lane", "Columbus", "OH", "43004", "USA", "2023-11-25", "2024-10-28", 1456.70, 1457, "active"),
        (15, "Amelia", "Thompson", "amelia.t@email.com", "555-0115", "486 Cherry Drive", "San Francisco", "CA", "94102", "USA", "2023-12-08", "2024-11-12", 2378.50, 2379, "active"),
        (16, "James", "Garcia", "james.garcia@email.com", "555-0116", "512 Sycamore Court", "Indianapolis", "IN", "46201", "USA", "2024-01-15", "2024-11-29", 645.80, 646, "active"),
        (17, "Harper", "Martinez", "harper.m@email.com", "555-0117", "628 Cottonwood Way", "Charlotte", "NC", "28201", "USA", "2024-02-03", "2024-12-01", 1129.40, 1129, "active"),
        (18, "Benjamin", "Robinson", "ben.robinson@email.com", "555-0118", "734 Beech Place", "Seattle", "WA", "98101", "USA", "2024-02-20", "2024-11-08", 892.15, 892, "active"),
        (19, "Evelyn", "Clark", "evelyn.clark@email.com", "555-0119", "845 Fir Boulevard", "Denver", "CO", "80201", "USA", "2024-03-15", "2024-11-20", 1567.25, 1567, "active"),
        (20, "Alexander", "Rodriguez", "alex.r@email.com", "555-0120", "956 Palm Street", "Boston", "MA", "02101", "USA", "2024-04-01", "2024-10-25", 734.90, 735, "active"),
        (21, "Ella", "Lewis", "ella.lewis@email.com", "555-0121", "147 Cypress Avenue", "Nashville", "TN", "37201", "USA", "2024-05-10", "2024-11-15", 1823.60, 1824, "active"),
        (22, "William", "Lee", "william.lee@email.com", "555-0122", "258 Juniper Road", "Detroit", "MI", "48201", "USA", "2024-06-05", "2024-11-28", 456.70, 457, "active"),
        (23, "Abigail", "Walker", "abigail.w@email.com", "555-0123", "369 Laurel Lane", "Portland", "OR", "97201", "USA", "2024-07-12", "2024-12-02", 1245.80, 1246, "active"),
        (24, "Michael", "Hall", "michael.hall@email.com", "555-0124", "471 Dogwood Drive", "Las Vegas", "NV", "89101", "USA", "2024-08-20", "2024-11-10", 678.45, 678, "active"),
        (25, "Emily", "Allen", "emily.allen@email.com", "555-0125", "582 Maple Court", "Miami", "FL", "33101", "USA", "2024-09-15", "2024-11-25", 1934.20, 1934, "active"),
    ]
    
    cursor.executemany("""
        INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers_data)
    
    print("✅ Created customers table (25 customers)")
    
    # ========================================================================
    # ORDERS TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            tax_amount REAL NOT NULL,
            shipping_cost REAL NOT NULL,
            discount_amount REAL DEFAULT 0,
            status TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            shipping_address TEXT,
            tracking_number TEXT,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Generate realistic orders
    orders_data = []
    order_id = 1
    
    # Create multiple orders for various customers
    order_scenarios = [
        (1, "2024-11-28", 247.50, "completed", "Credit Card"),
        (1, "2024-10-15", 459.98, "completed", "PayPal"),
        (1, "2024-08-22", 540.02, "completed", "Credit Card"),
        (2, "2024-12-01", 149.99, "processing", "Credit Card"),
        (2, "2024-09-10", 742.31, "completed", "Debit Card"),
        (3, "2024-11-15", 1089.99, "completed", "Credit Card"),
        (3, "2024-08-05", 566.76, "completed", "PayPal"),
        (3, "2024-05-20", 500.00, "completed", "Credit Card"),
        (4, "2024-10-20", 645.20, "completed", "Debit Card"),
        (5, "2024-11-30", 324.98, "processing", "Credit Card"),
        (5, "2024-09-18", 698.92, "completed", "PayPal"),
        (5, "2024-06-12", 500.00, "completed", "Credit Card"),
        (6, "2024-12-02", 178.65, "shipped", "Credit Card"),
        (6, "2024-08-15", 300.00, "completed", "Debit Card"),
        (7, "2024-11-10", 934.40, "completed", "Credit Card"),
        (7, "2024-07-22", 900.00, "completed", "PayPal"),
        (8, "2024-11-25", 456.80, "completed", "Credit Card"),
        (8, "2024-09-05", 500.00, "completed", "Debit Card"),
        (9, "2024-10-15", 1289.55, "completed", "PayPal"),
        (10, "2024-11-18", 723.45, "completed", "Credit Card"),
        (11, "2024-12-03", 845.90, "processing", "Credit Card"),
        (11, "2024-09-28", 700.00, "completed", "PayPal"),
        (11, "2024-06-15", 500.00, "completed", "Credit Card"),
        (12, "2024-11-05", 534.25, "completed", "Debit Card"),
        (13, "2024-11-22", 876.30, "completed", "Credit Card"),
        (14, "2024-10-28", 1456.70, "completed", "PayPal"),
        (15, "2024-11-12", 1378.50, "completed", "Credit Card"),
        (15, "2024-08-20", 1000.00, "completed", "Credit Card"),
        (16, "2024-11-29", 645.80, "processing", "Debit Card"),
        (17, "2024-12-01", 629.40, "shipped", "Credit Card"),
        (17, "2024-09-12", 500.00, "completed", "PayPal"),
        (18, "2024-11-08", 892.15, "completed", "Credit Card"),
        (19, "2024-11-20", 1067.25, "completed", "PayPal"),
        (19, "2024-08-30", 500.00, "completed", "Credit Card"),
        (20, "2024-10-25", 734.90, "completed", "Debit Card"),
        (21, "2024-11-15", 923.60, "completed", "Credit Card"),
        (21, "2024-07-18", 900.00, "completed", "PayPal"),
        (22, "2024-11-28", 456.70, "completed", "Credit Card"),
        (23, "2024-12-02", 745.80, "processing", "PayPal"),
        (23, "2024-09-20", 500.00, "completed", "Credit Card"),
        (24, "2024-11-10", 678.45, "completed", "Debit Card"),
        (25, "2024-11-25", 934.20, "completed", "Credit Card"),
        (25, "2024-08-08", 1000.00, "completed", "PayPal"),
    ]
    
    for customer_id, order_date, subtotal, status, payment_method in order_scenarios:
        tax = round(subtotal * 0.08, 2)
        shipping = 15.00 if subtotal < 500 else 0.00
        discount = 0.00
        total = round(subtotal + tax + shipping - discount, 2)
        
        tracking = f"TRK{order_id:06d}" if status in ["shipped", "completed"] else None
        
        orders_data.append((
            order_id,
            customer_id,
            order_date,
            total,
            tax,
            shipping,
            discount,
            status,
            payment_method,
            f"Same as customer address",
            tracking,
            None
        ))
        order_id += 1
    
    cursor.executemany("""
        INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders_data)
    
    print(f"✅ Created orders table ({len(orders_data)} orders)")
    
    # ========================================================================
    # ORDER_ITEMS TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    
    # Generate order items
    order_items_data = []
    item_id = 1
    
    # Map orders to products
    order_product_map = [
        (1, [(1, 1), (10, 1)]),  # Order 1: Headphones, Keyboard
        (2, [(7, 1), (9, 1)]),   # Order 2: Chair, Lamp
        (3, [(6, 1), (8, 2), (3, 1)]),  # Order 3: Desk converter, organizers, mouse
        (4, [(1, 1)]),  # Order 4: Headphones
        (5, [(2, 3), (4, 1), (3, 2), (5, 1)]),  # Order 5: Multiple items
        (6, [(13, 1), (12, 1)]),  # Order 6: Robot vacuum, Air purifier
        (7, [(11, 2), (14, 3), (18, 2)]),  # Order 7: LED bulbs, kettles, water bottles
        (8, [(16, 2), (17, 2), (18, 1)]),  # Order 8: Yoga mats, resistance bands, water bottle
        (9, [(4, 1), (5, 3)]),  # Order 9: Webcam, SSDs
        (10, [(1, 1), (2, 2), (3, 1)]),  # Order 10: Headphones, chargers, mouse
        (11, [(19, 1), (17, 1), (18, 2)]),  # Order 11: Fitness tracker, resistance bands, water bottles
        (12, [(10, 1), (9, 1), (8, 2)]),  # Order 12: Keyboard, lamp, organizers
        (13, [(20, 1), (16, 1), (17, 1)]),  # Order 13: Dumbbells, yoga mat, resistance bands
        (14, [(7, 1), (6, 1), (10, 1)]),  # Order 14: Chair, desk converter, keyboard
        (15, [(13, 1), (12, 1), (11, 3)]),  # Order 15: Robot vacuum, air purifier, LED bulbs
        (16, [(1, 2), (3, 1), (2, 1)]),  # Order 16: Headphones, mouse, charger
        (17, [(5, 2), (4, 1)]),  # Order 17: SSDs, webcam
        (18, [(15, 5), (14, 2)]),  # Order 18: Pillows, kettles
        (19, [(7, 1), (9, 2), (8, 1)]),  # Order 19: Chair, lamps, organizer
        (20, [(19, 1), (18, 3), (16, 2)]),  # Order 20: Fitness items
        (21, [(13, 1), (11, 4)]),  # Order 21: Robot vacuum, LED bulbs
        (22, [(1, 1), (10, 1), (3, 1)]),  # Order 22: Tech bundle
        (23, [(6, 1), (8, 2), (9, 1)]),  # Order 23: Desk setup
        (24, [(2, 5), (3, 2)]),  # Order 24: Chargers, mice
        (25, [(20, 1), (19, 1), (17, 2), (16, 1)]),  # Order 25: Fitness bundle
        (26, [(12, 1), (11, 6)]),  # Order 26: Air purifier, LED bulbs
        (27, [(7, 1), (10, 1)]),  # Order 27: Chair, keyboard
        (28, [(5, 3), (4, 1)]),  # Order 28: SSDs, webcam
        (29, [(1, 2), (2, 1)]),  # Order 29: Headphones, charger
        (30, [(16, 3), (17, 3), (18, 3)]),  # Order 30: Yoga bundle
        (31, [(15, 4), (14, 1)]),  # Order 31: Pillows, kettle
        (32, [(10, 1), (9, 1), (8, 3)]),  # Order 32: Office setup
        (33, [(13, 1), (12, 1)]),  # Order 33: Robot vacuum, air purifier
        (34, [(19, 1), (20, 1)]),  # Order 34: Fitness watch, dumbbells
        (35, [(11, 4), (14, 2)]),  # Order 35: LED bulbs, kettles
        (36, [(7, 1), (6, 1)]),  # Order 36: Chair, desk converter
        (37, [(1, 1), (3, 2)]),  # Order 37: Headphones, mice
        (38, [(16, 1), (17, 2), (18, 2)]),  # Order 38: Yoga items
        (39, [(5, 2), (2, 3)]),  # Order 39: SSDs, chargers
        (40, [(20, 1), (18, 1)]),  # Order 40: Dumbbells, water bottle
        (41, [(13, 1), (11, 2)]),  # Order 41: Robot vacuum, LED bulbs
        (42, [(15, 6), (14, 3)]),  # Order 42: Pillows, kettles
    ]
    
    for order_id, items in order_product_map:
        for product_id, quantity in items:
            # Get product price
            cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
            unit_price = cursor.fetchone()[0]
            subtotal = round(unit_price * quantity, 2)
            
            order_items_data.append((
                item_id,
                order_id,
                product_id,
                quantity,
                unit_price,
                subtotal
            ))
            item_id += 1
    
    cursor.executemany("""
        INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)
    """, order_items_data)
    
    print(f"✅ Created order_items table ({len(order_items_data)} items)")
    
    # ========================================================================
    # CUSTOMER_NOTES TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE customer_notes (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            note_date TEXT NOT NULL,
            note_type TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'open',
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)
    
    customer_notes_data = [
        (1, 3, 15, "2024-11-15", "support", "Product inquiry", "Customer asked about compatibility of wireless headphones with their device. Confirmed compatibility and provided setup instructions.", "normal", "closed"),
        (2, 7, 14, "2024-11-20", "feedback", "Positive feedback", "Customer very satisfied with robot vacuum purchase. Mentioned in review they'd recommend to friends.", "low", "closed"),
        (3, 1, 16, "2024-11-25", "complaint", "Shipping delay", "Customer reported shipping delay on order #1. Investigated and found carrier issue. Expedited shipping at no charge.", "high", "closed"),
        (4, 15, 8, "2024-11-28", "sales", "Bulk order inquiry", "Customer interested in purchasing 10+ fitness trackers for company wellness program. Sent bulk pricing quote.", "high", "open"),
        (5, 5, 15, "2024-12-01", "support", "Return request", "Customer wants to return air purifier. Within return window. Sent return label via email.", "normal", "open"),
        (6, 11, 17, "2024-12-02", "support", "Technical issue", "Customer having trouble connecting smart LED bulbs to WiFi. Walked through setup process. Issue resolved.", "normal", "closed"),
        (7, 3, 14, "2024-11-10", "feedback", "Product suggestion", "Customer suggested we carry more eco-friendly products. Forwarded feedback to product management team.", "low", "closed"),
        (8, 19, 16, "2024-11-18", "support", "Warranty claim", "Customer's webcam stopped working after 8 months. Covered under warranty. Sent replacement.", "high", "closed"),
        (9, 9, 15, "2024-10-20", "support", "Setup assistance", "Customer needed help setting up standing desk converter. Provided video tutorial link and assembly tips.", "normal", "closed"),
        (10, 21, 8, "2024-11-22", "sales", "Upgrade inquiry", "Customer asking about upgrading from current fitness tracker to premium model. Explained differences and offered upgrade discount.", "normal", "open"),
        (11, 12, 17, "2024-11-05", "complaint", "Defective product", "Customer received damaged desk organizer. Apologized and sent replacement with expedited shipping.", "high", "closed"),
        (12, 25, 14, "2024-11-28", "feedback", "Website improvement", "Customer suggested adding comparison feature for similar products. Great idea - forwarded to tech team.", "low", "closed"),
        (13, 6, 16, "2024-12-02", "support", "Payment issue", "Customer's payment declined. They updated card info and transaction completed successfully.", "normal", "closed"),
        (14, 14, 15, "2024-10-30", "support", "Product compatibility", "Asked if wireless mouse works with iPad. Confirmed compatibility and provided connection instructions.", "normal", "closed"),
        (15, 8, 17, "2024-11-26", "support", "Tracking inquiry", "Customer couldn't find tracking info. Located order and sent tracking link. Package arriving tomorrow.", "normal", "closed"),
        (16, 20, 8, "2024-11-01", "sales", "Loyalty program", "Customer asked about loyalty points redemption. Explained program benefits and current point balance.", "low", "closed"),
        (17, 16, 14, "2024-11-29", "support", "Order modification", "Customer wanted to add items to existing order. Order already shipped, suggested placing new order with discount code.", "normal", "closed"),
        (18, 4, 16, "2024-10-25", "feedback", "Delivery praise", "Customer impressed with fast delivery time. Shared positive experience on social media.", "low", "closed"),
        (19, 23, 15, "2024-12-03", "support", "Gift wrapping", "Customer asked if gift wrapping available for order. Confirmed service available for $5 per item.", "low", "open"),
        (20, 17, 17, "2024-12-01", "support", "Product recommendation", "Customer looking for ergonomic office setup recommendations. Suggested chair, desk converter, and keyboard bundle.", "normal", "open"),
    ]
    
    cursor.executemany("""
        INSERT INTO customer_notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customer_notes_data)
    
    print(f"✅ Created customer_notes table ({len(customer_notes_data)} notes)")
    
    # ========================================================================
    # CHAT_HISTORY TABLE
    # ========================================================================
    cursor.execute("""
        CREATE TABLE chat_history (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            employee_id INTEGER,
            session_id TEXT NOT NULL,
            message_date TEXT NOT NULL,
            sender_type TEXT NOT NULL,
            message TEXT NOT NULL,
            sentiment TEXT,
            resolved BOOLEAN DEFAULT 0,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)
    
    chat_history_data = [
        # Session 1: Product inquiry
        (1, 3, 15, "CHAT-001", "2024-11-15 14:23:15", "customer", "Hi, I'm interested in the wireless headphones. Are they compatible with Android?", "neutral", 0),
        (2, 3, 15, "CHAT-001", "2024-11-15 14:23:45", "agent", "Hello! Yes, our wireless Bluetooth headphones are fully compatible with Android devices. They work with any device that supports Bluetooth 5.0.", "positive", 0),
        (3, 3, 15, "CHAT-001", "2024-11-15 14:24:30", "customer", "Great! How long does the battery last?", "positive", 0),
        (4, 3, 15, "CHAT-001", "2024-11-15 14:25:00", "agent", "The battery lasts up to 30 hours on a single charge with active noise cancellation on, and up to 40 hours with it off.", "positive", 0),
        (5, 3, 15, "CHAT-001", "2024-11-15 14:25:45", "customer", "Perfect! I'll order them. Thanks for your help!", "positive", 1),
        
        # Session 2: Shipping inquiry
        (6, 7, 14, "CHAT-002", "2024-11-20 10:15:22", "customer", "I ordered a robot vacuum 3 days ago but haven't received tracking info yet.", "negative", 0),
        (7, 7, 14, "CHAT-002", "2024-11-20 10:16:10", "agent", "Let me check that for you. Can you provide your order number?", "neutral", 0),
        (8, 7, 14, "CHAT-002", "2024-11-20 10:16:45", "customer", "Order #6", "neutral", 0),
        (9, 7, 14, "CHAT-002", "2024-11-20 10:17:30", "agent", "Thank you! I see your order shipped this morning. Your tracking number is TRK000006. It should arrive in 2-3 business days.", "positive", 0),
        (10, 7, 14, "CHAT-002", "2024-11-20 10:18:00", "customer", "Oh great! I didn't get the email. Thanks for checking!", "positive", 1),
        
        # Session 3: Return request
        (11, 5, 15, "CHAT-003", "2024-12-01 16:30:00", "customer", "I need to return the air purifier I bought. It's too loud for my apartment.", "negative", 0),
        (12, 5, 15, "CHAT-003", "2024-12-01 16:30:45", "agent", "I'm sorry to hear it's not working out. You're within our 30-day return window. I can send you a prepaid return label.", "positive", 0),
        (13, 5, 15, "CHAT-003", "2024-12-01 16:31:20", "customer", "That would be great. Will I get a full refund?", "neutral", 0),
        (14, 5, 15, "CHAT-003", "2024-12-01 16:32:00", "agent", "Yes, you'll receive a full refund within 5-7 business days after we receive the item. I'm emailing the label now.", "positive", 0),
        (15, 5, 15, "CHAT-003", "2024-12-01 16:32:30", "customer", "Thank you so much for making this easy!", "positive", 1),
        
        # Session 4: Technical support
        (16, 11, 17, "CHAT-004", "2024-12-02 09:45:00", "customer", "Help! I can't get my smart LED bulbs to connect to WiFi.", "negative", 0),
        (17, 11, 17, "CHAT-004", "2024-12-02 09:45:30", "agent", "I can help with that. First, make sure the bulbs are powered on and flashing. Are they flashing?", "neutral", 0),
        (18, 11, 17, "CHAT-004", "2024-12-02 09:46:00", "customer", "Yes, they're flashing blue", "neutral", 0),
        (19, 11, 17, "CHAT-004", "2024-12-02 09:46:45", "agent", "Perfect. Now open the app and make sure you're connected to your 2.4GHz WiFi network (not 5GHz). The bulbs only work with 2.4GHz.", "neutral", 0),
        (20, 11, 17, "CHAT-004", "2024-12-02 09:48:00", "customer", "Oh! I was on the 5GHz network. Let me switch... OK, it's working now!", "positive", 0),
        (21, 11, 17, "CHAT-004", "2024-12-02 09:48:30", "agent", "Excellent! Is there anything else I can help you with?", "positive", 0),
        (22, 11, 17, "CHAT-004", "2024-12-02 09:48:45", "customer", "Nope, that was it. Thanks!", "positive", 1),
        
        # Session 5: Bulk order inquiry
        (23, 15, 8, "CHAT-005", "2024-11-28 11:20:00", "customer", "Hi, I'm interested in buying 15 fitness trackers for my company. Do you offer bulk discounts?", "positive", 0),
        (24, 15, 8, "CHAT-005", "2024-11-28 11:21:00", "agent", "Great question! Yes, we do offer bulk pricing. For 15 units, I can offer you 15% off the regular price. Let me prepare a quote for you.", "positive", 0),
        (25, 15, 8, "CHAT-005", "2024-11-28 11:22:30", "customer", "That sounds good. We'd also need company logos engraved. Is that possible?", "positive", 0),
        (26, 15, 8, "CHAT-005", "2024-11-28 11:23:15", "agent", "We can arrange custom engraving through our corporate sales team. I'll connect you with them. They'll reach out within 24 hours.", "positive", 0),
        (27, 15, 8, "CHAT-005", "2024-11-28 11:23:45", "customer", "Perfect! Looking forward to it.", "positive", 1),
        
        # Session 6: Product comparison
        (28, 19, 16, "CHAT-006", "2024-11-18 15:00:00", "customer", "What's the difference between your regular yoga mat and the premium one?", "neutral", 0),
        (29, 19, 16, "CHAT-006", "2024-11-18 15:01:00", "agent", "The premium mat is thicker (6mm vs 4mm), made from eco-friendly materials, and has better grip. It also comes with a carrying strap.", "neutral", 0),
        (30, 19, 16, "CHAT-006", "2024-11-18 15:02:00", "customer", "Is the extra $10 worth it for a beginner?", "neutral", 0),
        (31, 19, 16, "CHAT-006", "2024-11-18 15:02:45", "agent", "For beginners, the extra cushioning in the premium mat is actually really helpful. It's easier on your joints while you're building strength.", "positive", 0),
        (32, 19, 16, "CHAT-006", "2024-11-18 15:03:15", "customer", "Makes sense. I'll go with the premium. Thanks!", "positive", 1),
        
        # Session 7: Warranty claim
        (33, 19, 16, "CHAT-007", "2024-11-18 14:00:00", "customer", "My webcam stopped working. It's only been 8 months.", "negative", 0),
        (34, 19, 16, "CHAT-007", "2024-11-18 14:01:00", "agent", "I'm sorry to hear that. Our webcams have a 1-year warranty, so you're covered. Can you describe what's happening?", "neutral", 0),
        (35, 19, 16, "CHAT-007", "2024-11-18 14:02:00", "customer", "It's not being recognized by my computer anymore. Tried different USB ports.", "negative", 0),
        (36, 19, 16, "CHAT-007", "2024-11-18 14:03:00", "agent", "That sounds like a hardware issue. I'll process a warranty replacement for you right away. You should receive it in 3-5 business days.", "positive", 0),
        (37, 19, 16, "CHAT-007", "2024-11-18 14:03:30", "customer", "Do I need to send the broken one back?", "neutral", 0),
        (38, 19, 16, "CHAT-007", "2024-11-18 14:04:00", "agent", "Yes, I'll include a prepaid return label with your replacement. Just send it back within 14 days.", "neutral", 0),
        (39, 19, 16, "CHAT-007", "2024-11-18 14:04:30", "customer", "Got it. Thanks for the quick help!", "positive", 1),
        
        # Session 8: Gift recommendation
        (40, 23, 15, "CHAT-008", "2024-12-03 13:30:00", "customer", "I need gift ideas for my boss who works from home. Budget around $200.", "positive", 0),
        (41, 23, 15, "CHAT-008", "2024-12-03 13:31:00", "agent", "Great! For work-from-home gifts, I'd recommend our ergonomic office chair or standing desk converter. Both are very popular.", "positive", 0),
        (42, 23, 15, "CHAT-008", "2024-12-03 13:32:00", "customer", "The standing desk converter sounds perfect! Can it be gift wrapped?", "positive", 0),
        (43, 23, 15, "CHAT-008", "2024-12-03 13:32:45", "agent", "Yes! We offer gift wrapping for $5. Would you like to include a gift message as well?", "positive", 0),
        (44, 23, 15, "CHAT-008", "2024-12-03 13:33:15", "customer", "Yes please! This is perfect.", "positive", 1),
        
        # Session 9: Loyalty points
        (45, 20, 8, "CHAT-009", "2024-11-01 10:00:00", "customer", "How do I use my loyalty points?", "neutral", 0),
        (46, 20, 8, "CHAT-009", "2024-11-01 10:01:00", "agent", "You can redeem your points at checkout! Every 100 points equals $1 off your purchase. You currently have 735 points.", "positive", 0),
        (47, 20, 8, "CHAT-009", "2024-11-01 10:02:00", "customer", "So I have $7.35 to use? That's great!", "positive", 0),
        (48, 20, 8, "CHAT-009", "2024-11-01 10:02:30", "agent", "Exactly! You'll see the option to apply them during checkout. The points don't expire either.", "positive", 0),
        (49, 20, 8, "CHAT-009", "2024-11-01 10:03:00", "customer", "Awesome, thanks for explaining!", "positive", 1),
        
        # Session 10: Shipping options
        (50, 17, 14, "CHAT-010", "2024-12-01 16:00:00", "customer", "What shipping options do you have? I need something by Friday.", "neutral", 0),
        (51, 17, 14, "CHAT-010", "2024-12-01 16:01:00", "agent", "We have standard (5-7 days), expedited (2-3 days), and overnight shipping. For Friday delivery, you'd need expedited.", "neutral", 0),
        (52, 17, 14, "CHAT-010", "2024-12-01 16:02:00", "customer", "How much is expedited?", "neutral", 0),
        (53, 17, 14, "CHAT-010", "2024-12-01 16:02:30", "agent", "Expedited shipping is $25. Orders over $500 get free expedited shipping though!", "positive", 0),
        (54, 17, 14, "CHAT-010", "2024-12-01 16:03:00", "customer", "My order is $629, so it's free? Perfect!", "positive", 1),
    ]
    
    cursor.executemany("""
        INSERT INTO chat_history VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, chat_history_data)
    
    print(f"✅ Created chat_history table ({len(chat_history_data)} messages)")
    
    # ========================================================================
    # COMMIT AND CLOSE
    # ========================================================================
    conn.commit()
    conn.close()
    
    print("\n" + "="*70)
    print(" DATABASE CREATION COMPLETE!")
    print("="*70)
    print(f"\n Summary:")
    print(f"   • Departments: {len(departments_data)} records")
    print(f"   • Employees: {len(employees_data)} records")
    print(f"   • Products: {len(products_data)} records")
    print(f"   • Customers: {len(customers_data)} records")
    print(f"   • Orders: {len(orders_data)} records")
    print(f"   • Order Items: {len(order_items_data)} records")
    print(f"   • Customer Notes: {len(customer_notes_data)} records")
    print(f"   • Chat History: {len(chat_history_data)} messages")
    print(f"\n   Total Records: {len(departments_data) + len(employees_data) + len(products_data) + len(customers_data) + len(orders_data) + len(order_items_data) + len(customer_notes_data) + len(chat_history_data)}")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    create_comprehensive_database()
