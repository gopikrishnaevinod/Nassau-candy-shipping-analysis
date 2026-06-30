import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

st.title("🍬 Nassau Candy - Shipping Analysis Dashboard")
st.markdown("---")

# Load CSV files
df = pd.read_csv("cleaned_data.csv")
route_metrics = pd.read_csv("route_metrics.csv")
state_metrics = pd.read_csv("state_metrics.csv")
ship_mode_metrics = pd.read_csv("ship_mode_metrics.csv")

st.success("✓ Data loaded successfully!")

# FILTERS
st.sidebar.header("🔧 Filters")

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(pd.to_datetime(df["Order Date"]).min().date(),
           pd.to_datetime(df["Order Date"]).max().date())
)

selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_ship_modes = st.sidebar.multiselect(
    "Select Ship Mode(s)",
    options=sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

lead_time_threshold = st.sidebar.slider(
    "Lead Time Threshold (days)",
    min_value=0,
    max_value=int(df["Shipping_Lead_Time"].max()),
    value=7
)

selected_divisions = st.sidebar.multiselect(
    "Select Division(s)",
    options=sorted(df["Division"].unique()),
    default=sorted(df["Division"].unique())
)

df["Order Date"] = pd.to_datetime(df["Order Date"])

filtered_df = df[
    (df["Order Date"].dt.date >= date_range[0]) &
    (df["Order Date"].dt.date <= date_range[1]) &
    (df["Region"].isin(selected_regions)) &
    (df["Ship Mode"].isin(selected_ship_modes)) &
    (df["Division"].isin(selected_divisions))
]

# Metrics
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{len(filtered_df):,}")
col2.metric("Avg Lead Time", f"{filtered_df['Shipping_Lead_Time'].mean():.1f} days")
col3.metric(
    "On Time Rate",
    f"{(filtered_df['Shipping_Lead_Time'] <= lead_time_threshold).mean()*100:.1f}%"
)
col4.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")

st.markdown("---")

# Charts
st.subheader("🐢 Bottom 10 Slowest Routes")
bottom_10 = route_metrics.nlargest(10, "Avg_Lead_Time")
fig1 = px.bar(bottom_10, x="Avg_Lead_Time", y="Route", orientation="h",
              title="Slowest Routes")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("⚡ Top 10 Fastest Routes")
top_10 = route_metrics.nsmallest(10, "Avg_Lead_Time")
fig2 = px.bar(top_10, x="Avg_Lead_Time", y="Route", orientation="h",
              title="Fastest Routes")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🗺️ State Performance")
fig3 = px.bar(state_metrics, x="State/Province",
              y="Avg_Lead_Time",
              title="Average Lead Time by State")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🚚 Shipping Mode Performance")
fig4 = px.bar(ship_mode_metrics,
              x="Ship Mode",
              y="Avg_Lead_Time",
              title="Average Lead Time by Ship Mode")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("📋 Route Metrics Table")
st.dataframe(route_metrics.head(20), use_container_width=True)

st.caption("Nassau Candy Distributor - Shipping Route Efficiency Analysis Dashboard")
