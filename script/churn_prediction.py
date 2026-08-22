import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine

# 1. Pastikan folder images/ tersedia
os.makedirs("images", exist_ok=True)

# 2. Koneksi ke Database MySQL (root tanpa password)
engine = create_engine("mysql+pymysql://root:@localhost:3306/ecommerce_db")

# 3. Ekstraksi Fitur dari MySQL
query_ml = """
WITH max_date_ref AS (
    SELECT MAX(order_date) AS max_date FROM sales
)
SELECT 
    order_id,
    DATEDIFF((SELECT max_date FROM max_date_ref), order_date) AS recency_days,
    quantity,
    unit_price,
    total_sales,
    CASE WHEN DATEDIFF((SELECT max_date FROM max_date_ref), order_date) > 90 THEN 1 ELSE 0 END AS is_churn
FROM sales;
"""

print("Mengambil dataset dari database MySQL...")
df_ml = pd.read_sql(query_ml, con=engine)

# Keluarkan recency_days dari fitur X untuk menghindari Data Leakage
feature_cols = ["quantity", "unit_price", "total_sales"]
X = df_ml[feature_cols]
y = df_ml["is_churn"]

# Split Dataset (80% Training, 20% Testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Training Model Random Forest
print("Melatih model Machine Learning (Random Forest)...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluasi Model
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("\n" + "=" * 45)
print("       LAPORAN EVALUASI MODEL CHURN")
print("=" * 45)
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

# 7. Feature Importance Analysis
importances = model.feature_importances_
df_importance = pd.DataFrame(
    {"Feature": feature_cols, "Importance": importances}
).sort_values(by="Importance", ascending=False)

print("\n" + "=" * 45)
print("    FEATURE IMPORTANCE (Pengaruh Variabel)")
print("=" * 45)
print(df_importance.to_string(index=False))

# 8. Simpan Visualisasi
plt.figure(figsize=(8, 4))
sns.barplot(
    x="Importance",
    y="Feature",
    data=df_importance,
    hue="Feature",
    palette="viridis",
    legend=False,
)
plt.title("Faktor Utama yang Mempengaruhi Churn Pelanggan")
plt.xlabel("Tingkat Kepentingan (Importance)")
plt.ylabel("Variabel")
plt.tight_layout()
plt.savefig("images/feature_importance.png")

print(
    "\nGrafik Feature Importance berhasil disimpan ke 'images/feature_importance.png'!"
)