import pandas as pd
import matplotlib.pyplot as plt

## => Part 1: Learn how to Use Data as Information

# Read the CSV file
worksheet1 = pd.read_csv("worksheet1.csv")

# Read each column
median_age_males = worksheet1['median_age_males']
median_age_females = worksheet1['median_age_females']
year = worksheet1['year']

# Calculate the minimum and maximum median ages for males and females
male_min_age = median_age_males.min()
male_max_age = median_age_males.max()
female_min_age = median_age_females.min()
female_max_age = median_age_females.max()

# Create a tuple containing the minimum and maximum median ages for males and females
male_range = (male_min_age, male_max_age)
female_range = (female_min_age, female_max_age)

# Print the results
print("Male median age:")
print(f"{male_range[0]} to {male_range[1]}")
print("Female median age:")
print(f"{female_range[0]} to {female_range[1]}")

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(year, median_age_males, color='blue', label='Male Median Age', marker='o')
plt.plot(year, median_age_males, color='blue', linestyle='-', alpha=0.5)
plt.scatter(year, median_age_females, color='red', label='Female Median Age', marker='o')
plt.plot(year, median_age_females, color='red', linestyle='-', alpha=0.5)

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Median Age')
plt.title('Median Age of Marriage Over Time')
plt.legend(loc = 'upper right')

# Display plot
plt.grid(True)
plt.show()



