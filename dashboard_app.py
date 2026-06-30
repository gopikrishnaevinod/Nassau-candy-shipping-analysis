@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/gopimrishnaevinod/nassau-candy-shipping-analysis/main/cleaned_data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

@st.cache_data
def load_route_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopimrishnaevinod/nassau-candy-shipping-analysis/main/route_metrics.csv')

@st.cache_data
def load_state_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopimrishnaevinod/nassau-candy-shipping-analysis/main/state_metrics.csv')

@st.cache_data
def load_ship_mode_metrics():
    return pd.read_csv('https://raw.githubusercontent.com/gopimrishnaevinod/nassau-candy-shipping-analysis/main/ship_mode_metrics.csv')
