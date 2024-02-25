import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file (replace 'purchase_orders.csv' with your file path)
df = pd.read_csv('purchase_orders.csv')

# Remove commas from "Vendor Price" column and convert it to integer
df['Vendor Price'] = df['Vendor Price'].str.replace(',', '', regex=True).astype(int)

# Group the data by End-User and calculate the total "Vendor Price"
vendor_prices = df.groupby('End-User')['Vendor Price'].sum()

# Sort the End-Users by their total "Vendor Price" in descending order
vendor_prices = vendor_prices.sort_values(ascending=False)

# Calculate the total "Vendor Price" for all End-Users
total_vendor_price = vendor_prices.sum()

# Calculate the percentage of "Vendor Price" for each End-User
percentages = (vendor_prices / total_vendor_price) * 100

# Create a pie chart
fig, ax = plt.subplots(figsize=(10, 6))

# Use the "Set3" color map for the pie chart
colors = plt.cm.Set3(range(len(vendor_prices)))

# Create the pie chart with colors and explode the slice with the smallest percentage
explode = [0.1 if percent < 5 else 0 for percent in percentages]
wedges, texts, autotexts = ax.pie(vendor_prices, labels=None, autopct=lambda p: f'{p:.1f}%' if p > 1 else '', startangle=140, counterclock=False, colors=colors, textprops={'fontsize': 10}, pctdistance=0.85, explode=explode)

# Add the total "Vendor Price" to the title
title = f'Purchase Orders Values by End-User\nTotal "Vendor Price": ${total_vendor_price:,}'  # Include commas for thousands separator
ax.set_title(title, fontsize=16)

# Create custom labels with values outside the chart for slices with percentage > 1%
for i, price in enumerate(vendor_prices):
    if percentages.iloc[i] > 1:
        angle = wedges[i].theta2 - (wedges[i].theta2 - wedges[i].theta1) / 2
        x = 1.2 * plt.gca().transAxes.transform((0.5, 0.5))[0]
        y = 1.2 * plt.gca().transAxes.transform((0.5, 0.5))[1]
        ax.text(x, y, f"${price:,}", ha='center', va='center', fontsize=10, rotation=angle)

# Create a legend on the left side with End-User names, colors, and percentage for slices with percentage <= 1%
legend_labels = []
for i, (index, price) in enumerate(vendor_prices.items()):
        legend_labels.append(f"{index} (${price:,.0f})")
ax.legend(legend_labels, title="End-Users", loc="center left", bbox_to_anchor=(-0.15, 0.5))

# Show the chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.show()
