import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 40px;
    font-weight: 700;
}

.subtitle {
    font-size: 17px;
    opacity: 0.7;
    margin-bottom: 25px;
}

div[data-testid="stMetric"] {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.25);
    background-color: rgba(128,128,128,0.05);
}

div[data-testid="stMetricLabel"] {
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    font-size: 25px;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data/supermarket_sales.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


df = load_data()


# SIDEBAR

st.sidebar.title("🛒 Sales Analytics")
st.sidebar.markdown("### 🔍 Filters")

branch_options = sorted(df["branch"].dropna().unique())

branch = st.sidebar.multiselect(
    "🏢 Branch",
    branch_options,
    default=branch_options
)

city_options = sorted(df["city"].dropna().unique())

city = st.sidebar.multiselect(
    "📍 City",
    city_options,
    default=city_options
)

product_options = sorted(df["product_line"].dropna().unique())

product = st.sidebar.multiselect(
    "🛍️ Product Line",
    product_options,
    default=product_options
)


# DATE FILTER

valid_dates = df["date"].dropna()

if not valid_dates.empty:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:

    date_range = None


# FILTER DATA

filtered_df = df[
    (df["branch"].isin(branch)) &
    (df["city"].isin(city)) &
    (df["product_line"].isin(product))
].copy()


if date_range and len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["date"] >= start_date) &
        (filtered_df["date"] <= end_date)
    ]


# TITLE

st.markdown(
    '<div class="main-title">🛒 Supermarket Sales Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive Business Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# EMPTY DATA

if filtered_df.empty:

    st.warning("⚠️ No data found for the selected filters.")
    st.stop()


# KPI CALCULATIONS

total_revenue = filtered_df["revenue"].sum()

transactions = len(filtered_df)

average_sale = filtered_df["revenue"].mean()

gross_income = filtered_df["gross_income"].sum()

best_branch = (
    filtered_df
    .groupby("branch")["revenue"]
    .sum()
    .idxmax()
)

best_product = (
    filtered_df
    .groupby("product_line")["revenue"]
    .sum()
    .idxmax()
)


# BUSINESS OVERVIEW

st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🧾 Transactions",
        f"{transactions:,}"
    )

with col3:
    st.metric(
        "💵 Average Sale",
        f"${average_sale:,.2f}"
    )

with col4:
    st.metric(
        "📈 Gross Income",
        f"${gross_income:,.0f}"
    )


# TOP PERFORMERS

st.divider()

st.subheader("🏆 Top Performers")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"🏢 **Best Branch:** {best_branch}"
    )

with col2:
    st.info(
        f"🛍️ **Best Product Line:** {best_product}"
    )


# SALES PERFORMANCE

st.divider()

st.subheader("📈 Sales Performance")


# BRANCH REVENUE

branch_sales = (
    filtered_df
    .groupby(
        "branch",
        as_index=False
    )["revenue"]
    .sum()
    .sort_values(
        "revenue",
        ascending=False
    )
)

fig_branch = px.bar(
    branch_sales,
    x="branch",
    y="revenue",
    title="Revenue by Branch",
    text="revenue",
    labels={
        "branch": "Branch",
        "revenue": "Revenue ($)"
    }
)

fig_branch.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_branch.update_layout(
    height=400,
    showlegend=False
)


# PRODUCT REVENUE

product_sales = (
    filtered_df
    .groupby(
        "product_line",
        as_index=False
    )["revenue"]
    .sum()
    .sort_values(
        "revenue",
        ascending=True
    )
)

fig_product = px.bar(
    product_sales,
    x="revenue",
    y="product_line",
    orientation="h",
    title="Revenue by Product Line",
    text="revenue",
    labels={
        "product_line": "Product Line",
        "revenue": "Revenue ($)"
    }
)

fig_product.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_product.update_layout(
    height=400,
    showlegend=False
)


# DISPLAY CHARTS

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig_branch,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


# TOP 5 PRODUCTS

st.divider()

st.subheader("🔥 Top 5 Product Lines")

top_products = (
    filtered_df
    .groupby(
        "product_line",
        as_index=False
    )["revenue"]
    .sum()
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(5)
)

