import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Nassau Candy - Shipping Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🍬 Nassau Candy Distributor - Shipping Route Efficiency Dashboard")
st.markdown("---")

# =====================================================
# LOAD DATA (with caching)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/cleaned_data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

@st.cache_data
def load_route_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/route_metrics.csv')

@st.cache_data
def load_state_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/state_metrics.csv')

@st.cache_data
def load_ship_mode_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopikrishnaevinod/nassau-candy-shipping-analysis/main/ship_mode_metrics.csv')

# Load all data
df = load_data()
route_metrics = load_route_metrics()
state_metrics = load_state_metrics()
ship_mode_metrics = load_ship_mode_metrics()

# =====================================================
# SIDEBAR - FILTERS
# =====================================================
st.sidebar.header("🔧 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Order Date'].min().date(), df['Order Date'].max().date()),
    min_value=df['Order Date'].min().date(),
    max_value=df['Order Date'].max().date()
)

# Region filter
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=sorted(df['Region'].unique()),
    default=sorted(df['Region'].unique())
)

# Ship Mode filter
selected_ship_modes = st.sidebar.multiselect(
    "Select Ship Mode(s)",
    options=sorted(df['Ship Mode'].unique()),
    default=sorted(df['Ship Mode'].unique())
)

# Lead time threshold
lead_time_threshold = st.sidebar.slider(
    "Lead Time Threshold (days)",
    min_value=0,
    max_value=int(df['Shipping_Lead_Time'].max()),
    value=7
)

# Division filter
selected_divisions = st.sidebar.multiselect(
    "Select Division(s)",
    options=sorted(df['Division'].unique()),
    default=sorted(df['Division'].unique())
)

# =====================================================
# APPLY FILTERS
# =====================================================
filtered_df = df[
    (df['Order Date'].dt.date >= date_range[0]) &
    (df['Order Date'].dt.date <= date_range[1]) &
    (df['Region'].isin(selected_regions)) &
    (df['Ship Mode'].isin(selected_ship_modes)) &
    (df['Division'].isin(selected_divisions))
]

# =====================================================
# CREATE TABS
# =====================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "🗺️ Geographic Analysis", "🚚 Ship Mode", "🛣️ Route Details", "📈 Trends"]
)

