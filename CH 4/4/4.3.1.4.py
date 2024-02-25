# Regular EDA (exploring data analysis) and plotting libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Turn the categories into numbers
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
 
# Models from Scikit-Learn
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# Model Evaluation 
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, roc_curve, auc

# => Load data
df_1 = pd.read_csv("./Bejaia region Dataset.csv")
df_2 = pd.read_csv("./Sidi-Bel Abbes Region Dataset.csv")
print(df_1.shape, df_2.shape)

df = pd.concat([df_1, df_2])
print(df.shape)

# => Data Exploration 
print(df.head())

print(df.tail())

print(df.isna().sum())

# drop the missing target variables 
df.dropna(inplace=True)
print(df.isna().sum())
print(df["Classes"].value_counts())

# remove the extra spaces
# 1,2,3,5 => not fire
# 1, 3 => fire
df["Classes"].replace({"not fire ": "not fire", "not fire  ": "not fire", "not fire   ": "not fire", "not fire     ": "not fire", "fire ": "fire", "fire   ": "fire"}, inplace=True)

print(df["Classes"].value_counts())

df["Classes"].value_counts().plot(kind="bar", figsize=(8, 6), color=["salmon", "lightblue"]);
plt.title("Classes")
plt.ylabel("Amount")
plt.yticks(np.arange(0, 145, 10))
plt.xticks(rotation=0);
plt.show()

print(df.info())
print(df.describe())

# Compare Classes column with month column
print(pd.crosstab(df.Classes, df.month))

#Create a plot of crosstab
pd.crosstab(df.Classes, df.month).plot(kind="bar", figsize=(10, 6), color=["salmon", "lightblue", "lightgreen", "lightpink"])

plt.title("Fire Frequency for Month")
plt.ylabel("Amount")
plt.yticks(np.arange(0, 55, 5))
plt.xticks(rotation=0);
plt.show()

# Temp vs. wind
# Create another figure
plt.figure(figsize=(10, 6))

# Scatter with positive examples
plt.scatter(df.Temperature[df.Classes=="fire"], df.Ws[df.Classes=="fire"], c="salmon")

# Scatter with negative examples
plt.scatter(df.Temperature[df.Classes=="not fire"], df.Ws[df.Classes=="not fire"], c="lightblue")

# Add some helpful info
plt.title("Fire in function of Temperature and Wind Speed Rate")
plt.xlabel("Temperature")
plt.ylabel("Wind Speed")
plt.legend(["Fire", "Not Fire"])
plt.show()

# Check the distribution of the Temperature column with a histogram
plt.figure(figsize=(10, 6))
plt.hist(df.Temperature, bins=20, color='skyblue', edgecolor='black')  # Adjust the number of bins as needed
plt.title('Distribution of Temperature')
plt.xlabel('Temperature')
plt.ylabel('Frequency')
plt.show()

# Temp vs humidity

# Create another figure
plt.figure(figsize=(10, 6))

# Scatter with positive examples
plt.scatter(df.Temperature[df.Classes=="fire"], df.RH[df.Classes=="fire"], c="salmon")

# Scatter with negative examples
plt.scatter(df.Temperature[df.Classes=="not fire"], df.RH[df.Classes=="not fire"], c="lightblue")

# Add some helpful info
plt.title("Fire in function of Temperature and Relative Humidity")
plt.xlabel("Temperature")
plt.ylabel("Relative Humidity")
plt.legend(["Fire", "Not Fire"])
plt.show()

df.head()
print(df.dtypes)

# delete the year column and change the DC, FWI columns to float type
df = df.drop('year', axis=1)
df["DC"] = df["DC"].astype(float)
df["FWI"] = df["FWI"].astype(float)

# change the categorical Classes to numerical
categorical_features = ["Classes"]
one_hot = OneHotEncoder()
transformer = ColumnTransformer([("one_hot", one_hot, categorical_features)], remainder="passthrough")

transformed_y = transformer.fit_transform(df)
df["Classes"] = transformed_y

# Ensure all columns are numeric
df = df.apply(pd.to_numeric, errors='coerce')
# Make a correlation matrix
print(df.corr())

# Let's make our correlation matrix a little prettier
corr_matrix = df.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, linewidths=0.5, fmt=".2f", cmap="YlGnBu", ax=ax)
ax.set_title('Correlation Matrix')
plt.show()
df["Classes"].value_counts()

# => Modeling

# Split data into X and y
x = df.drop("Classes", axis=1)

y = df["Classes"]
x.head()
y.head()

# Split data into train and test sets
np.random.seed(5)

# Split into train & test set
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3)

print(len(x_train), len(x_test), len(x), 194+49)

# Put models in a dictionary
models = {"Linear SVC": LinearSVC(dual='auto', max_iter=10000), "KNN": KNeighborsClassifier(), "Random Forest": RandomForestClassifier()}

# Create a function to fit and score models
def fit_and_score(models, x_train, x_test, y_train, y_test):
    """
    Fits and evaluates given machine learning models.
    models : a dict of different Scikit-Learn machine learning models
    x_train : training data (no labels)
    x_test : testing data (no labels)
    y_train : training labels
    y_test : test labels
    """
    # Set random seed
    np.random.seed(5)
    # Make a dictionary to keep model scores
    model_scores = {}
    # Loop through models
    for name, model in models.items():
        # Fit the model to the data
        model.fit(x_train, y_train)
        # Evaluate the model and append its score to model_scores
        y_pred = model.predict(x_test)
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        roc_auc = auc(fpr, tpr)
        model_scores[name] = roc_auc
    return model_scores

model_scores = fit_and_score(models=models, x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)

print(model_scores)

# => Model Comparision
model_compare = pd.DataFrame(model_scores, index=["Accuracy"])
ax = model_compare.T.plot.bar(legend=False)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.xticks(rotation=0)
plt.ylabel("Accuracy")
plt.xlabel("Model")
plt.title("Model Comparison")
for p in ax.patches:
    ax.annotate(str(round(p.get_height(), 2)), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')
plt.legend(["Accuracy"], loc='upper left')
plt.show()