fig_top = px.bar(
    top_products,
    x="revenue",
    y="product_line",
    orientation="h",
    title="Top Product Lines by Revenue",
    text="revenue",
    labels={
        "product_line": "Product Line",
        "revenue": "Revenue ($)"
    }
)

fig_top.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_top.update_layout(
    height=400,
    showlegend=False
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)


# CUSTOMER ANALYSIS

st.divider()

st.subheader("👥 Customer Analysis")

col1, col2 = st.columns(2)


gender_sales = (
    filtered_df
    .groupby(
        "gender_customer",
        as_index=False
    )["revenue"]
    .sum()
)

fig_gender = px.pie(
    gender_sales,
    names="gender_customer",
    values="revenue",
    title="Revenue by Customer Gender",
    hole=0.45
)

with col1:
    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


customer_type_sales = (
    filtered_df
    .groupby(
        "customer_type",
        as_index=False
    )["revenue"]
    .sum()
)

fig_customer = px.bar(
    customer_type_sales,
    x="customer_type",
    y="revenue",
    title="Revenue by Customer Type",
    text="revenue",
    labels={
        "customer_type": "Customer Type",
        "revenue": "Revenue ($)"
    }
)

fig_customer.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_customer.update_layout(
    showlegend=False,
    height=400
)

with col2:
    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )


# PAYMENT ANALYSIS

st.divider()

st.subheader("💳 Payment Analysis")

payment_sales = (
    filtered_df
    .groupby(
        "payment_method",
        as_index=False
    )["revenue"]
    .sum()
)

fig_payment = px.pie(
    payment_sales,
    names="payment_method",
    values="revenue",
    title="Revenue by Payment Method",
    hole=0.5
)

fig_payment.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)


# MONTHLY TREND

st.divider()

st.subheader("📅 Revenue Trend")

monthly_df = filtered_df.dropna(
    subset=["date"]
).copy()

monthly_df["month_number"] = (
    monthly_df["date"].dt.month
)

monthly_df["month"] = (
    monthly_df["date"].dt.strftime("%b")
)

monthly_sales = (
    monthly_df
    .groupby(
        ["month_number", "month"],
        as_index=False
    )["revenue"]
    .sum()
    .sort_values(
        "month_number"
    )
)

fig_month = px.line(
    monthly_sales,
    x="month",
    y="revenue",
    title="Monthly Revenue Trend",
    markers=True,
    labels={
        "month": "Month",
        "revenue": "Revenue ($)"
    }
)

fig_month.update_traces(
    line_width=3
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)


# BUSINESS INSIGHTS

st.divider()

st.subheader("💡 Business Insights")

top_product_name = top_products.iloc[0]["product_line"]

top_product_revenue = top_products.iloc[0]["revenue"]

best_payment_row = (
    payment_sales
    .sort_values(
        "revenue",
        ascending=False
    )
    .iloc[0]
)

best_payment = best_payment_row["payment_method"]

best_payment_revenue = best_payment_row["revenue"]


col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"🏆 **Best Branch**\n\n"
        f"{best_branch} generates the highest revenue."
    )

with col2:
    st.info(
        f"🔥 **Top Product**\n\n"
        f"{top_product_name} leads with "
        f"${top_product_revenue:,.0f} revenue."
    )

with col3:
    st.warning(
        f"💳 **Top Payment Method**\n\n"
        f"{best_payment} generates "
        f"${best_payment_revenue:,.0f} revenue."
    )


# DOWNLOAD

st.divider()

st.subheader("📥 Download Report")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Filtered Sales Data",
    data=csv_data,
    file_name="supermarket_filtered_sales.csv",
    mime="text/csv"
)


# DATA PREVIEW

st.divider()

with st.expander("📋 View Dataset Preview"):

    st.caption(
        f"Showing first 10 records from "
        f"{len(filtered_df):,} filtered transactions."
    )

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True,
        hide_index=True
    )


# FOOTER

st.divider()

st.caption(
    "Supermarket Sales Analytics • "
    "Python • Pandas • Plotly • Streamlit"
)