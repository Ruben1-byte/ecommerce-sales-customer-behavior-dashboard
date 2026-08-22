import pandas as pd
import datetime as dt


# 1. MEMUAT DATASET & BERSIHKAN NAMA KOLOM
df = pd.read_csv('cleaned_ecommerce_sales.csv')

# Menghapus spasi tak terlihat di awal/akhir nama kolom
df.columns = df.columns.str.strip()

# Deteksi otomatis kolom tanggal
date_col = next((col for col in df.columns if 'date' in col.lower()), None)
if date_col:
    df['Order Date'] = pd.to_datetime(df[date_col])
else:
    raise KeyError(f"Kolom tanggal tidak ditemukan! Kolom yang ada: {df.columns.tolist()}")

# Deteksi/kalkulasi kolom Total Sales
if 'Total Sales' not in df.columns:
    qty_col = next((col for col in df.columns if 'qty' in col.lower() or 'quantity' in col.lower()), None)
    price_col = next((col for col in df.columns if 'price' in col.lower()), None)
    if qty_col and price_col:
        df['Total Sales'] = df[qty_col] * df[price_col]
    else:
        raise KeyError(f"Kolom Quantity/Price tidak ditemukan! Kolom yang ada: {df.columns.tolist()}")

# Deteksi nama kolom Customer ID (Fallback ke Order ID jika tidak ada ID pelanggan)
cust_col = next((col for col in df.columns if 'customer' in col.lower()), None)
if not cust_col:
    cust_col = next((col for col in df.columns if 'order' in col.lower() and 'date' not in col.lower()), df.columns[0])

# Deteksi nama kolom Order ID
order_id_col = next((col for col in df.columns if 'order' in col.lower() and 'date' not in col.lower()), df.columns[0])

print(f"Berhasil membaca dataset! Memproses {df[cust_col].nunique()} entitas unik...")


# 2. MENGHITUNG METRIK RFM (NAMED AGGREGATION)
snapshot_date = df['Order Date'].max() + dt.timedelta(days=1)

# Menggunakan as_index=False untuk menghindari bentrokan reset_index()
rfm = df.groupby(cust_col, as_index=False).agg(
    Recency=('Order Date', lambda x: (snapshot_date - x.max()).days),
    Frequency=(order_id_col, 'nunique'),
    Monetary=('Total Sales', 'sum')
)
# Samakan nama kolom identitas menjadi 'Customer Id'
rfm = rfm.rename(columns={cust_col: 'Customer Id'})


# 3. MEMBERIKAN SKOR RFM (1 - 4)
rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), q=4, labels=[1, 2, 3, 4])

rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)


# 4. MEMBUAT ATURAN SEGMENTASI PELANGGAN
def assign_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    
    if r >= 3 and f >= 3 and m >= 3:
        return 'Champions'
    elif r >= 3 and f >= 2:
        return 'Loyal'
    elif r >= 3 and f == 1:
        return 'Potential'
    elif r <= 2 and f >= 3:
        return 'At Risk'
    elif r <= 2 and f <= 2:
        return 'Hibernating'
    else:
        return 'Needs Attention'

rfm['Customer Segment'] = rfm.apply(assign_segment, axis=1)


# 5. MENAMPILKAN RINGKASAN & EKSPOR HASIL
print("\n--- DISTRIBUSI SEGMEN PELANGGAN ---")
print(rfm['Customer Segment'].value_counts())

print("\n--- RATA-RATA NILAI RFM PER SEGMEN ---")
print(rfm.groupby('Customer Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'Customer Id': 'count'
}).rename(columns={'Customer Id': 'Total Customers'}).round(1))

# Simpan hasil analisis ke file CSV
rfm.to_csv('rfm_customer_segments.csv', index=False)
print("\n[SUKSES] Berkas 'rfm_customer_segments.csv' telah disimpan!")