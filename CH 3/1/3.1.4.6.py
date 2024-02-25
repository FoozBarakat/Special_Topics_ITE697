import pandas as pd
import matplotlib.pyplot as plt

## => Part 1


# Load the CSV file into a DataFrame
df = pd.read_csv('rpi_describe.csv')

# View the contents of the first five rows in the dataframe
print(df.head())

# View the contents of the last five rows in the dataframe
print(df.tail())

# Use the describe method of the new dataframe to view the table of statistics
print(df.describe())

# Add a new column to the dataframe and populate it with rounded weights
df['rounded'] = df['weight'].round()
# Verify that values were added
print(df.head())

# Create the new column named "diff" and fill it with values
df['diff'] = df['rounded'] - 20

# Check the result
print(df.head())

# Calculate descriptive statistics for the 'rounded' column
count = df['rounded'].count()
mean = df['rounded'].mean()
median = df['rounded'].median()
std = df['rounded'].std()
rng = df['rounded'].max() - df['rounded'].min()

# Create strings reporting the descriptive statistics
countstring = "The count of the dataset is {}.".format(count)
meanstring = "The mean of the dataset is {:.2f}.".format(mean)
stdstring = "The standard deviation of the dataset is {:.2f}.".format(std)
rangestring = "The range of the dataset is {:.2f} (min: {:.2f}, max: {:.2f}).".format(rng, df['rounded'].min(), df['rounded'].max())

# Display the strings
print(countstring)
print(meanstring)
print(stdstring)
print(rangestring)


## => Part 2


# Create a variable called 'freq' to hold the weight values and their frequencies
freq = df['rounded'].value_counts()

# Convert the freq object to a data frame. Use to_frame().
freq = freq.to_frame().reset_index()

# Rename the columns to 'value' and 'frequency'
freq.columns = ['value', 'freq']

# Create a new figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Plot the first graph on the left subplot
axs[0].plot(freq.value, freq.freq, "o", markersize=10, color='red')
axs[0].set_title('Frequency Distribution of Weight (rounded)')
axs[0].set_xlabel('Weight')
axs[0].set_ylabel('Frequency')

# Create a variable called 'freq' to hold the weight values and their frequencies
freq_weight = df['weight'].value_counts()

# Convert the freq object to a data frame. Use to_frame().
freq_weight = freq_weight.to_frame().reset_index()

# Rename the columns to 'value' and 'frequency'
freq_weight.columns = ['value', 'freq_weight']

# Plot the second graph on the right subplot
axs[1].plot(freq_weight.value, freq_weight.freq_weight, "o", markersize=10, color='pink')
axs[1].set_title('Frequency Distribution of Weight (not rounded)')
axs[1].set_xlabel('Weight')
axs[1].set_ylabel('Frequency')

# Adjust the layout
plt.tight_layout()

# Display the plot
plt.show()
