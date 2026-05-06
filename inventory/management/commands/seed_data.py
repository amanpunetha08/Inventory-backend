from datetime import datetime
from django.core.management.base import BaseCommand
from inventory.db import db


class Command(BaseCommand):
    help = 'Seed dummy data into MongoDB'

    def handle(self, *args, **options):
        user = 'amanpunetha0305@gmail.com'

        # Categories
        categories = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'Wearables', 'description': 'Smartwatches and fitness trackers', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'Accessories', 'description': 'Cables, stands, and peripherals', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'Audio', 'description': 'Speakers, headphones, and microphones', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'Computing', 'description': 'Laptops, desktops, and components', 'user': user, 'created_at': datetime.utcnow()},
        ]
        db['categories'].delete_many({'user': user})
        db['categories'].insert_many(categories)

        # Suppliers
        suppliers = [
            {'name': 'TechWorld Distributors', 'email': 'sales@techworld.com', 'phone': '+1-555-0101', 'address': '123 Tech Blvd, San Jose, CA', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'Global Electronics Co', 'email': 'orders@globalelec.com', 'phone': '+1-555-0202', 'address': '456 Circuit Ave, Austin, TX', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'AudioPro Supplies', 'email': 'info@audiopro.com', 'phone': '+1-555-0303', 'address': '789 Sound St, Nashville, TN', 'user': user, 'created_at': datetime.utcnow()},
            {'name': 'WearTech Inc', 'email': 'supply@weartech.io', 'phone': '+1-555-0404', 'address': '321 Gadget Ln, Seattle, WA', 'user': user, 'created_at': datetime.utcnow()},
        ]
        db['suppliers'].delete_many({'user': user})
        db['suppliers'].insert_many(suppliers)

        # Items
        items = [
            {'name': 'Wireless Headphones', 'sku': 'WH-1000XM5', 'category': 'Electronics', 'quantity': 3, 'price': 349.99, 'description': 'Premium noise-cancelling headphones', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Smart Watch Series 8', 'sku': 'SWS8-45MM', 'category': 'Wearables', 'quantity': 2, 'price': 399.99, 'description': 'Advanced health monitoring smartwatch', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'USB-C Cable', 'sku': 'USBCC-1M', 'category': 'Accessories', 'quantity': 0, 'price': 9.99, 'description': '1m braided USB-C cable', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Bluetooth Speaker', 'sku': 'BS-FLIP6', 'category': 'Electronics', 'quantity': 1, 'price': 129.99, 'description': 'Portable waterproof speaker', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Laptop Stand', 'sku': 'LTS-ALU', 'category': 'Accessories', 'quantity': 15, 'price': 49.99, 'description': 'Aluminum adjustable laptop stand', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Wireless Mouse', 'sku': 'WM-5000', 'category': 'Electronics', 'quantity': 28, 'price': 24.99, 'description': 'Ergonomic wireless mouse', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Mechanical Keyboard', 'sku': 'MK-PRO65', 'category': 'Electronics', 'quantity': 12, 'price': 159.99, 'description': '65% mechanical keyboard with RGB', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': '4K Monitor', 'sku': 'MON-27-4K', 'category': 'Computing', 'quantity': 5, 'price': 449.99, 'description': '27 inch 4K IPS display', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Webcam HD', 'sku': 'WC-1080P', 'category': 'Accessories', 'quantity': 20, 'price': 79.99, 'description': '1080p webcam with microphone', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Fitness Tracker', 'sku': 'FT-BAND7', 'category': 'Wearables', 'quantity': 0, 'price': 59.99, 'description': 'Water-resistant fitness band', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Portable SSD 1TB', 'sku': 'SSD-1TB-EX', 'category': 'Computing', 'quantity': 8, 'price': 109.99, 'description': 'External SSD USB 3.2', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
            {'name': 'Noise Cancelling Earbuds', 'sku': 'NCE-PRO2', 'category': 'Audio', 'quantity': 4, 'price': 199.99, 'description': 'True wireless ANC earbuds', 'user': user, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
        ]
        db['items'].delete_many({'user': user})
        db['items'].insert_many(items)

        # Orders
        orders = [
            {'product': 'Wireless Headphones', 'supplier': 'TechWorld Distributors', 'quantity': 50, 'total': 12500.00, 'status': 'Delivered', 'user': user, 'created_at': datetime.utcnow()},
            {'product': 'Smart Watch Series 8', 'supplier': 'WearTech Inc', 'quantity': 30, 'total': 9000.00, 'status': 'Shipped', 'user': user, 'created_at': datetime.utcnow()},
            {'product': 'USB-C Cable', 'supplier': 'Global Electronics Co', 'quantity': 200, 'total': 1200.00, 'status': 'Pending', 'user': user, 'created_at': datetime.utcnow()},
            {'product': 'Bluetooth Speaker', 'supplier': 'AudioPro Supplies', 'quantity': 25, 'total': 2500.00, 'status': 'Delivered', 'user': user, 'created_at': datetime.utcnow()},
            {'product': 'Mechanical Keyboard', 'supplier': 'TechWorld Distributors', 'quantity': 40, 'total': 4800.00, 'status': 'Shipped', 'user': user, 'created_at': datetime.utcnow()},
            {'product': '4K Monitor', 'supplier': 'Global Electronics Co', 'quantity': 10, 'total': 4500.00, 'status': 'Pending', 'user': user, 'created_at': datetime.utcnow()},
        ]
        db['orders'].delete_many({'user': user})
        db['orders'].insert_many(orders)

        # Notifications
        notifications = [
            {'message': 'Wireless Headphones stock is low (3 left)', 'type': 'warning', 'read': False, 'user': user, 'created_at': datetime.utcnow()},
            {'message': 'USB-C Cable is out of stock', 'type': 'alert', 'read': False, 'user': user, 'created_at': datetime.utcnow()},
            {'message': 'Fitness Tracker is out of stock', 'type': 'alert', 'read': False, 'user': user, 'created_at': datetime.utcnow()},
            {'message': 'Order #3 from Global Electronics Co is pending', 'type': 'info', 'read': True, 'user': user, 'created_at': datetime.utcnow()},
        ]
        db['notifications'].delete_many({'user': user})
        db['notifications'].insert_many(notifications)

        self.stdout.write(self.style.SUCCESS('Dummy data seeded successfully for demo@gmail.com'))