# =====================================================
# TAB 1: OVERVIEW
# =====================================================
with tab1:
    st.subheader("📊 Key Performance Metrics")
    
    # Metrics in 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Orders",
            f"{len(filtered_df):,}",
            f"{len(filtered_df) - len(df) // 4:.0f}"
        )
    
    with col2:
        avg_lead = filtered_df['Shipping_Lead_Time'].mean()
        st.metric(
            "Avg Lead Time",
            f"{avg_lead:.1f} days",
            f"σ: {filtered_df['Shipping_Lead_Time'].std():.1f}"
        )
    
    with col3:
        on_time = (filtered_df['Shipping_Lead_Time'] <= lead_time_threshold).sum() / len(filtered_df) * 100
        st.metric(
            "On-Time Rate",
            f"{on_time:.1f}%",
            f"({int((filtered_df['Shipping_Lead_Time'] <= lead_time_threshold).sum())} orders)"
        )
    
    with col4:
        total_sales = filtered_df['Sales'].sum()
        st.metric(
            "Total Sales",
            f"${total_sales:,.0f}",
            f"{len(filtered_df)} transactions"
        )
    
    st.markdown("---")
    
    # Lead time distribution
    st.subheader("📉 Lead Time Distribution")
    fig_dist = px.histogram(
        filtered_df,
        x='Shipping_Lead_Time',
        nbins=30,
        title='Distribution of Shipping Lead Times',
        labels={'Shipping_Lead_Time': 'Lead Time (days)'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_dist.add_vline(
        x=filtered_df['Shipping_Lead_Time'].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {filtered_df['Shipping_Lead_Time'].mean():.1f}d"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# =====================================================
# TAB 2: GEOGRAPHIC ANALYSIS
# =====================================================
with tab2:
    st.subheader("🗺️ Geographic Performance")
    
    # State-level analysis
    state_perf = filtered_df.groupby('State/Province').agg({
        'Order ID': 'count',
        'Shipping_Lead_Time': 'mean',
        'Sales': 'sum'
    }).rename(columns={
        'Order ID': 'Order_Count',
        'Shipping_Lead_Time': 'Avg_Lead_Time',
        'Sales': 'Total_Sales'
    }).reset_index().sort_values('Avg_Lead_Time', ascending=False).head(15)
    
    fig_state = px.bar(
        state_perf,
        x='State/Province',
        y='Avg_Lead_Time',
        color='Avg_Lead_Time',
        color_continuous_scale='RdYlGn_r',
        title='Top 15 States by Average Lead Time',
        labels={'Avg_Lead_Time': 'Lead Time (days)'},
        hover_data={'Order_Count': True, 'Total_Sales': ':.0f'}
    )
    st.plotly_chart(fig_state, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 State Performance Table")
    st.dataframe(state_perf, use_container_width=True)

# =====================================================
# TAB 3: SHIP MODE COMPARISON
# =====================================================
with tab3:
    st.subheader("🚚 Shipping Mode Performance")
    
    ship_mode_perf = filtered_df.groupby('Ship Mode').agg({
        'Order ID': 'count',
        'Shipping_Lead_Time': ['mean', 'min', 'max', 'std'],
        'Sales': 'sum'
    }).round(2)
    
    ship_mode_perf.columns = ['Orders', 'Avg_Lead_Time', 'Min_Time', 'Max_Time', 'Std_Dev', 'Total_Sales']
    ship_mode_perf = ship_mode_perf.reset_index().sort_values('Avg_Lead_Time')
    
    # Bar chart
    fig_modes = px.bar(
        ship_mode_perf,
        x='Ship Mode',
        y='Avg_Lead_Time',
        color='Avg_Lead_Time',
        title='Average Lead Time by Ship Mode',
        labels={'Avg_Lead_Time': 'Lead Time (days)'},
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig_modes, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Ship Mode Details")
    st.dataframe(ship_mode_perf, use_container_width=True)

# =====================================================
# TAB 4: ROUTE DETAILS
# =====================================================
with tab4:
    st.subheader("🛣️ Route Drill-Down Analysis")
    
    # Create route column
    filtered_df['Route'] = filtered_df['Division'] + ' → ' + filtered_df['State/Province']
    
    # Get route performance
    route_perf = filtered_df.groupby('Route').agg({
        'Order ID': 'count',
        'Shipping_Lead_Time': 'mean',
        'Sales': 'sum'
    }).rename(columns={
        'Order ID': 'Orders',
        'Shipping_Lead_Time': 'Avg_Lead_Time',
        'Sales': 'Total_Sales'
    }).reset_index().sort_values('Avg_Lead_Time', ascending=False)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Unique Routes", len(route_perf))
    
    with col2:
        above_threshold = len(route_perf[route_perf['Avg_Lead_Time'] > lead_time_threshold])
        st.metric("Routes Above Threshold", above_threshold)
    
    with col3:
        problematic = len(route_perf[route_perf['Avg_Lead_Time'] > 1400])
        st.metric("Critical Routes (>1400 days)", problematic)
    
    st.markdown("---")
    
    # Route table with sorting options
    sort_option = st.selectbox(
        "Sort by:",
        ["Slowest Routes", "Fastest Routes", "Most Orders", "Highest Sales"]
    )
    
    if sort_option == "Slowest Routes":
        route_perf_sorted = route_perf.sort_values('Avg_Lead_Time', ascending=False)
    elif sort_option == "Fastest Routes":
        route_perf_sorted = route_perf.sort_values('Avg_Lead_Time', ascending=True)
    elif sort_option == "Most Orders":
        route_perf_sorted = route_perf.sort_values('Orders', ascending=False)
    else:
        route_perf_sorted = route_perf.sort_values('Total_Sales', ascending=False)
    
    st.dataframe(route_perf_sorted, use_container_width=True)

# =====================================================
# TAB 5: TRENDS
# =====================================================
with tab5:
    st.subheader("📈 Trends Over Time")
    
    # Monthly trend
    filtered_df['Month'] = filtered_df['Order Date'].dt.to_period('M')
    monthly_trend = filtered_df.groupby('Month').agg({
        'Order ID': 'count',
        'Shipping_Lead_Time': 'mean'
    }).reset_index()
    monthly_trend['Month'] = monthly_trend['Month'].astype(str)
    
    fig_trend = px.line(
        monthly_trend,
        x='Month',
        y='Shipping_Lead_Time',
        markers=True,
        title='Average Lead Time Trend Over Time',
        labels={'Shipping_Lead_Time': 'Avg Lead Time (days)', 'Month': 'Month'}
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # Region comparison over time
    st.subheader("Regional Trends")
    region_monthly = filtered_df.groupby(['Month', 'Region']).agg({
        'Shipping_Lead_Time': 'mean'
    }).reset_index()
    region_monthly['Month'] = region_monthly['Month'].astype(str)
    
    fig_region_trend = px.line(
        region_monthly,
        x='Month',
        y='Shipping_Lead_Time',
        color='Region',
        title='Lead Time Trends by Region',
        markers=True,
        labels={'Shipping_Lead_Time': 'Avg Lead Time (days)'}
    )
    st.plotly_chart(fig_region_trend, use_container_width=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("🍬 Nassau Candy Distributor - Shipping Analytics Dashboard | Data-driven logistics insights")
