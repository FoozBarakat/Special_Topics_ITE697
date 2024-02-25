import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file (replace 'purchase_orders.csv' with your file path)
df = pd.read_csv('purchase_orders.csv')

# Group the data by End-User and calculate the PO counts
po_counts = df['End-User'].value_counts()

# Calculate the total number of POs
total_pos = po_counts.sum()

# Create a pie chart
fig, ax = plt.subplots(figsize=(10, 6))

# Generate a color map for the slices
colors = plt.cm.Set3(range(len(po_counts)))

# Create the pie chart with colors
wedges, texts, autotexts = ax.pie(po_counts, labels=None, autopct='%1.1f%%', startangle=140, counterclock=False, colors=colors, textprops={'fontsize': 12})

# Add the total number of POs to the title
title = f'Purchase Orders for FCV in FY23\nTotal POs: {total_pos}'
ax.set_title(title, fontsize=16)

# Add the number of POs as text labels inside the pie chart
for i, count in enumerate(po_counts):
    ax.text(0.5 * plt.gca().transAxes.transform((1, 1))[0], 0.5 * plt.gca().transAxes.transform((1, 1))[1], f"{count} POs", ha='center', va='center', fontsize=10)

# Create a legend on the left side with End-User names, colors, and the total number of POs
legend_labels = [f"{po_counts.index[i]} ({po_counts[i]} POs)" for i in range(len(po_counts))]
legend_labels.append(f"Total POs: {total_pos}")
ax.legend(legend_labels, title="End-Users", loc="center left", bbox_to_anchor=(-0.15, 0.5))

# Show the chart
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.show()
