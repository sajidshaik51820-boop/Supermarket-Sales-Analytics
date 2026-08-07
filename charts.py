import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# Load Dataset
# ==========================
df = pd.read_csv("data/supermarket_sales.csv")

# Convert date column (works with mixed formats)
df["date"] = pd.to_datetime(df["date"], format="mixed")

# -------------------------------
# Revenue by Branch (Bar Chart)
# -------------------------------
branch_sales = df.groupby("branch")["revenue"].sum()

plt.figure(figsize=(6, 4))
plt.bar(branch_sales.index, branch_sales.values)
plt.title("Revenue by Branch")
plt.xlabel("Branch")
plt.ylabel("Revenue")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("branch_sales.png")
plt.close()

# -------------------------------
# Payment Method (Pie Chart)
# -------------------------------
payment = df["payment_method"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(
    payment.values,
    labels=payment.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Payment Methods")
plt.tight_layout()
plt.savefig("payment_methods.png")
plt.close()

# -------------------------------
# Monthly Revenue (Line Chart)
# -------------------------------
df["month"] = df["date"].dt.month_name()

monthly_sales = (
    df.groupby("month")["revenue"]
      .sum()
)

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales = monthly_sales.reindex(month_order).dropna()

plt.figure(figsize=(8, 4))
plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=2
)
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=30)
plt.grid(alpha=0.4)
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.close()

# -------------------------------
# Product Line Revenue
# -------------------------------
product = (
    df.groupby("product_line")["revenue"]
      .sum()
      .sort_values()
)

plt.figure(figsize=(9, 5))
plt.barh(product.index, product.values)
plt.title("Revenue by Product Line")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig("product_sales.png")
plt.close()

# -------------------------------
# Customer Rating Distribution
# -------------------------------
plt.figure(figsize=(6, 4))
plt.hist(df["rating"], bins=10)
plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Customers")
plt.tight_layout()
plt.savefig("ratings.png")
plt.close()

print("=" * 60)
print("All charts generated successfully!")
print("=" * 60)

print("\nGenerated Files:")
print("✅ branch_sales.png")
print("✅ payment_methods.png")
print("✅ monthly_sales.png")
print("✅ product_sales.png")
print("✅ ratings.png")
