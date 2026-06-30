"""
Nassau Candy Distributor - Project Starter Script
Step-by-step beginner guide to get started with data analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 60)
print("NASSAU CANDY DISTRIBUTOR - PROJECT STARTER")
print("=" * 60)

# =====================================================
# STEP 1: LOAD YOUR DATA
# =====================================================
print("\n[STEP 1] Loading dataset...")
try:
    # Change this path to your actual CSV file location
    df = pd.read_csv('data/orders_shipments.csv')
    print(f"✓ Dataset loaded successfully!")
    print(f"  Total rows: {len(df):,}")
    print(f"  Total columns: {len(df.columns)}")
except FileNotFoundError:
    print("❌ Error: Could not find CSV file")
    print("   Make sure your file is at: data/orders_shipments.csv")
    exit()

# =====================================================
# STEP 2: EXPLORE YOUR DATA
# =====================================================
print("\n[STEP 2] Exploring data structure...")

print("\nColumn Names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\nData Types:")
print(df.dtypes)

print("\nFirst 3 rows of data:")
print(df.head(3))

# =====================================================
# STEP 3: CHECK FOR DATA QUALITY ISSUES
# =====================================================
print("\n[STEP 3] Data Quality Check...")

print("\nMissing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("  ✓ No missing values found!")
else:
    print("  ❌ Missing values detected:")
    print(missing[missing > 0])

print("\nDataset Info:")
print(df.info())

# =====================================================
# STEP 4: DATA CLEANING
# =====================================================
print("\n[STEP 4] Cleaning data...")

# Make a copy to work with
df_clean = df.copy()

# Convert date columns to datetime
print("  - Converting date columns...")
df_clean['Order Date'] = pd.to_datetime(df_clean['Order Date'], errors='coerce')
df_clean['Ship Date'] = pd.to_datetime(df_clean['Ship Date'], errors='coerce')

# Calculate shipping lead time
print("  - Calculating shipping lead time...")
df_clean['Shipping_Lead_Time'] = (
    df_clean['Ship Date'] - df_clean['Order Date']
).dt.days

# Remove rows with missing dates
print("  - Removing rows with invalid dates...")
df_clean = df_clean.dropna(subset=['Order Date', 'Ship Date'])

# Remove negative lead times (data entry errors)
initial_count = len(df_clean)
df_clean = df_clean[df_clean['Shipping_Lead_Time'] >= 0]
removed = initial_count - len(df_clean)
if removed > 0:
    print(f"  - Removed {removed} rows with negative lead times")

# Standardize text fields
print("  - Standardizing text fields...")
df_clean['State/Province'] = df_clean['State/Province'].str.strip().str.upper()
df_clean['Region'] = df_clean['Region'].str.strip()
df_clean['Ship Mode'] = df_clean['Ship Mode'].str.strip()

# Remove duplicates
duplicates = df_clean.duplicated().sum()
if duplicates > 0:
    print(f"  - Removing {duplicates} duplicate rows")
    df_clean = df_clean.drop_duplicates()

print(f"\n✓ Data cleaning complete!")
print(f"  Original rows: {len(df):,}")
print(f"  Cleaned rows: {len(df_clean):,}")

# =====================================================
# STEP 5: BASIC STATISTICS
# =====================================================
print("\n[STEP 5] Basic Statistics...")

print("\nShipping Lead Time Summary:")
print(f"  Average: {df_clean['Shipping_Lead_Time'].mean():.2f} days")
print(f"  Median: {df_clean['Shipping_Lead_Time'].median():.2f} days")
print(f"  Minimum: {df_clean['Shipping_Lead_Time'].min():.0f} days")
print(f"  Maximum: {df_clean['Shipping_Lead_Time'].max():.0f} days")
print(f"  Std Dev: {df_clean['Shipping_Lead_Time'].std():.2f} days")

print("\nAvailable Regions:")
print(f"  {df_clean['Region'].unique().tolist()}")

print("\nAvailable Ship Modes:")
print(f"  {df_clean['Ship Mode'].unique().tolist()}")

print("\nDate Range:")
print(f"  From: {df_clean['Order Date'].min().date()}")
print(f"  To:   {df_clean['Order Date'].max().date()}")

# =====================================================
# STEP 6: SAMPLE ANALYSIS
# =====================================================
print("\n[STEP 6] Sample Analysis...")

print("\nAverage Lead Time by Region:")
region_analysis = df_clean.groupby('Region')['Shipping_Lead_Time'].agg([
    ('Avg', 'mean'),
    ('Count', 'count'),
    ('Min', 'min'),
    ('Max', 'max')
]).round(2).sort_values('Avg', ascending=False)
print(region_analysis)

print("\nAverage Lead Time by Ship Mode:")
ship_mode_analysis = df_clean.groupby('Ship Mode')['Shipping_Lead_Time'].agg([
    ('Avg', 'mean'),
    ('Count', 'count')
]).round(2).sort_values('Avg')
print(ship_mode_analysis)

# =====================================================
# STEP 7: SAVE CLEANED DATA
# =====================================================
print("\n[STEP 7] Saving cleaned data...")
try:
    df_clean.to_csv('outputs/cleaned_data.csv', index=False)
    print("✓ Cleaned data saved to: outputs/cleaned_data.csv")
except Exception as e:
    print(f"❌ Error saving file: {e}")

# =====================================================
# STEP 8: NEXT STEPS
# =====================================================
print("\n" + "=" * 60)
print("✓ SETUP COMPLETE!")
print("=" * 60)

print("\nNext Steps:")
print("1. Review the cleaned data in outputs/cleaned_data.csv")
print("2. Run the route analysis script")
print("3. Create visualizations")
print("4. Build the Streamlit dashboard")
print("\nFor detailed instructions, see PROJECT_ROADMAP.md")
print("=" * 60)

# Optional: Display sample of clean data
print("\nSample of cleaned data:")
print(df_clean[['Order ID', 'Order Date', 'Ship Date', 'Shipping_Lead_Time', 
                'Region', 'State/Province', 'Ship Mode']].head(10))
