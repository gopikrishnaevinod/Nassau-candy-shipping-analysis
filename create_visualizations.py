import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 70)
print("NASSAU CANDY DISTRIBUTOR - CREATING VISUALIZATIONS")
print("=" * 70)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
print("\n[STEP 1] Loading data...")
df = pd.read_csv('outputs/cleaned_data.csv')
route_metrics = pd.read_csv('outputs/route_metrics.csv')
state_metrics = pd.read_csv('outputs/state_metrics.csv')
ship_mode_metrics = pd.read_csv('outputs/ship_mode_metrics.csv')
print(f"✓ Data loaded!")

# =====================================================
# VISUALIZATION 1: Lead Time Distribution
# =====================================================
print("\n[VISUALIZATION 1] Creating lead time distribution...")
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(df['Shipping_Lead_Time'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
ax.axvline(df['Shipping_Lead_Time'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Shipping_Lead_Time"].mean():.1f} days')
ax.axvline(df['Shipping_Lead_Time'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Shipping_Lead_Time"].median():.1f} days')
ax.set_xlabel('Shipping Lead Time (days)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Shipping Lead Times', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/visualizations/01_lead_time_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_lead_time_distribution.png")
plt.close()

# =====================================================
# VISUALIZATION 2: Top 15 Slowest Routes
# =====================================================
print("\n[VISUALIZATION 2] Creating slowest routes chart...")
fig, ax = plt.subplots(figsize=(12, 8))
top_slow = route_metrics.nlargest(15, 'Avg_Lead_Time')
colors = ['red' if x > df['Shipping_Lead_Time'].mean() else 'orange' for x in top_slow['Avg_Lead_Time']]
ax.barh(range(len(top_slow)), top_slow['Avg_Lead_Time'], color=colors, alpha=0.7, edgecolor='black')
ax.set_yticks(range(len(top_slow)))
ax.set_yticklabels(top_slow['Route'], fontsize=10)
ax.set_xlabel('Average Lead Time (days)', fontsize=12)
ax.set_title('Top 15 Slowest Routes (Bottlenecks)', fontsize=14, fontweight='bold')
ax.axvline(df['Shipping_Lead_Time'].mean(), color='green', linestyle='--', linewidth=2, label='Overall Average')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/visualizations/02_slowest_routes.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_slowest_routes.png")
plt.close()

# =====================================================
# VISUALIZATION 3: Top 15 Fastest Routes
# =====================================================
print("\n[VISUALIZATION 3] Creating fastest routes chart...")
fig, ax = plt.subplots(figsize=(12, 8))
top_fast = route_metrics.nsmallest(15, 'Avg_Lead_Time')
colors = ['green' if x < df['Shipping_Lead_Time'].mean() else 'yellow' for x in top_fast['Avg_Lead_Time']]
ax.barh(range(len(top_fast)), top_fast['Avg_Lead_Time'], color=colors, alpha=0.7, edgecolor='black')
ax.set_yticks(range(len(top_fast)))
ax.set_yticklabels(top_fast['Route'], fontsize=10)
ax.set_xlabel('Average Lead Time (days)', fontsize=12)
ax.set_title('Top 15 Fastest Routes (Best Performance)', fontsize=14, fontweight='bold')
ax.axvline(df['Shipping_Lead_Time'].mean(), color='red', linestyle='--', linewidth=2, label='Overall Average')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/visualizations/03_fastest_routes.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_fastest_routes.png")
plt.close()

# =====================================================
# VISUALIZATION 4: Top 10 Slowest States
# =====================================================
print("\n[VISUALIZATION 4] Creating state performance chart...")
fig, ax = plt.subplots(figsize=(12, 6))
top_slow_states = state_metrics.head(10)
colors = ['darkred' if x > 1500 else 'red' if x > 1400 else 'orange' for x in top_slow_states['Avg_Lead_Time']]
bars = ax.bar(range(len(top_slow_states)), top_slow_states['Avg_Lead_Time'], color=colors, alpha=0.7, edgecolor='black')
ax.set_xticks(range(len(top_slow_states)))
ax.set_xticklabels(top_slow_states.index, rotation=45, ha='right', fontsize=10)
ax.set_ylabel('Average Lead Time (days)', fontsize=12)
ax.set_title('Top 10 States with Highest Lead Times (Geographic Bottlenecks)', fontsize=14, fontweight='bold')
ax.axhline(df['Shipping_Lead_Time'].mean(), color='green', linestyle='--', linewidth=2, label='Overall Average')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/visualizations/04_state_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_state_performance.png")
plt.close()

# =====================================================
# VISUALIZATION 5: Ship Mode Comparison
# =====================================================
print("\n[VISUALIZATION 5] Creating ship mode comparison...")
fig, ax = plt.subplots(figsize=(10, 6))
ship_data = ship_mode_metrics.sort_values('Avg_Lead_Time')
colors = ['green', 'yellow', 'orange', 'red']
bars = ax.bar(range(len(ship_data)), ship_data['Avg_Lead_Time'], color=colors, alpha=0.7, edgecolor='black')
ax.set_xticks(range(len(ship_data)))
ax.set_xticklabels(ship_data['Ship Mode'], fontsize=11)
ax.set_ylabel('Average Lead Time (days)', fontsize=12)
ax.set_title('Shipping Mode Performance Comparison', fontsize=14, fontweight='bold')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, ship_data['Avg_Lead_Time'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{val:.0f}', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('outputs/visualizations/05_ship_mode_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 05_ship_mode_comparison.png")
plt.close()

# =====================================================
# VISUALIZATION 6: Route Volume vs Lead Time
# =====================================================
print("\n[VISUALIZATION 6] Creating volume vs lead time scatter...")
fig, ax = plt.subplots(figsize=(12, 6))
scatter = ax.scatter(route_metrics['Total_Shipments'], 
                     route_metrics['Avg_Lead_Time'],
                     s=100,
                     c=route_metrics['Avg_Lead_Time'],
                     cmap='RdYlGn_r',
                     alpha=0.6,
                     edgecolors='black',
                     linewidth=0.5)

ax.set_xlabel('Total Shipments per Route', fontsize=12)
ax.set_ylabel('Average Lead Time (days)', fontsize=12)
ax.set_title('Route Volume vs Performance (Size = Volume)', fontsize=14, fontweight='bold')

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Lead Time (days)', fontsize=10)

plt.tight_layout()
plt.savefig('outputs/visualizations/06_volume_vs_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 06_volume_vs_performance.png")
plt.close()

# =====================================================
# VISUALIZATION 7: Delay Frequency by Route
# =====================================================
print("\n[VISUALIZATION 7] Creating delay frequency chart...")
fig, ax = plt.subplots(figsize=(12, 8))
high_delay = route_metrics.nlargest(15, 'Delay_Frequency_%')
colors = ['darkred' if x > 90 else 'red' if x > 70 else 'orange' for x in high_delay['Delay_Frequency_%']]
ax.barh(range(len(high_delay)), high_delay['Delay_Frequency_%'], color=colors, alpha=0.7, edgecolor='black')
ax.set_yticks(range(len(high_delay)))
ax.set_yticklabels(high_delay['Route'], fontsize=10)
ax.set_xlabel('Delay Frequency (%)', fontsize=12)
ax.set_title('Routes with Highest Delay Rates (>7 days threshold)', fontsize=14, fontweight='bold')
ax.set_xlim(0, 105)
plt.tight_layout()
plt.savefig('outputs/visualizations/07_delay_frequency.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 07_delay_frequency.png")
plt.close()

# =====================================================
# SUMMARY
# =====================================================
print("\n" + "=" * 70)
print("✓ VISUALIZATIONS COMPLETE!")
print("=" * 70)

print("\n📊 CHARTS CREATED:")
print("  1. ✓ 01_lead_time_distribution.png")
print("  2. ✓ 02_slowest_routes.png")
print("  3. ✓ 03_fastest_routes.png")
print("  4. ✓ 04_state_performance.png")
print("  5. ✓ 05_ship_mode_comparison.png")
print("  6. ✓ 06_volume_vs_performance.png")
print("  7. ✓ 07_delay_frequency.png")

print("\n📁 Location: outputs/visualizations/")
print("\n✅ Ready for:")
print("  • Research paper (add charts here)")
print("  • Streamlit dashboard (use these charts)")
print("  • Executive summary (include key charts)")

print("\n" + "=" * 70)
