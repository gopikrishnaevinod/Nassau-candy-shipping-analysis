import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

st.title("🍬 Nassau Candy - Shipping Analysis Dashboard")
st.markdown("---")

# Load CSV files from GitHub
try:
    df = pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/cleaned_data.csv')
    route_metrics = pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/route_metrics.csv')
    state_metrics = pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/state_metrics.csv')
    ship_mode_metrics = pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/ship_mode_metrics.csv')
    st.success("✓ Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ===== TAB 1: OVERVIEW =====
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{len(df):,}")
col2.metric("Avg Lead Time", f"{df['Shipping_Lead_Time'].mean():.1f} days")
col3.metric("Total Routes", "100")
col4.metric("Total Sales", f"${df['Sales'].sum():,.0f}")

st.markdown("---")

# ===== SLOWEST ROUTES =====
st.subheader("🐢 Bottom 10 Slowest Routes")
bottom_10 = route_metrics.nlargest(10, 'Avg_Lead_Time')[['Route', 'Avg_Lead_Time', 'Total_Shipments']]
fig1 = px.bar(bottom_10, x='Avg_Lead_Time', y='Route', orientation='h', 
              title='Slowest Routes', color='Avg_Lead_Time', color_continuous_scale='Reds')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ===== FASTEST ROUTES =====
st.subheader("⚡ Top 10 Fastest Routes")
top_10 = route_metrics.nsmallest(10, 'Avg_Lead_Time')[['Route', 'Avg_Lead_Time', 'Total_Shipments']]
fig2 = px.bar(top_10, x='Avg_Lead_Time', y='Route', orientation='h',
              title='Fastest Routes', color='Avg_Lead_Time', color_continuous_scale='Greens')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ===== STATE PERFORMANCE =====
st.subheader("🗺️ Top 10 Slowest States")
top_slow_states = state_metrics.nlargest(10, 'Avg_Lead_Time')[['State/Province', 'Avg_Lead_Time', 'Shipment_Count']]
fig3 = px.bar(top_slow_states, x='Avg_Lead_Time', y='State/Province', orientation='h',
              title='States with Highest Lead Times', color='Avg_Lead_Time', color_continuous_scale='Oranges')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ===== SHIP MODE COMPARISON =====
st.subheader("🚚 Shipping Mode Performance")
fig4 = px.bar(ship_mode_metrics, x='Ship Mode', y='Avg_Lead_Time',
              title='Average Lead Time by Ship Mode', color='Avg_Lead_Time', color_continuous_scale='Blues')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ===== DATA TABLES =====
st.subheader("📋 Route Metrics Table")
st.dataframe(route_metrics.head(20), use_container_width=True)

st.markdown("---")
st.caption("Nassau Candy Distributor - Shipping Route Efficiency Analysis Dashboard")
