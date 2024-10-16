from django.db import connection

def generate_order_number():
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM orders')
    count = cursor.fetchone()[0] + 1
    order_number = f'ORD{count:05d}'  # Ensures consistent 5-digit format
    return order_number