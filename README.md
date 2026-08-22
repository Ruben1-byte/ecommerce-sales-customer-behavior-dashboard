# 📊 E-Commerce Sales & Customer Behavior Dashboard

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange?logo=mysql&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-Desktop-E97627?logo=tableau&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white)

Proyek **End-to-End Data Analytics & Machine Learning Pipeline** yang menganalisis **1.500+ baris data transaksi e-commerce** untuk memahami tren penjualan, performa kategori produk, segmentasi perilaku pelanggan (RFM), serta pemodelan prediksi risiko *Customer Churn*.

---

## 📌 Executive Summary & Key KPIs

Berdasarkan hasil pemrosesan dan analisis data transaksi, diperoleh indikator kinerja utama (*Key Performance Indicators*):

- **Total Revenue:** Rp 6.368.650.000
- **Total Transactions:** 1.500 Pesanan
- **Top Category:** **Electronics** menyumbang pendapatan tertinggi.
- **Payment Method Distribution:** Terdistribusi seimbang antara *Credit Card*, *E-Wallet*, *Bank Transfer*, dan *QRIS*.

---

## 📁 Repository Structure

```text
E-Commerce Sales & Customer Behavior Dashboard/
├── dashboard/
│   └── E-Commerce Sales & Customer Behavior Dashboard.twbx  # Tableau Workbook
├── data/
│   ├── cleaned_ecommerce_sales.csv                         # Cleaned sales dataset
│   └── rfm_customer_segments.csv                           # RFM Output dataset
├── images/
│   ├── Customer Insights.png                               # Screenshot Dashboard 2
│   ├── Dashboard 1.png                                     # Screenshot Dashboard 1
│   └── feature_importance.png                              # ML Feature Importance Chart
├── notebooks/                                              # EDA & Prototyping
├── script/
│   ├── datacleaning.py                                     # Python Data Cleaning
│   ├── load_to_mysql.py                                    # Automated MySQL Ingestion
│   ├── rfm_analysis.py                                     # RFM Segmentation Script
│   └── churn_prediction.py                                 # Scikit-Learn ML Churn Model
├── sql/
│   ├── create_tables_and_indexes.sql                       # MySQL DDL & Indexing
│   └── analytical_queries.sql                              # CTE & Window Functions
├── .gitignore
└── README.md

🔄 End-to-End Analytics Pipeline
[ Raw CSV Data ]
       │
       ▼
[ Python Data Cleaning ] (datacleaning.py)
       │
       ├─────────────────────────────────────────┐
       ▼                                         ▼
[ MySQL Database ] (load_to_mysql.py)     [ Tableau Dashboards ]
       │                                  - Sales Overview (Dashboard 1)
       ├────────────────────────┐         - Customer Insights (Dashboard 2)
       ▼                        ▼
[ SQL Analytical Queries ]   [ Feature Engineering ]
(analytical_queries.sql)     (churn_prediction.py)
                                │
                                ▼
                     [ Random Forest Churn Model ]

🧹 Pembersihan & Transmisi Data (Python)
Proses manipulasi data dilakukan di script/datacleaning.py dan script/load_to_mysql.py:
Data Cleaning: Menangani missing values, duplikasi, standarisasi tipe data tanggal (DATETIME), serta pembersihan whitespace.
MySQL Ingestion: Mengonversi DataFrame ke tabel relasional MySQL (ecommerce_db.sales) menggunakan SQLAlchemy & PyMySQL dengan presisi tipe data (SMALLINT UNSIGNED, DECIMAL, VARCHAR).

🗄️ Database Optimization & Analytical SQL
Pengindeksan dilakukan di sql/create_tables_and_indexes.sql untuk mempercepat eksekusi query:

SQL
ALTER TABLE sales ADD PRIMARY KEY (order_id);
ALTER TABLE sales ADD INDEX idx_order_date (order_date);
ALTER TABLE sales ADD INDEX idx_category (category);
Sampel Query Analitis (sql/analytical_queries.sql)

1. Top 3 Produk Terlaris per Kategori (DENSE_RANK)
SQL
WITH product_rankings AS (
    SELECT 
        category,
        product_name,
        SUM(quantity) AS total_quantity_sold,
        SUM(total_sales) AS total_revenue_generated,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY SUM(quantity) DESC) AS rank_position
    FROM sales
    GROUP BY category, product_name
)
SELECT category, product_name, total_quantity_sold, total_revenue_generated
FROM product_rankings
WHERE rank_position <= 3
ORDER BY category, rank_position;

2. Pertumbuhan Penjualan Bulanan / MoM Growth (LAG)
SQL
WITH monthly_perf AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS month_year,
        SUM(total_sales) AS total_revenue,
        COUNT(order_id) AS total_orders
    FROM sales
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    month_year,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY month_year) AS prev_month_revenue,
    ROUND(((total_revenue - LAG(total_revenue) OVER (ORDER BY month_year)) / LAG(total_revenue) OVER (ORDER BY month_year)) * 100, 2) AS mom_growth_percent
FROM monthly_perf;

💡 Customer Insights & RFM Segmentation
Mengelompokkan pelanggan berdasarkan kriteria Recency, Frequency, & Monetary (script/rfm_analysis.py):
Champions (195 Pelanggan): Segmen paling bernilai dengan rata-rata nilai transaksi mencapai Rp 8,03 Juta per pelanggan.
At-Risk & Hibernating (743 Pelanggan): Mencakup ~49.5% dari total pelanggan yang sudah lama tidak bertransaksi. Sangat membutuhkan strategi kampanye win-back.
Loyal & Potential (562 Pelanggan): Pelanggan aktif yang berpotensi ditingkatkan nilai belanjanya melalui upselling / cross-selling.

🤖 Machine Learning: Customer Churn Prediction
Memprediksi potensi pelanggan mengalami Churn (1) jika tidak bertransaksi dalam > 90 hari terakhir.
Python
# Algoritma: Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier

X = df_ml[["quantity", "unit_price", "total_sales"]]
y = df_ml["is_churn"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

📈 Evaluasi Model & Feature Engineering
Penanganan Target Leakage: Pengujian awal memasukkan recency_days ke dalam fitur X, menghasilkan skor sempurna buatan (ROC-AUC 1.00). Untuk menghindari data leakage, fitur recency_days diisolasi.
Hasil Model Baseline:
Accuracy: 56%
ROC-AUC Score: 0.5195

Feature Importance:
total_sales (46.67%)
unit_price (34.84%)
quantity (18.48%)

Learning Point ML: Murni variabel transaksi tunggal belum cukup kuat memprediksi churn secara independen. Diperlukan penambahan fitur agregasi riwayat belanja (Customer-level Aggregate Features) untuk meningkatkan akurasi pemodelan selanjutnya.

🖼️ Dashboard Preview & Structure
1. Sales Overview Dashboard
Fokus pada tren penjualan bulanan, performa kategori produk, dan distribusi metode pembayaran.

2. Customer Insights Dashboard
Fokus pada peta sebaran pelanggan dan analisis segmentasi RFM.

🚀 Cara Menjalankan Proyek Secara Lokal
Clone Repository:

Bash
git clone [https://github.com/Ruben1-byte/ecommerce-sales-customer-behavior-dashboard.git](https://github.com/Ruben1-byte/ecommerce-sales-customer-behavior-dashboard.git)
cd ecommerce-sales-customer-behavior-dashboard
Aktifkan Virtual Environment & Install Dependencies:

PowerShell
python -m venv .venv
.\.venv\Scripts\activate
pip install pandas sqlalchemy pymysql scikit-learn matplotlib seaborn
Jalankan Ingest MySQL & Machine Learning:

PowerShell
# 1. Pastikan Service MySQL/XAMPP aktif
python script/load_to_mysql.py

# 2. Jalankan Model Prediksi Churn
python script/churn_prediction.py
