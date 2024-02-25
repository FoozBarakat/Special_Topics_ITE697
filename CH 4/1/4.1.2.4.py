import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the file, stores-dist.csv
salesDist = pd.read_csv('./stores-dist.csv')

# Verify the imported data
print(salesDist.head())

# The district column has no relevance at this time, so it can be dropped.
salesDist = salesDist.rename(columns={'annual net sales':'sales','number of stores in district':'stores'})
print(salesDist.head())

print(salesDist.info())
print(salesDist.corr())

sales = salesDist.drop('district', axis = 1)
print(sales.head())


y = sales['sales']
x = sales.stores


# Increase the size of the plot
plt.figure(figsize=(10, 8))

# Create a scatter plot: Number of stores in the District vs. Annual Net Sales
plt.plot(x, y, 'o', markersize = 8)

# Add axis labels and increase the font size
plt.ylabel('Annual Net Sales')
plt.xlabel('Number of Stores in the District')
plt.title('Relationship between Number of Stores and Annual Net Sales', fontsize = 15)

# Display the scatter plot
plt.show()


# => Linear Regression

m, b = np.polyfit(x, y, 1) 
print ('The slope of line is {:.2f}.'.format(m))
print ('The y-intercept is {:.2f}.'.format(b))
print ('The best fit simple linear regression line is {:.2f}x + {:.2f}.'.format(m, b))

y_mean = y.mean()    
x_mean = x.mean()
print ('The centroid for this dataset is x = {:.2f} and y = {:.2f}.'.format(x_mean, y_mean))

plt.figure(figsize=(10,8))

plt.plot(x,y, '*', markersize = 10, label = "Annual Net Sales") 
plt.plot(x_mean,y_mean, 'o', markersize = 20, color = "r") 

plt.plot(x, m*x + b, '-', label = 'Simple Linear Regression Line', linewidth = 2)

plt.ylabel('Annual Net Sales', fontsize = 13)
plt.xlabel('Number of Stores in District', fontsize = 13)
plt.title('Relationship between Number of Stores and Annual Net Sales', fontsize = 15)

plt.text(x_mean, y_mean, f'({x_mean:.2f}, {y_mean:.2f})', fontsize=12)

plt.annotate('Centroid', xy = (x_mean-0.1, y_mean-5), xytext = (x_mean-3, y_mean-20), arrowprops = dict(facecolor = 'black', shrink=0.05), fontsize = 20)

plt.legend(loc = 'upper right')

# Display the scatter plot
plt.grid(True)
plt.show()


# => Prediction

def predict(query):
    if query >= 1:
        predict = m * query + b
        return predict
    else:
        print ("You must have at least 1 store in the district to predict the annual net sales.")

print('predict(3): ', predict(3))
print('predict(7): ', predict(7))
print('predict(12): ', predict(12))
print('predict(15): ', predict(15))