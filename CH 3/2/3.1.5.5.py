import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

brainFile = './brainsize.txt'
brainFrame = pd.read_csv(brainFile)

print(brainFrame.head())
print(brainFrame.describe())

# Filter data for males and females
menDf = brainFrame[(brainFrame.Gender == 'Male')]
womenDf = brainFrame[(brainFrame.Gender == 'Female')]

# Calculate mean smarts for males and females
menMeanSmarts = menDf[["PIQ", "FSIQ", "VIQ"]].mean(axis=1)
womenMeanSmarts = womenDf[['PIQ', 'FSIQ', 'VIQ']].mean(axis=1)

# Create a figure with two subplots
fig, axs = plt.subplots(1, 2, figsize=(8, 5))

# Plot the scatter plot for females on the left subplot
axs[0].scatter(womenMeanSmarts, womenDf['MRI_Count'], color="red")
axs[0].set_title('MRI Count vs. Mean Smarts for Females')
axs[0].set_xlabel('Mean Smarts')
axs[0].set_ylabel('MRI Count')

# Plot the scatter plot for males on the right subplot
axs[1].scatter(menMeanSmarts, menDf["MRI_Count"], color="blue")
axs[1].set_title('MRI Count vs. Mean Smarts for Males')
axs[1].set_xlabel('Mean Smarts')
axs[1].set_ylabel('MRI Count')

# Display the plot
plt.show()

# Drop the 'Gender' column from the menDf dataframe to exclude non-numeric data
menDf_numeric = menDf.drop(columns=['Gender'])
# Calculate the correlation matrix for the remaining numeric columns using Pearson method
menCorr = menDf_numeric.corr(method='pearson')

# Drop the 'Gender' column from the womenDf dataframe to exclude non-numeric data
womenDf_numeric = womenDf.drop(columns=['Gender'])
# Calculate the correlation matrix for the remaining numeric columns using Pearson method
womenCorr = womenDf_numeric.corr(method='pearson')

# Set up the subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 8))

# Plot the heatmap for women on the left
sns.heatmap(womenCorr, ax=axs[0], annot=True, cmap='magma', fmt=".2f")
axs[0].set_title('Correlation Heatmap for Women')

# Plot the heatmap for men on the right
sns.heatmap(menCorr, ax=axs[1], annot=True, cmap='viridis', fmt=".2f")
axs[1].set_title('Correlation Heatmap for Men')

# Display the plot
plt.show()