import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
worksheet2 = pd.read_csv("worksheet2.csv")
worksheet3 = pd.read_csv("worksheet3.csv")

# Plotting
plt.figure(figsize=(10, 6))

# Plot original data for men
plt.scatter(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', label='Men (Original)', marker='o')
plt.plot(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', linestyle='-', alpha=0.5)

# Plot original data for women
plt.scatter(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', label='Women (Original)', marker='o')
plt.plot(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', linestyle='-', alpha=0.5)


bars = plt.bar(worksheet3['year'], worksheet3['women-men_hours'], color='skyblue')

# Add value labels to each bar
for bar, value in zip(bars, worksheet3['women-men_hours']):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha='center', va='bottom')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Difference in Hours (Women - Men)')
plt.title('Difference in Hours of Housework Between Men and Women')
plt.legend()

# Display plot
plt.grid(True)
plt.show()
