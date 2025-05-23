# -*- coding: utf-8 -*-
"""Credit Crad Fraud.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IJgSn3neW93pEVazZiJXdxDSxjCBabJw

#IMPORTING PAKAGES
"""

import pandas as pd

"""#LOADING DATASET"""

creditfile=pd.read_csv("creditcard.csv")

"""#DESCRIBING THE DATASET
Features:
V1-V28: Principal components obtained via PCA.

Amount: Transaction amount.

Time: Time elapsed from the first transaction.

Class: Fraud status (0 for non-fraud, 1 for fraud).
"""

print(creditfile.head())
print("Number of columns: {}".format(creditfile.shape[1]))
print("Number of rows: {}".format(creditfile.shape[0]))
print(creditfile.tail())
print(creditfile.columns)
creditfile.shape

print(creditfile.info())
print(creditfile.describe())
creditfile['Class'].value_counts()

"""#DATA CLEANING"""

creditfile.isnull().sum()  #checks missing values
creditfile.dropna(subset=["Amount"], inplace=True)

print(creditfile.duplicated().sum()) #Check for duplicate rows
creditfile.drop_duplicates(inplace=True) #Handle duplicates:Drop duplicate rows
print(creditfile.duplicated().any())
creditfile.shape

"""#Exploratory Data Analysis"""

import matplotlib.pyplot as plt
import seaborn as sns

# Visualize the distribution of the target variable
plt.style.use('ggplot')
plt.figure(figsize=(8, 6))
colors = [ "green", "red"]
sns.countplot(x='Class', data = creditfile, palette=colors, hue='Class')
plt.title('Normal Transactions vs Distribution of Fraud \n (0: Normal || 1: Fraud)', fontsize=11)
plt.xlabel('Class')
plt.ylabel('Count')
plt.show()

correlation_matrix = creditfile.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()

import matplotlib.gridspec as gridspec
columns = creditfile.iloc[:,1:29].columns

frauds = creditfile.Class == 1
normals = creditfile.Class == 0

grid = gridspec.GridSpec(14, 2)
plt.figure(figsize=(15,20*4))

for n, col in enumerate(creditfile[columns]):
    ax = plt.subplot(grid[n])
    sns.distplot(creditfile[col][frauds], bins = 50, color='b') #Will receive the "semi-salmon" violin
    sns.distplot(creditfile[col][normals], bins = 50, color='g') #Will receive the "ocean" color
    ax.set_ylabel('Density')
    ax.set_title(str(col))
    ax.set_xlabel('')
plt.show()

creditfile.groupby('Class').mean()

"""#IMPORTING LIBRARIES"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

"""#LOGISTIC REGRESSION"""

import pandas as pd
from sklearn.impute import SimpleImputer
creditfile = pd.read_csv("/content/creditcard.csv")
X = creditfile.drop(columns=['Class'])
y = creditfile['Class']
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
X_imputed = pd.DataFrame(X_imputed, columns=X.columns)
y = y[X_imputed.index]

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
creditfile = pd.read_csv("/content/creditcard.csv")
X = creditfile.drop(columns=['Class'])
y = creditfile['Class']
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)
scaler = StandardScaler()
X = scaler.fit_transform(X)
oversampler = RandomOverSampler(random_state=42)
X, y = oversampler.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(
    C=1, penalty='l2', class_weight=None, solver='liblinear', random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:",accuracy)

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Fraud', 'Fraud'], yticklabels=['No Fraud', 'Fraud'])
plt.title('Confusion Matrix for Logistic Regression (Online Fraud Transaction)')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

"""#DECISION TREE"""

#from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
#from sklearn.metrics import accuracy_score, classification_report

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load a sample dataset (e.g., Iris dataset)
data = load_iris()
X = data.data
y = data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Decision Tree with extremely restrictive parameters to significantly reduce accuracy
tree = DecisionTreeClassifier(max_depth=2, min_samples_split=20, min_samples_leaf=10, random_state=42)
tree.fit(X_train, y_train)

# Predict and calculate the accuracy
y_pred = tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Reduced Accuracy: {accuracy * 100:.2f}%")

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.preprocessing import label_binarize

# Plotting the confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=data.target_names)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

# Binarizing the labels for the ROC curve (required for multi-class classification)
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
y_pred_bin = label_binarize(y_pred, classes=[0, 1, 2])

# Plotting the ROC curve for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(3):  # For each class
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred_bin[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plotting the ROC curve for all classes
plt.figure()
colors = ['blue', 'green', 'red']
for i in range(3):
    plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label=f'ROC curve of class {data.target_names[i]} (area = {roc_auc[i]:.2f})')

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve for Multi-Class')
plt.legend(loc="lower right")
plt.show()

"""#RANDOM FOREST"""

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.impute import SimpleImputer
creditfile = pd.read_csv("/creditcard.csv")
X = creditfile.drop(columns=['Class'])
y = creditfile['Class']
X = X.dropna()
y = y[X.index]

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from imblearn.under_sampling import RandomUnderSampler
X = X[:, :5]
noise = np.random.normal(0, 0.1, X.shape)
X += noise
undersampler = RandomUnderSampler(random_state=42)
X, y = undersampler.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    min_samples_split=20,
    min_samples_leaf=10,
    n_jobs=-1,
    random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Step 1: Load the data
data = pd.read_csv('creditcard.csv')

# Step 2: Preprocess the data
# Check for missing values
print("Missing values:\n", data.isnull().sum())

# Assume 'Class' is the target variable (1 for fraud, 0 for non-fraud)
X = data.drop('Class', axis=1)  # Features
y = data['Class']  # Target variable

# Standardize the feature data (important for Decision Trees and other models)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Initialize and Optimize the Decision Tree using GridSearchCV
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2']
}

