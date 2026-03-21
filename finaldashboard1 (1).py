import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Analytics Dashboard", layout="wide")

st.title("📊 Customer Analytics Dashboard")

# ---------------------------
# LOAD DATA
# ---------------------------
rfm = pd.read_csv("rfm.csv")
cohort = pd.read_csv("cohort_clean.csv")
basket = pd.read_csv("basket_clean.csv")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=rfm["segment_label"].unique(),
    default=rfm["segment_label"].unique()
)

rfm = rfm[rfm["segment_label"].isin(segment_filter)]

# ---------------------------
# KPI SECTION
# ---------------------------
st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", rfm["CustomerID"].nunique())
col2.metric("Total Revenue", int(rfm["monetary"].sum()))
col3.metric("Total Rules", len(basket))

# ---------------------------
# RFM SEGMENTATION
# ---------------------------
st.subheader("RFM Segmentation")

segment_data = rfm.groupby("segment_label")["CustomerID"].count()

st.bar_chart(segment_data)

# ---------------------------
# COHORT ANALYSIS
# ---------------------------
st.subheader("Cohort Retention Analysis")

pivot = cohort.pivot(index="CohortMonth", columns="MonthNumber", values="CustomerCount")

fig, ax = plt.subplots()
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)

st.pyplot(fig)

# ---------------------------
# MARKET BASKET
# ---------------------------
st.subheader("Market Basket Analysis")

st.dataframe(basket)

top_rules = basket.sort_values(by="confidence", ascending=False).head(10)

st.subheader("Top Product Associations")

st.bar_chart(top_rules.set_index("antecedents")["confidence"])

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown("Project: Customer Analytics (RFM + Cohort + Market Basket)")