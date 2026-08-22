import pandas as pd
import numpy as np

# 1. Generate Dataset Simulasi (Atau Import CSV E-Commerce Anda)
np.random.seed(42)
n_rows = 1500

dates = pd.date_range(start='2026-01-01', end='2026-08-10', freq='h')
order_dates = np.random.choice(dates, size=n_rows)

categories = ['Electronics', 'Fashion', 'Home & Living', 'Gadgets', 'Accessories']
products = {
    'Electronics': ('Laptop', 8500000),
    'Fashion': ('Kemeja Casual', 250000),
    'Home & Living': ('Lampu Meja', 150000),
    'Gadgets': ('Smartwatch', 1200000),
    'Accessories': ('Headphone Bluetooth', 450000)
}

data = []
for i in range(n_rows):
    cat = np.random.choice(categories)
    prod_name, price = products[cat]
    qty = np.random.randint(1, 4)
    payment = np.random.choice(['Midtrans - Bank Transfer', 'Midtrans - QRIS', 'Credit Card', 'E-Wallet'])
    status = np.random.choice(['Paid', 'Paid', 'Paid', 'Pending', 'Failed'], p=[0.75, 0.1, 0.05, 0.05, 0.05])
    
    data.append({
        'order_id': f'ORD-{10000 + i}',
        'order_date': order_dates[i],
        'category': cat,
        'product_name': prod_name,
        'unit_price': price,
        'quantity': qty,
        'payment_method': payment,
        'payment_status': status
    })

df = pd.DataFrame(data)

# 2. Data Cleaning & Feature Engineering
# Hapus duplikat (jika ada)
df.drop_duplicates(inplace=True)

# Tambahkan Kolom Kalkulasi
df['total_sales'] = df['unit_price'] * df['quantity']
df['order_month'] = df['order_date'].dt.strftime('%Y-%m')
df['order_day'] = df['order_date'].dt.day_name()

# Export Data Bersih ke CSV
df.to_csv('cleaned_ecommerce_sales.csv', index=False)
print("Data berhasil dibersihkan dan disimpan ke 'cleaned_ecommerce_sales.csv'!")