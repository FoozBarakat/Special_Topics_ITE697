import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read the CSV file
worksheet2 = pd.read_csv("worksheet2.csv")

# Plotting
plt.figure(figsize=(10, 6))

# Plot original data for men
plt.scatter(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', label='Men (Original)', marker='o')
plt.plot(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', linestyle='-', alpha=0.5)

# Plot original data for women
plt.scatter(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', label='Women (Original)', marker='o')
plt.plot(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', linestyle='-', alpha=0.5)


# Sort the dataframe by year
worksheet2.sort_values('year', inplace=True)

# Add missing years
missing_years = [1970, 1980, 1990]
for year in missing_years:
    worksheet2.loc[len(worksheet2)] = [year, np.nan, np.nan]

# Sort the dataframe again
worksheet2.sort_values('year', inplace=True)

# Interpolate missing values
worksheet2['men_hours_housework_week'] = worksheet2['men_hours_housework_week'].interpolate(method='linear')
worksheet2['women_hours_housework_week'] = worksheet2['women_hours_housework_week'].interpolate(method='linear')

# Plot interpolated data for men
plt.scatter(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', label='Men (Interpolated)', marker='x')
plt.plot(worksheet2['year'], worksheet2['men_hours_housework_week'], color='blue', linestyle='--', alpha=0.5)

# Plot interpolated data for women
plt.scatter(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', label='Women (Interpolated)', marker='x')
plt.plot(worksheet2['year'], worksheet2['women_hours_housework_week'], color='red', linestyle='--', alpha=0.5)


# Get the data for the previous five periods
X = worksheet2['year'][-5:].values.reshape(-1, 1)
y_men = worksheet2['men_hours_housework_week'][-5:].values
y_women = worksheet2['women_hours_housework_week'][-5:].values

# Fit a linear regression model for men
model_men = LinearRegression()
model_men.fit(X, y_men)

# Fit a linear regression model for women
model_women = LinearRegression()
model_women.fit(X, y_women)

# Extrapolate the values for the year 2020 for men and women
year_2020 = 2020
X_2020 = np.array([[year_2020]])
extrapolated_value_men = model_men.predict(X_2020)
extrapolated_value_women = model_women.predict(X_2020)

print('Extrapolated Value Men: ', extrapolated_value_men)
print('Extrapolated Value Women: ', extrapolated_value_women)

# Plot extrapolated line for men
plt.plot([X[0][0], year_2020], [model_men.predict([[X[0][0]]])[0], extrapolated_value_men[0]], color='blue', linestyle=':', label='Men (Extrapolated)')


# Plot extrapolated line for women
plt.plot([X[0][0], year_2020], [model_women.predict([[X[0][0]]])[0], extrapolated_value_women[0]], color='red', linestyle=':', label='Women (Extrapolated)')

# Adding labels and title
plt.xlabel('Year')
plt.ylabel('Hours')
plt.title('Men and Women Housework Hours')
plt.legend()

# Display plot
plt.grid(True)
plt.show()



