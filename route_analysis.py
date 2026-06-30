import pandas as pd

print("=" * 70)
print("NASSAU CANDY DISTRIBUTOR - ROUTE ANALYSIS")
print("=" * 70)

# Load cleaned data
print("\n[STEP 1] Loading cleaned dataset...")
df = pd.read_csv('outputs/cleaned_data.csv')
print(f"✓ Loaded {len(df):,} rows")

# Define routes
print("\n[STEP 2] Defining routes...")
df['Route'] = df['Division'] + ' → ' + df['State/Province']
print(f"✓ Total unique routes: {df['Route'].nunique()}")

# Calculate route metrics
print("\n[STEP 3] Calculating route metrics...")
route_metrics = df.groupby('Route').agg({
    'Order ID': 'count',
    'Shipping_Lead_Time': ['mean', 'std', 'min', 'max'],
    'Sales': 'sum'
}).round(2)

route_metrics.columns = ['Total_Shipments', 'Avg_Lead_Time', 'Std_Dev', 'Min_Time', 'Max_Time', 'Total_Sales']

# Add efficiency score
route_metrics['Efficiency_Score'] = (
    (route_metrics['Avg_Lead_Time'] / route_metrics['Avg_Lead_Time'].max()) * 100
).round(2)

# Calculate delay frequency (threshold = 7 days)
delay_threshold = 7
route_delay_freq = df.groupby('Route').apply(
    lambda x: (x['Shipping_Lead_Time'] > delay_threshold).sum() / len(x) * 100
).round(2)
route_metrics['Delay_Frequency_%'] = route_delay_freq

# Sort by lead time
route_metrics = route_metrics.sort_values('Avg_Lead_Time')

print("✓ Metrics calculated!")

# Save to CSV
route_metrics_export = route_metrics.reset_index()
route_metrics_export.to_csv('outputs/route_metrics.csv', index=False)
print(f"✓ Saved: outputs/route_metrics.csv")

# Display TOP 10 FASTEST ROUTES
print("\n" + "=" * 70)
print("TOP 10 FASTEST ROUTES")
print("=" * 70 + "\n")
for i, (route, row) in enumerate(route_metrics.head(10).iterrows(), 1):
    print(f"{i}. {route}")
    print(f"   Avg Lead Time: {row['Avg_Lead_Time']:.2f} days | Orders: {row['Total_Shipments']:.0f} | Delays: {row['Delay_Frequency_%']:.1f}%\n")

# Display BOTTOM 10 SLOWEST ROUTES
print("\n" + "=" * 70)
print("BOTTOM 10 SLOWEST ROUTES")
print("=" * 70 + "\n")
for i, (route, row) in enumerate(route_metrics.tail(10).iterrows(), 1):
    print(f"{i}. {route}")
    print(f"   Avg Lead Time: {row['Avg_Lead_Time']:.2f} days | Orders: {row['Total_Shipments']:.0f} | Delays: {row['Delay_Frequency_%']:.1f}%\n")

# State analysis
print("\n" + "=" * 70)
print("STATE PERFORMANCE ANALYSIS")
print("=" * 70 + "\n")
state_metrics = df.groupby('State/Province').agg({
    'Order ID': 'count',
    'Shipping_Lead_Time': 'mean',
    'Sales': 'sum'
}).round(2).sort_values('Shipping_Lead_Time', ascending=False)

state_metrics.columns = ['Shipment_Count', 'Avg_Lead_Time', 'Total_Sales']
state_metrics_export = state_metrics.reset_index()
state_metrics_export.to_csv('outputs/state_metrics.csv', index=False)
print("✓ Saved: outputs/state_metrics.csv")

print("\nTop 10 Slowest States:")
for i, (state, row) in enumerate(state_metrics.head(10).iterrows(), 1):
    print(f"{i}. {state}: {row['Avg_Lead_Time']:.2f} days | Orders: {row['Shipment_Count']:.0f}")

# Ship mode analysis
print("\n" + "=" * 70)
print("SHIP MODE COMPARISON")
print("=" * 70 + "\n")
ship_mode_metrics = df.groupby('Ship Mode').agg({
    'Order ID': 'count',
    'Shipping_Lead_Time': ['mean', 'min', 'max'],
    'Sales': 'sum'
}).round(2)

ship_mode_metrics.columns = ['Total_Orders', 'Avg_Lead_Time', 'Min_Time', 'Max_Time', 'Total_Sales']
ship_mode_metrics_export = ship_mode_metrics.reset_index()
ship_mode_metrics_export.to_csv('outputs/ship_mode_metrics.csv', index=False)

print("Ship Mode Performance:")
for mode, row in ship_mode_metrics.iterrows():
    print(f"{mode}: {row['Avg_Lead_Time']:.2f} days avg | {row['Total_Orders']:.0f} orders")

print("\n" + "=" * 70)
print("✓ ANALYSIS COMPLETE!")
print("=" * 70)
print("\nFiles created:")
print("  ✓ outputs/route_metrics.csv")
print("  ✓ outputs/state_metrics.csv")
print("  ✓ outputs/ship_mode_metrics.csv")