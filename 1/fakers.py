import random
from datetime import datetime, timedelta
from faker import Faker
import csv

# Initialize Faker
fake = Faker()

# Function to generate random dates
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# CSV file setup
with open('ecommerce_data.csv', mode='w', newline='') as csv_file:
    fieldnames = [
        'ID', 'ProductID', 'ProductName', 'Category', 'VariantID', 'VariantName', 'Price',
        'CustomerID', 'CustomerName', 'CustomerEmail', 'OrderID', 'OrderDate', 'Quantity', 'TotalAmount'
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()

    categories = ['Clothing', 'Groceries', 'Electronics', 'Books', 'Home & Garden']
    product_names = ['T-Shirt', 'Laptop', 'Apple', 'Jeans', 'Headphones', 'Novel', 'Blender', 'Smartphone', 'Desk Lamp', 'Sneakers']

    record_id = 1
    variant_id = 1

    # Insert sample products and variants
    product_variant_map = {}
    for product_id in range(1, 51):  # Increased to 50 products
        product_name = random.choice(product_names)
        category = random.choice(categories)

        num_variants = random.randint(1, 3)
        product_variant_map[product_id] = []
        for _ in range(num_variants):
            variant_name = fake.color_name()
            price = round(random.uniform(10, 1000), 2)

            writer.writerow({
                'ID': record_id, 'ProductID': product_id, 'ProductName': product_name, 'Category': category,
                'VariantID': variant_id, 'VariantName': variant_name, 'Price': price,
                'CustomerID': '', 'CustomerName': '', 'CustomerEmail': '', 'OrderID': '', 'OrderDate': '', 'Quantity': '', 'TotalAmount': ''
            })

            product_variant_map[product_id].append(variant_id)
            record_id += 1
            variant_id += 1

    # Insert sample customers
    customer_ids = []
    for customer_id in range(1, 101):  # Increased to 100 customers
        customer_name = fake.name()
        customer_email = fake.email()
        customer_ids.append(customer_id)

        writer.writerow({
            'ID': record_id, 'ProductID': '', 'ProductName': '', 'Category': '',
            'VariantID': '', 'VariantName': '', 'Price': '',
            'CustomerID': customer_id, 'CustomerName': customer_name, 'CustomerEmail': customer_email, 
            'OrderID': '', 'OrderDate': '', 'Quantity': '', 'TotalAmount': ''
        })

        record_id += 1

    # Insert sample orders and order items
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    current_date = start_date

    order_id = 1
    while current_date <= end_date:
        num_orders = random.randint(1, 10)  # 1-10 orders per day
        for _ in range(num_orders):
            customer_id = random.choice(customer_ids)
            total_amount = 0

            writer.writerow({
                'ID': record_id, 'ProductID': '', 'ProductName': '', 'Category': '',
                'VariantID': '', 'VariantName': '', 'Price': '',
                'CustomerID': customer_id, 'CustomerName': '', 'CustomerEmail': '', 
                'OrderID': order_id, 'OrderDate': current_date.date(), 'Quantity': '', 'TotalAmount': ''
            })

            record_id += 1

            num_items = random.randint(1, 5)
            for _ in range(num_items):
                product_id = random.choice(list(product_variant_map.keys()))
                variant_id = random.choice(product_variant_map[product_id])
                quantity = random.randint(1, 10)
                price_at_purchase = round(random.uniform(10, 1000), 2)
                item_total = quantity * price_at_purchase
                total_amount += item_total

                writer.writerow({
                    'ID': record_id, 'ProductID': product_id, 'ProductName': '', 'Category': '',
                    'VariantID': variant_id, 'VariantName': '', 'Price': price_at_purchase,
                    'CustomerID': '', 'CustomerName': '', 'CustomerEmail': '', 
                    'OrderID': order_id, 'OrderDate': '', 'Quantity': quantity, 'TotalAmount': item_total
                })

                record_id += 1

            # Update the total amount for the order
            writer.writerow({
                'ID': record_id, 'ProductID': '', 'ProductName': '', 'Category': '',
                'VariantID': '', 'VariantName': '', 'Price': '',
                'CustomerID': '', 'CustomerName': '', 'CustomerEmail': '', 
                'OrderID': order_id, 'OrderDate': '', 'Quantity': '', 'TotalAmount': round(total_amount, 2)
            })

            record_id += 1
            order_id += 1

        current_date += timedelta(days=1)

print(f"Data generation complete. Total records: {record_id - 1}")