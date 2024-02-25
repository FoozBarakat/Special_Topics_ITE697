import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium 

## => Part 2: Load the Data
SF = pd.read_csv("Map-Crime_Incidents-Previous_Three_Months.csv")

# a) By typing the name of the data frame variable into a cell, you can visualize the top and bottom rows in a structured way.

print(SF.head(10))  # Displays the top 10 rows
print(SF.tail(10))  # Displays the bottom 10 rows

# b) Use the function columns to view the name of the variables in the DataFrame.
print(SF.columns)  # Displays the column names

# c) Use the function len to determine the number of rows in the dataset.
print(len(SF))  # Displays the number of rows in the DataFrame


## => Part 3: Prepare the Data

# Extract the month and day from the Date field
# Use lambda functions to extract the month and day digits from the 'Date' variable
# Apply these lambda functions to create new 'Month' and 'Day' columns in the DataFrame
SF['Month'] = SF['Date'].apply(lambda row: int(row[0:2]))
SF['Day'] = SF['Date'].apply(lambda row: int(row[3:5]))

# Verify changes
# Print the first few values of the 'Month' and 'Day' columns to verify extraction
print(SF['Month'].head(2))
print(SF['Day'].head(2))

# Remove variables from the SF data frame
# Remove the 'IncidntNum' column using the del function
del SF['IncidntNum']

# Remove the 'Location' column using the drop function with axis=1 and inplace=True
SF.drop('Location', axis=1, inplace=True)

# Verify changes
# Check that the columns have been removed from the DataFrame
print(SF.columns)

## => Part 4: Analyze the Data

# Summarize variables to obtain statistical information

# Use the function value_counts to summarize the number of crimes committed by type
# Print to display the contents of the CountCategory variable
CountCategory = SF['Category'].value_counts()
print(CountCategory)

# By default, the counts are ordered in descending order.
# The value of the optional parameter ascending can be set to True to reverse this behavior
SF['Category'].value_counts(ascending=True)

# What type of crime was committed the most?

# By nesting the two functions into one command, you can accomplish the same result with one line of code
print(SF['Category'].value_counts(ascending=True))

# Challenge Question: Which PdDistrict had the most incidents of reported crime?
# Provide the Python command(s) used to support your answer

# Possible code for the challenge question
print(SF['PdDistrict'].value_counts(ascending=True))

# Subset the data into smaller data frames

# Logical indexing can be used to select only the rows for which a given condition is satisfied
# For example, the following code extracts only the crimes committed in August, and stores the result in a new DataFrame
AugustCrimes = SF[SF['Month'] == 8]

# How many crime incidents were there for the month of August?
# How many burglaries were reported in the month of August?

# Possible code for the question: How many burglaries were reported in the month of August?
AugustCrimes = SF[SF['Month'] == 8]
AugustCrimesB = SF[SF['Category'] == 'BURGLARY']
len(AugustCrimesB)

# To create a subset of the SF data frame for a specific day, use the function query operand to compare Month and Day at the same time
Crime0704 = SF.query('Month == 7 and Day == 4')
Crime0704

# Verify changes
# Check that the columns have been removed from the DataFrame
print(SF.columns)


## => Part 5: Present the Data

# Step 1: Plotting Data on a Graph
plt.plot(SF['X'], SF['Y'], 'ro')
plt.show()

# Step 2: Mapping Police Department Districts
pd_districts = np.unique(SF['PdDistrict'])
pd_districts_levels = dict(zip(pd_districts, range(len(pd_districts))))
SF['PdDistrictCode'] = SF['PdDistrict'].apply(lambda row: pd_districts_levels[row])

# Step 3: Enhancing the Plot with Folium
from matplotlib import colors
color_dict = dict(zip(pd_districts, list(colors.cnames.values())[0:len(pd_districts)]))
print(color_dict)
obs = list(zip(SF['Y'], SF['X'], SF['PdDistrict']))

map_osm = folium.Map(location=[SF['Y'].mean(), SF['X'].mean()], zoom_start=12)
plotEvery = 50  # Define the interval for plotting markers

for el in obs[0:-1:plotEvery]:
    folium.CircleMarker(el[0:2], color=color_dict[el[2]], fill_color=color_dict[el[2]], radius=10).add_to(map_osm)

map_osm.save('crime_map.html')

