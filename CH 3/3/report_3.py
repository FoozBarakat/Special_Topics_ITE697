import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import locale

# Set the locale to format numbers with commas
locale.setlocale(locale.LC_ALL, '')

# Read data from the "purchase_orders.csv" file
df = pd.read_csv("purchase_orders.csv")

# Remove commas and convert the Vendor Price column to numeric
df['Vendor Price'] = df['Vendor Price'].str.replace(',', '').astype(float)

# Create a dictionary to map quarters
quarter_mapping = {
    'P 01': 'Q1',
    'P 02': 'Q1',
    'P 03': 'Q1',
    'P 04': 'Q2',
    'P 05': 'Q2',
    'P 06': 'Q2',
    'P 07': 'Q3',
    'P 08': 'Q3',
    'P 09': 'Q3',
    'P 10': 'Q4',
    'P 11': 'Q4',
    'P 12': 'Q4',
}

# Add a new column for quarters
df['Quarter'] = df['PO Booking Period'].map(quarter_mapping)

# Ensure that 'PO Booking Period' is treated as strings
df['PO Booking Period'] = df['PO Booking Period'].astype(str)

# Filter out the 'nan' value from unique_periods
unique_periods = df['PO Booking Period'].unique()
unique_periods = unique_periods[unique_periods != 'nan']

# Rearrange unique_periods so that P 01 is first
unique_periods = sorted(unique_periods, key=lambda x: (int(x.split()[1]) if len(x.split()) > 1 else 0))
unique_periods.remove('P 01')
unique_periods = ['P 01'] + unique_periods

# Define colors for the quarters
colors = ['skyblue', 'lightcoral', 'lightgreen', 'lightsalmon']

# Create a bar chart
plt.figure(figsize=(12, 6))

quarters = ['Q1', 'Q2', 'Q3', 'Q4']

# Initialize a dictionary to store the sum of vendor prices for each quarter
quarter_sums = {}

# Calculate the number of unique periods for positioning
num_periods = len(unique_periods)
bar_width = 0.8  # Increase the width of each bar for better alignment

# Calculate the positions for each group of bars
x_positions = np.arange(num_periods)  # x-axis positions for each period

for i, quarter in enumerate(quarters):
    total_vendor_prices = df[df['Quarter'] == quarter].groupby('PO Booking Period')['Vendor Price'].sum().reindex(unique_periods, fill_value=0).tolist()

    # Calculate the x-axis positions for each bar within the group, centered
    x = x_positions + i * bar_width

    # Create bars for each period within the quarter
    plt.bar(x, total_vendor_prices, width=bar_width, color=colors[i], alpha=0.7, label=f'Quarter {quarter}')

    # Calculate and store the sum of vendor prices for the quarter
    quarter_sum = sum(total_vendor_prices)
    quarter_sums[quarter] = quarter_sum

    # Add text labels above the columns with the sum of vendor prices for each period
    for xpos, ypos in zip(x, total_vendor_prices):
        if ypos != 0:  # Check if the value is not zero to avoid adding labels for empty columns
            formatted_ypos = locale.format_string('%d', int(ypos), grouping=True)  # Format with commas
            plt.text(xpos, ypos + 100, formatted_ypos, ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Calculate the total for all quarters
total_all_quarters = sum(quarter_sums.values())

# Add the total for all quarters to the title with number formatting
formatted_total_all_quarters = locale.format_string('%d', int(total_all_quarters), grouping=True)  # Format with commas
plt.title(f'Vendor Price by Period and Quarter\nTotal for All Quarters: ${formatted_total_all_quarters}')

# Remove x-axis labels
plt.xticks([])

plt.xlabel('Quarter')
plt.ylabel('Vendor Price')

# Add the quarter sums to the legend with number formatting
legend_labels = [f'Quarter {quarter} (Sum: ${locale.format_string("%d", int(quarter_sums[quarter]), grouping=True)})' for quarter in quarters]
plt.legend(labels=legend_labels)

plt.show()
