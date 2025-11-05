from django.core.management.base import BaseCommand
from myapp.models import User, Product, Order
from myapp.validators import validate_user, validate_product, validate_order, ValidationError
import threading
import time

class Command(BaseCommand):
    help = 'Insert test data concurrently into multiple databases'
    
    def __init__(self):
        super().__init__()
        self.results = {
            'users': [],
            'products': [],
            'orders': []
        }
        self.lock = threading.Lock()
    
    def handle(self, *args, **options):
        users_data = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
            {'id': 4, 'name': 'David', 'email': 'david@example.com'},
            {'id': 5, 'name': 'Eve', 'email': 'eve@example.com'},
            {'id': 6, 'name': 'Frank', 'email': 'frank@example.com'},
            {'id': 7, 'name': 'Grace', 'email': 'grace@example.com'},
            {'id': 8, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 9, 'name': 'Henry', 'email': 'henry@example.com'},
            {'id': 10, 'name': '', 'email': 'jane@example.com'},
        ]
        
        products_data = [
            {'id': 1, 'name': 'Laptop', 'price': 1000.00},
            {'id': 2, 'name': 'Smartphone', 'price': 700.00},
            {'id': 3, 'name': 'Headphones', 'price': 150.00},
            {'id': 4, 'name': 'Monitor', 'price': 300.00},
            {'id': 5, 'name': 'Keyboard', 'price': 50.00},
            {'id': 6, 'name': 'Mouse', 'price': 30.00},
            {'id': 7, 'name': 'Laptop', 'price': 1000.00},
            {'id': 8, 'name': 'Smartwatch', 'price': 250.00},
            {'id': 9, 'name': 'Gaming Chair', 'price': 500.00},
            {'id': 10, 'name': 'Earbuds', 'price': -50.00},
        ]
        
        orders_data = [
            {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2},
            {'id': 2, 'user_id': 2, 'product_id': 2, 'quantity': 1},
            {'id': 3, 'user_id': 3, 'product_id': 3, 'quantity': 5},
            {'id': 4, 'user_id': 4, 'product_id': 4, 'quantity': 1},
            {'id': 5, 'user_id': 5, 'product_id': 5, 'quantity': 3},
            {'id': 6, 'user_id': 6, 'product_id': 6, 'quantity': 4},
            {'id': 7, 'user_id': 7, 'product_id': 7, 'quantity': 2},
            {'id': 8, 'user_id': 8, 'product_id': 8, 'quantity': 0},
            {'id': 9, 'user_id': 9, 'product_id': 1, 'quantity': -1},
            {'id': 10, 'user_id': 10, 'product_id': 11, 'quantity': 2},
        ]
        
        threads = []
        
        # Create threads for users
        for user_data in users_data:
            t = threading.Thread(target=self.insert_user, args=(user_data,))
            threads.append(t)
        
        # Create threads for products
        for product_data in products_data:
            t = threading.Thread(target=self.insert_product, args=(product_data,))
            threads.append(t)
        
        # Create threads for orders
        for order_data in orders_data:
            t = threading.Thread(target=self.insert_order, args=(order_data,))
            threads.append(t)
        
        # Start all threads
        start_time = time.time()
        for t in threads:
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
        
        end_time = time.time()
        
        # Print results
        self.print_results(end_time - start_time)
    
    def insert_user(self, data):
        try:
            validate_user(data)
            user = User.objects.using('users_db').create(
                name=data['name'],
                email=data['email']
            )
            with self.lock:
                self.results['users'].append({
                    'id': data['id'],
                    'status': 'SUCCESS',
                    'message': f"User '{data['name']}' inserted successfully",
                    'db_id': user.id
                })
        except ValidationError as e:
            with self.lock:
                self.results['users'].append({
                    'id': data['id'],
                    'status': 'FAILED',
                    'message': str(e)
                })
        except Exception as e:
            with self.lock:
                self.results['users'].append({
                    'id': data['id'],
                    'status': 'ERROR',
                    'message': f"Unexpected error: {str(e)}"
                })
    
    def insert_product(self, data):
        try:
            validate_product(data)
            product = Product.objects.using('products_db').create(
                name=data['name'],
                price=data['price']
            )
            with self.lock:
                self.results['products'].append({
                    'id': data['id'],
                    'status': 'SUCCESS',
                    'message': f"Product '{data['name']}' inserted successfully",
                    'db_id': product.id
                })
        except ValidationError as e:
            with self.lock:
                self.results['products'].append({
                    'id': data['id'],
                    'status': 'FAILED',
                    'message': str(e)
                })
        except Exception as e:
            with self.lock:
                self.results['products'].append({
                    'id': data['id'],
                    'status': 'ERROR',
                    'message': f"Unexpected error: {str(e)}"
                })
    
    def insert_order(self, data):
        try:
            validate_order(data)
            order = Order.objects.using('orders_db').create(
                user_id=data['user_id'],
                product_id=data['product_id'],
                quantity=data['quantity']
            )
            with self.lock:
                self.results['orders'].append({
                    'id': data['id'],
                    'status': 'SUCCESS',
                    'message': f"Order for user_id={data['user_id']}, product_id={data['product_id']} inserted successfully",
                    'db_id': order.id
                })
        except ValidationError as e:
            with self.lock:
                self.results['orders'].append({
                    'id': data['id'],
                    'status': 'FAILED',
                    'message': str(e)
                })
        except Exception as e:
            with self.lock:
                self.results['orders'].append({
                    'id': data['id'],
                    'status': 'ERROR',
                    'message': f"Unexpected error: {str(e)}"
                })
    
    def print_results(self, execution_time):
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("CONCURRENT INSERTION RESULTS"))
        self.stdout.write("="*80 + "\n")
        
        # Sort results by ID
        self.results['users'].sort(key=lambda x: x['id'])
        self.results['products'].sort(key=lambda x: x['id'])
        self.results['orders'].sort(key=lambda x: x['id'])
        
        # Print Users Results
        self.stdout.write("\n" + self.style.HTTP_INFO("USERS TABLE (users.db):"))
        self.stdout.write("-" * 80)
        for result in self.results['users']:
            status_style = self.style.SUCCESS if result['status'] == 'SUCCESS' else self.style.ERROR
            self.stdout.write(f"Row {result['id']}: [{status_style(result['status'])}] {result['message']}")
        
        # Print Products Results
        self.stdout.write("\n" + self.style.HTTP_INFO("PRODUCTS TABLE (products.db):"))
        self.stdout.write("-" * 80)
        for result in self.results['products']:
            status_style = self.style.SUCCESS if result['status'] == 'SUCCESS' else self.style.ERROR
            self.stdout.write(f"Row {result['id']}: [{status_style(result['status'])}] {result['message']}")
        
        # Print Orders Results
        self.stdout.write("\n" + self.style.HTTP_INFO("ORDERS TABLE (orders.db):"))
        self.stdout.write("-" * 80)
        for result in self.results['orders']:
            status_style = self.style.SUCCESS if result['status'] == 'SUCCESS' else self.style.ERROR
            self.stdout.write(f"Row {result['id']}: [{status_style(result['status'])}] {result['message']}")
        
        # Print Summary
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("SUMMARY:"))
        self.stdout.write("-" * 80)
        
        users_success = sum(1 for r in self.results['users'] if r['status'] == 'SUCCESS')
        products_success = sum(1 for r in self.results['products'] if r['status'] == 'SUCCESS')
        orders_success = sum(1 for r in self.results['orders'] if r['status'] == 'SUCCESS')
        
        self.stdout.write(f"Users: {users_success}/10 successful insertions")
        self.stdout.write(f"Products: {products_success}/10 successful insertions")
        self.stdout.write(f"Orders: {orders_success}/10 successful insertions")
        self.stdout.write(f"Total execution time: {execution_time:.4f} seconds")
        self.stdout.write("="*80 + "\n")