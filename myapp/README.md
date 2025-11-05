# Django DRF Multi-Database Concurrent Insertion System

A Django REST Framework application that simulates a distributed system with multiple SQLite databases and demonstrates concurrent data insertion using Python threads.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Expected Output](#expected-output)
- [Technical Details](#technical-details)
- [Validation Rules](#validation-rules)
- [Database Architecture](#database-architecture)

## 🎯 Overview

This project demonstrates:
- **Multi-database architecture** with separate SQLite databases for different models
- **Concurrent insertions** using Python threading (30 simultaneous threads)
- **Application-level validation** without database constraints
- **Thread-safe operations** using locks for result aggregation

## ✨ Features

- ✅ Three separate SQLite databases (users.db, products.db, orders.db)
- ✅ Custom database router for model-specific database routing
- ✅ Concurrent insertions using threading (10 threads per model)
- ✅ Comprehensive application-level validation
- ✅ Thread-safe result collection and reporting
- ✅ Detailed success/failure reporting for each insertion
- ✅ Execution time tracking

## 📁 Project Structure

```
distributed_db_system/
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
│
├── distributed_db_system/             # Main project directory
│   ├── __init__.py
│   ├── settings.py                    # Django settings with multi-DB config
│   ├── urls.py                        # URL configuration
│   └── wsgi.py                        # WSGI configuration
│
└── myapp/                             # Main application
    ├── __init__.py
    ├── models.py                      # User, Product, Order models
    ├── validators.py                  # Application-level validators
    ├── routers.py                     # Database router
    ├── apps.py                        # App configuration
    ├── admin.py                       # Admin configuration
    ├── tests.py                       # Test cases
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── insert_data.py         # Custom management command
```

## 📦 Requirements

- Python 3.8+
- Django 4.2.7
- Django REST Framework 3.14.0

## 🚀 Installation

### Step 1: Clone or Create Project Directory

```bash
mkdir distributed_db_system
cd distributed_db_system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Project Structure

```bash
# Create Django project
django-admin startproject distributed_db_system .

# Create Django app
python manage.py startapp myapp

# Create management commands directory
mkdir -p myapp/management/commands
touch myapp/management/__init__.py
touch myapp/management/commands/__init__.py
```

### Step 5: Add All Project Files

Copy all the files from the artifact into their respective locations as shown in the project structure.

### Step 6: Run Migrations

```bash
# Migrate users database
python manage.py migrate --database=users_db

# Migrate products database
python manage.py migrate --database=products_db

# Migrate orders database
python manage.py migrate --database=orders_db

# Migrate default database
python manage.py migrate
```

## 💻 Usage

### Run the Concurrent Insertion Command

```bash
python manage.py insert_data
```

This single command will:
1. Create 30 threads (10 for each model)
2. Simultaneously insert test data into three separate databases
3. Validate each record at the application level
4. Display detailed results for each insertion
5. Show summary statistics and execution time

### Test Data

The command uses predefined test data that includes both valid and invalid records to demonstrate validation:

**Users (users.db):**
- 9 valid users
- 1 invalid user (Row 10: missing name)

**Products (products.db):**
- 9 valid products
- 1 invalid product (Row 10: negative price)

**Orders (orders.db):**
- 7 valid orders
- 3 invalid orders (Row 8: zero quantity, Row 9: negative quantity, Row 10: non-existent product)

## 📊 Expected Output

```
====================================================================================================
CONCURRENT DATABASE INSERTION RESULTS
Simulating Distributed System with Multiple SQLite Databases
====================================================================================================

📊 USERS TABLE (users.db):
----------------------------------------------------------------------------------------------------
✓ Row 1: User 'Alice' (alice@example.com) inserted successfully
✓ Row 2: User 'Bob' (bob@example.com) inserted successfully
✓ Row 3: User 'Charlie' (charlie@example.com) inserted successfully
✓ Row 4: User 'David' (david@example.com) inserted successfully
✓ Row 5: User 'Eve' (eve@example.com) inserted successfully
✓ Row 6: User 'Frank' (frank@example.com) inserted successfully
✓ Row 7: User 'Grace' (grace@example.com) inserted successfully
✓ Row 8: User 'Alice' (alice@example.com) inserted successfully
✓ Row 9: User 'Henry' (henry@example.com) inserted successfully
✗ Row 10: Row 10: Name is required and cannot be empty

📊 PRODUCTS TABLE (products.db):
----------------------------------------------------------------------------------------------------
✓ Row 1: Product 'Laptop' ($1000.0) inserted successfully
✓ Row 2: Product 'Smartphone' ($700.0) inserted successfully
✓ Row 3: Product 'Headphones' ($150.0) inserted successfully
✓ Row 4: Product 'Monitor' ($300.0) inserted successfully
✓ Row 5: Product 'Keyboard' ($50.0) inserted successfully
✓ Row 6: Product 'Mouse' ($30.0) inserted successfully
✓ Row 7: Product 'Laptop' ($1000.0) inserted successfully
✓ Row 8: Product 'Smartwatch' ($250.0) inserted successfully
✓ Row 9: Product 'Gaming Chair' ($500.0) inserted successfully
✗ Row 10: Row 10: Price cannot be negative

📊 ORDERS TABLE (orders.db):
----------------------------------------------------------------------------------------------------
✓ Row 1: Order (User: 1, Product: 1, Qty: 2) inserted successfully
✓ Row 2: Order (User: 2, Product: 2, Qty: 1) inserted successfully
✓ Row 3: Order (User: 3, Product: 3, Qty: 5) inserted successfully
✓ Row 4: Order (User: 4, Product: 4, Qty: 1) inserted successfully
✓ Row 5: Order (User: 5, Product: 5, Qty: 3) inserted successfully
✓ Row 6: Order (User: 6, Product: 6, Qty: 4) inserted successfully
✓ Row 7: Order (User: 7, Product: 7, Qty: 2) inserted successfully
✗ Row 8: Row 8: Quantity must be greater than 0
✗ Row 9: Row 9: Quantity must be greater than 0
✗ Row 10: Row 10: Quantity must be greater than 0

====================================================================================================
📈 SUMMARY:
----------------------------------------------------------------------------------------------------
Users:    9 successful | 1 failed
Products: 9 successful | 1 failed
Orders:   7 successful | 3 failed
----------------------------------------------------------------------------------------------------
Total threads executed: 30 (10 per model)
Total execution time: 0.0523 seconds
====================================================================================================
```

## 🔧 Technical Details

### Database Configuration

The project uses Django's multi-database support with a custom router:

```python
DATABASES = {
    'default': {...},
    'users_db': {...},    # For User model
    'orders_db': {...},   # For Order model
    'products_db': {...}, # For Product model
}
```

### Threading Implementation

- **30 concurrent threads**: 10 threads per model
- **Thread-safe result collection**: Using `threading.Lock()`
- **Simultaneous execution**: All threads start together
- **Blocking wait**: Main thread waits for all threads to complete

### Database Router

The `MultiDBRouter` class routes each model to its specific database:
- `User` → `users_db`
- `Product` → `products_db`
- `Order` → `orders_db`

## ✅ Validation Rules

### User Validation
- **Name**: Required, cannot be empty or whitespace
- **Email**: Required, must match valid email format (regex validation)

### Product Validation
- **Name**: Required, cannot be empty or whitespace
- **Price**: Required, must be positive (greater than 0), cannot be negative

### Order Validation
- **User ID**: Required, must be a positive integer
- **Product ID**: Required, must be a positive integer
- **Quantity**: Required, must be greater than 0

All validations are performed at the **application level** without database constraints.

## 🗄️ Database Architecture

```
Distributed Database System
│
├── users.db
│   └── users table (id, name, email)
│
├── products.db
│   └── products table (id, name, price)
│
└── orders.db
    └── orders table (id, user_id, product_id, quantity)
```

Each database is:
- **Isolated**: Separate SQLite file
- **Independent**: Can be on different servers in production
- **Concurrent**: Supports simultaneous write operations
- **Thread-safe**: SQLite handles concurrent access

## 🧪 Testing

To verify the insertions:

```bash
# Check users database
python manage.py dbshell --database=users_db
> SELECT * FROM users;

# Check products database
python manage.py dbshell --database=products_db
> SELECT * FROM products;

# Check orders database
python manage.py dbshell --database=orders_db
> SELECT * FROM orders;
```

## 📝 Notes

1. **No Authentication Required**: As per assignment requirements, no authentication or authorization is implemented.

2. **Application-Level Validation**: All validations are handled in Python code, not at the database level.

3. **Thread Safety**: The implementation uses locks to ensure thread-safe result aggregation.

4. **Production Considerations**: In production, consider:
   - Using PostgreSQL/MySQL instead of SQLite for better concurrency
   - Implementing connection pooling
   - Adding retry logic for failed insertions
   - Using task queues (Celery) for large-scale insertions

## 🐛 Troubleshooting

### Issue: "No module named 'myapp'"
**Solution**: Ensure `myapp` is in `INSTALLED_APPS` in `settings.py`

### Issue: "Table doesn't exist"
**Solution**: Run migrations for each database:
```bash
python manage.py migrate --database=users_db
python manage.py migrate --database=products_db
python manage.py migrate --database=orders_db
```

### Issue: "Command not found"
**Solution**: Ensure the management command file structure is correct and all `__init__.py` files exist.

## 📄 License

This project is created for educational purposes as part of a Django DRF assignment.

## 👥 Author

Created as a demonstration of Django multi-database architecture and concurrent programming with threads.

---

**Assignment Completed**: ✅
- Multi-database setup with SQLite
- Concurrent insertions using threads
- Application-level validation
- Single command execution
- Detailed result reporting