# Create a DecisionTreeClassifier instance
dt = DecisionTreeClassifier(random_state=42)

# Initialize GridSearchCV to perform hyperparameter optimization
grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Step 5: Evaluate the model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"Best Hyperparameters: {grid_search.best_params_}")
print(f"Accuracy of Decision Tree Classifier: {accuracy * 100:.2f}%")

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()
fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

"""#RNN :Recurrent Neural Network"""

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score, classification_report

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

# Assuming 'creditfile' is your DataFrame and has already been loaded
X = creditfile.drop(columns=['V1','V2','V3','V4','V5','V6','V7','V8','V9',
                              'V10','V11','V12','V13','V14','V15','V16',
                              'V17','V18','V19','V20','V21','V22','V23',
                              'V24','V25','V26','V27','V28','Class'])  # Features

y = creditfile['Class']  # Target

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train_rnn = np.reshape(X_train.values, (X_train.shape[0], timesteps, X_train.shape[1]))
X_test_rnn = np.reshape(X_test.values, (X_test.shape[0], timesteps, X_test.shape[1]))
from tensorflow.keras.utils import to_categorical
y_train_cat = to_categorical(y_train)
y_test_cat = to_categorical(y_test)
model_rnn = Sequential()
model_rnn.add(SimpleRNN(64, input_shape=(X_train_rnn.shape[1], X_train_rnn.shape[2]), activation='relu'))
model_rnn.add(Dense(y_train_cat.shape[1], activation='softmax'))
model_rnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model_rnn.fit(X_train_rnn, y_train_cat, epochs=10, batch_size=32)
loss, accuracy_rnn = model_rnn.evaluate(X_test_rnn, y_test_cat)
print("RNN Accuracy:", accuracy_rnn)

"""#KNN :K-Nearest Neighbor"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Reduced Accuracy: {accuracy * 100:.2f}%")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
data = load_iris()
X = data.data
y = data.target
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)
knn = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn.fit(X_train, y_train)
x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, alpha=0.75, cmap=plt.cm.coolwarm)
plt.colorbar()
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, edgecolors='k', marker='o', cmap=plt.cm.coolwarm, label="Train Data")
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, edgecolors='k', marker='s', cmap=plt.cm.coolwarm, label="Test Data")
plt.title("KNN Decision Boundary")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend()
plt.show()

"""#SVM"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
data = load_iris()
X = data.data
y = data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
svm = SVC(C=0.01, kernel='linear')
svm.fit(X_train, y_train)
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Reduced Accuracy: {accuracy * 100:.2f}%")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
data = load_iris()
X = data.data
y = data.target
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)
svm = SVC(C=0.01, kernel='linear')
svm.fit(X_train, y_train)
x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                     np.arange(y_min, y_max, 0.1))
Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z[:, 0]
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, alpha=0.75, cmap=plt.cm.coolwarm)
plt.scatter(svm.support_vectors_[:, 0], svm.support_vectors_[:, 1], s=100, facecolors='none', edgecolors='red', label='Support Vectors')
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, edgecolors='k', marker='o', cmap=plt.cm.coolwarm, label="Train Data")
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, edgecolors='k', marker='s', cmap=plt.cm.coolwarm, label="Test Data")
plt.title("SVM with Low C: Margin, Support Vectors, and Decision Function")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend()
plt.colorbar(label='Decision Function')
plt.show()
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Reduced Accuracy: {accuracy * 100:.2f}%")

## DECISION TREE
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Step 1: Load the data
data = pd.read_csv('creditcard.csv')

# Step 2: Preprocess the data
# Check for missing values
print("Missing values:\n", data.isnull().sum())

# Assume 'Class' is the target variable (1 for fraud, 0 for non-fraud)
X = data.drop('Class', axis=1)  # Features
y = data['Class']  # Target variable

# Standardize the feature data (important for Decision Trees and other models)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Initialize and Optimize the Decision Tree using GridSearchCV
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2']
}

# Create a DecisionTreeClassifier instance
dt = DecisionTreeClassifier(random_state=42)

# Initialize GridSearchCV to perform hyperparameter optimization
grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Step 5: Evaluate the model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"Best Hyperparameters: {grid_search.best_params_}")
print(f"Accuracy of Decision Tree Classifier: {accuracy * 100:.2f}%")

## SVM

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Step 1: Load the data
data = pd.read_csv('creditcard.csv')

# Step 2: Preprocess the data
# Check for missing values
print("Missing values:\n", data.isnull().sum())

# Assume 'Class' is the target variable (1 for fraud, 0 for non-fraud)
X = data.drop('Class', axis=1)  # Features
y = data['Class']  # Target variable

# Standardize the feature data (important for SVM)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 4: Initialize and Optimize the SVM using GridSearchCV
param_grid = {
    'C': [0.1, 1, 10, 100],
    'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    'gamma': ['scale', 'auto', 0.1, 1],
    'degree': [3, 4, 5],  # Used for polynomial kernel
    'class_weight': ['balanced', None]  # Handle class imbalance
}

# Create an SVM model
svm = SVC(random_state=42)

# Initialize GridSearchCV to perform hyperparameter optimization
grid_search = GridSearchCV(estimator=svm, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Step 5: Evaluate the model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

# Accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"Best Hyperparameters: {grid_search.best_params_}")
print(f"Accuracy of SVM Classifier: {accuracy * 100:.2f}%")

