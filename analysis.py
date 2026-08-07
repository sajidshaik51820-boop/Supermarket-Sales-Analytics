import pandas as pd

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("data/supermarket_sales.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# ==========================
# BASIC INFORMATION
# ==========================
print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n" + "=" * 60)
print("TOTAL REVENUE")
print("=" * 60)
print(f"${df['revenue'].sum():,.2f}")

print("\n" + "=" * 60)
print("AVERAGE SALE")
print("=" * 60)
print(f"${df['revenue'].mean():.2f}")

print("\n" + "=" * 60)
print("REVENUE BY BRANCH")
print("=" * 60)
print(df.groupby("branch")["revenue"].sum().sort_values(ascending=False))

print("\n" + "=" * 60)
print("REVENUE BY PRODUCT LINE")
print("=" * 60)
print(df.groupby("product_line")["revenue"].sum().sort_values(ascending=False))

print("\n" + "=" * 60)
print("PAYMENT METHODS")
print("=" * 60)
print(df["payment_method"].value_counts())

print("\n" + "=" * 60)
print("CITY WISE REVENUE")
print("=" * 60)
print(df.groupby("city")["revenue"].sum().sort_values(ascending=False))

print("\n" + "=" * 60)
print("AVERAGE CUSTOMER RATING")
print("=" * 60)
print(round(df["rating"].mean(), 2))