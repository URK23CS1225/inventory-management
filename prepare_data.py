import pandas as pd
import numpy as np
import gzip
import json
from datetime import datetime

# Load retail data
df = pd.read_csv('retail_store_inventory.csv')

# Calculate daily demand per product from historical sales
demand_data = df.groupby('Product ID').agg({
    'Units Sold': 'mean'
}).reset_index()
demand_data.columns = ['product_id', 'daily_demand']
demand_data['daily_demand'] = demand_data['daily_demand'].round(2)

# Get product info and simulate inventory parameters
product_info = df.groupby('Product ID').agg({
    'Category': 'first',
    'Inventory Level': 'last',
    'Units Sold': 'mean'
}).reset_index()

# Create inventory dataset with simulated parameters
inventory_data = pd.DataFrame({
    'product_id': product_info['Product ID'],
    'product_name': product_info['Category'] + '_' + product_info['Product ID'],
    'current_stock': product_info['Inventory Level'],
    'max_capacity': (product_info['Inventory Level'] * np.random.uniform(1.5, 2.5, len(product_info))).astype(int),
    'lead_time_days': np.random.randint(3, 15, len(product_info))
})

# Save compressed inventory data
inventory_data.to_csv('inventory.csv.gz', index=False, compression='gzip')

# Save demand data
demand_data.to_csv('demand.csv', index=False)

print(f"✓ Processed {len(inventory_data)} products")
print(f"✓ Created inventory.csv.gz")
print(f"✓ Created demand.csv")
