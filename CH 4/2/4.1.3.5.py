import pandas as pd
from sklearn import tree
from io import StringIO
import subprocess
import numpy as np
from sklearn.model_selection import train_test_split

# => Part 1


# Create a pandas dataframe called "training" from the titanic-train.csv file
training = pd.read_csv("./titanic_train.csv")

# Verify the contents of the training dataframe using the pandas info() method
print(training.info())

# View the first few rows of the data
print(training.head())

# Replace string data with numeric labels
training["Gender"] = training["Gender"].apply(lambda toLabel: 0 if toLabel == 'male' else 1)

# Verify that the Gender variable has been changed
print(training.head())

# Address missing values in the dataset
print(training["Age"].fillna(training["Age"].mean(), inplace=True))

# Verify that the missing values for the age variable have been eliminated
print(training.info())

# Create an array object with the variable that will be the target for the model
y_target = training["Survived"].values

# Create an array of the values that will be the input for the model
columns = ["Fare", "Pclass", "Gender", "Age", "SibSp"]
X_input = training[list(columns)].values

# Create clf_train as a decision tree classifier object
clf_train = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)

# Train the model using the fit() method of the decision tree object
clf_train = clf_train.fit(X_input, y_target)

# Evaluate the model and print the result
score = clf_train.score(X_input, y_target) * 100
print(f"The accuracy of the model is: {score:.1f}%")

# Create a DOT file for the decision tree visualization
# with open("./titanic.dot", 'w') as f:
  # Export the decision tree classifier to the DOT file
  # f = tree.export_graphviz(clf_train, out_file=f, feature_names=columns)

# Define the shell command
# command = "dot -Tpng ./titanic.dot -o ./titanic.png"

# Run the command
# subprocess.run(command, shell=True)


# => Part 2

testing = pd.read_csv("./titanic_test.csv")

# Display the number of records in the dataset
print("Number of records in the dataset:", len(testing))

# Display which variables are missing values and how many are missing
print("Variables with missing values and their counts:")
print(testing.isnull().sum())

# Replace the Gender labels in the testing dataframe
testing["Gender"] = testing["Gender"].apply(lambda toLabel: 0 if toLabel == 'male' else 1)

# Replace missing age values with the mean of the ages
testing["Age"].fillna(testing["Age"].mean(), inplace=True)

# Verify the changes
print("Updated data:")
print(testing.info())
print(testing.head())

# Create the array of input variables from the testing data set
X_input = testing[list(columns)].values

# Apply the model to the testing data set
target_labels = clf_train.predict(X_input)

# Convert the target array into a pandas dataframe
target_labels = pd.DataFrame({'Est_Survival': target_labels, 'Name': testing['Name']})

all_data = pd.read_csv("./titanic_all.csv")

# Merge the target_labels dataframe and the all_data dataframe on the field Name
testing_results = pd.merge(target_labels, all_data[['Name', 'Survived']], on=['Name'])

# Compute the accuracy as a ratio of matching observations to total observations
acc = np.sum(testing_results['Est_Survival'] == testing_results['Survived']) / float(len(testing_results))

# Print the accuracy
print(f"The accuracy of the estimated labels is: {acc*100:.2f}%")


# => Part 3

all_data = pd.read_csv("./titanic_all.csv", usecols=['Survived','Pclass','Gender','Age','SibSp','Fare'])

# Display the number of records in the dataset
print("Number of records in the dataset:", len(all_data))

# View info for the new dataframe
print(all_data.info())

# Label the gender variable with 0 and 1
all_data["Gender"] = all_data["Gender"].apply(lambda toLabel: 0 if toLabel == 'male' else 1)

# Replace missing Age values with the mean age
all_data["Age"].fillna(all_data["Age"].mean(), inplace=True)

# Display the first few rows of the data set
print(all_data.head())

#create the input and target variables as uppercase X and lowercase y. Reuse the columns variable.
X = all_data[list(columns)].values
y = all_data["Survived"].values

#generate the four testing and training data arrays with the train_test_split() method
X_train,X_test,y_train,y_test=train_test_split(X, y, test_size=0.40, random_state=0)

#create the training decision tree object
clf_train = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)

#fit the training model using the input and target variables
clf_train = clf_train.fit(X_train, y_train)

#score the model on the two datasets and store the scores in variables. Convert the scores to strings using str()
train_score = str(clf_train.score(X_train,y_train))
test_score = str(clf_train.score(X_test,y_test))

# Convert scores to floats
train_score = float(train_score)
test_score = float(test_score)

# Print scores as percentages with two decimal places
print(f'Training score = {train_score:.2%}, Testing score = {test_score:.2%}')

