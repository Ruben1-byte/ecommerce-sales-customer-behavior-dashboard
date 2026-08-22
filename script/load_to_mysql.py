import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy.dialects.mysql import SMALLINT

# 1. Load dataset bersih dari folder data/
df = pd.read_csv("data/cleaned_ecommerce_sales.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# 2. Definisikan pemetaan tipe data presisi MySQL
dtype_mapping = {
    "order_id": types.VARCHAR(50),
    "customer_id": types.VARCHAR(50),
    "order_date": types.DATETIME(),
    "category": types.VARCHAR(50),
    "quantity": SMALLINT(unsigned=True),
    "price": types.DECIMAL(10, 2),
    "total_amount": types.DECIMAL(12, 2),
}

# 3. Koneksi ke MySQL (root tanpa password -> root:@localhost:3306)
engine = create_engine("mysql+pymysql://root:@localhost:3306/ecommerce_db")

# 4. Impor data ke tabel 'sales'
df.to_sql(
    "sales", con=engine, if_exists="replace", index=False, dtype=dtype_mapping
)

print("Impor data ke MySQL berhasil!")