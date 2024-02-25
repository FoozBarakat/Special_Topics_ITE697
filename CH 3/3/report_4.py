import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load your data (assuming your data is in a CSV file)
df = pd.read_csv('purchase_orders.csv')

# Filter rows where 'SO#' is not NaN
orders_with_so = df[df['SO#'].notna()]

# Filter rows where 'SO#' is NaN
orders_without_so = df[df['SO#'].isna()]

# Create a figure with 1 row and 3 columns
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Define different color palettes for the pie charts
color_palette1 = plt.cm.Set3(np.linspace(0, 1, len(orders_without_so['End-User'].unique())))

# Plot 1: Pie chart for count of purchase orders with and without SO#
order_count = [len(orders_with_so), len(orders_without_so)]
# Calculate the total vendor price for booked and not booked purchase orders
total_vendor_price_booked = orders_with_so['Vendor Price'].str.replace(',', '').astype(float).sum()
total_vendor_price_not_booked = orders_without_so['Vendor Price'].str.replace(',', '').astype(float).sum()
# Create legend labels including total vendor price
legend_labels = [
    'Booked ({0} POs, ${1:,.0f})'.format(len(orders_with_so), total_vendor_price_booked),
    'Not Booked ({0} POs, ${1:,.0f})'.format(len(orders_without_so), total_vendor_price_not_booked)
]
axs[0].pie(order_count, autopct='%1.1f%%', startangle=140, counterclock=False, colors=color_palette1)
axs[0].set_title('Booked VS. Not Booked')
axs[0].legend(legend_labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize='small', title='End-User')

# Plot 2: Pie chart for the count of purchase orders for each end-user without SO#
end_users_without_so_sorted = orders_without_so['End-User'].value_counts().sort_values(ascending=False)
color_palette2 = plt.cm.Pastel1(np.linspace(0, 1, len(end_users_without_so_sorted)))  # Define color palette
axs[1].pie(end_users_without_so_sorted, autopct='%1.1f%%', startangle=140, counterclock=False, colors=color_palette2)
axs[1].set_title('The POs that will be moved to FY24')
# Modify the legend for this plot
legend_labels_po = [f"{end_user} ({count} POs)" for end_user, count in end_users_without_so_sorted.items()]
axs[1].legend(legend_labels_po, loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize='small', title='End-User')

# Plot 3: Pie chart for the total vendor price for each end-user without SO#
# Remove commas from 'Vendor Price' and convert to float
orders_without_so['Vendor Price'] = orders_without_so['Vendor Price'].str.replace(',', '').astype(float)
total_prices_without_so = orders_without_so.groupby('End-User')['Vendor Price'].sum().sort_values(ascending=False)
color_palette3 = plt.cm.Pastel2(np.linspace(0, 1, len(total_prices_without_so)))  # Define color palette

# Apply functionality from provided code to this pie chart
ax = axs[2]
vendor_prices = total_prices_without_so
vendor_prices = vendor_prices.sort_values(ascending=False)
total_vendor_price = vendor_prices.sum()
percentages = (vendor_prices / total_vendor_price) * 100

# Use the "Set3" color map for the pie chart
colors = plt.cm.Set3(range(len(vendor_prices)))

# Create the pie chart with colors and explode the slice with the smallest percentage
explode = [0.1 if percent < 5 else 0 for percent in percentages]
wedges, texts, autotexts = ax.pie(vendor_prices, labels=None, autopct='', startangle=140, counterclock=False, colors=colors, textprops={'fontsize': 10}, pctdistance=0.85, explode=explode)

# Add the total "Vendor Price" to the title
title = f'POs Values that will be moved to FY24\nTotal: ${total_vendor_price:,.0f}'  # Include commas for thousands separator
ax.set_title(title)

# Create custom labels with percentages inside the chart segments for slices with percentage > 1%
for i, price in enumerate(vendor_prices):
    if percentages.iloc[i] > 1.8:
        angle = wedges[i].theta2 - (wedges[i].theta2 - wedges[i].theta1) / 2
        radius = 0.4  # Adjust the radius for label placement
        x = radius * np.cos(np.deg2rad(angle))
        y = radius * np.sin(np.deg2rad(angle))
        ax.text(x, y, f'{percentages.iloc[i]:.1f}%', ha='center', va='center', fontsize=10)

# Create a legend under the pie chart
legend_labels_price = [f"{end_user} (${price:,.0f})" for end_user, price in vendor_prices.items()]
legend = axs[2].legend(legend_labels_price, title="End-User", loc='upper center', bbox_to_anchor=(0.5, -0.3), fontsize='small')

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
