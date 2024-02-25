import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# => Part 1


# Import the file stores-dist.txt
salesDist = pd.read_csv('./stores-dist.csv')

# Change the column headings
salesDist.columns = ['district','sales','stores']

# Verify the imported data
print(salesDist.head())

# Drop the district column.
sales = salesDist.drop('district',axis=1)

# Verify that the district column has been dropped
print(sales.head())


# => Part 2

#dependent variable for y axis
y = sales.sales 

#independent variable for x axi
x = sales.stores

# compute the y values from the polynomial model for each x value
order = 1
p = np.poly1d(np.polyfit(x, y ,order))

print('The array p(x) stores the calculated y value from the polynomial model for each x value,\n\n{}.'.format(p(x)))
print('\nThe vector of coefficients p describes this regression model:\n{}'.format(p))
print('\nThe zeroth order term (y-intercept or b) is stored in p[0]: {}.'.format(p[0]))
print('\nThe first order term (slope or m) is stored in p[1]: {}.'.format(p[1]))

from sklearn.metrics import r2_score
r2 = r2_score(y, p(x))
print(f'r2 = {r2}')

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y, p(x))
print(f'mse = {mse}')

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y, p(x))
print(f'mae = {mae}')