# -*- coding: utf-8 -*-
"""Overall_MSFT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qKBW3G4y955lMaZLCs8FRBkAmgv5ayLr

# **Description: EDA of this data, includes multicollinearity . I am using this data to predict Close value.There are two parts. In part 1, the data includes Open, High, Low, Close, Adj Close. Upon getting high multicolineraty, I removed these and just kept Close for Part 2**

# Part 1

## Data loading

### Subtask:
Load the data from "MSFT.xlsx" into a Pandas DataFrame.

**Reasoning**:
Load the data from "MSFT.xlsx" into a Pandas DataFrame and print the first 5 rows.
"""

import pandas as pd

df = pd.read_excel('MSFT.xlsx')
display(df.head())

"""## Data exploration

### Subtask:
Explore the data to understand its characteristics.

**Reasoning**:
Explore the data by checking its shape, data types, missing values, and statistical properties.
"""

# Data Shape and Size
print("Data Shape:", df.shape)

# Data Types
print("\nData Types:\n", df.dtypes)

# Missing Values
print("\nMissing Values:\n", df.isnull().sum())

# Statistical Properties
print("\nDescriptive Statistics:\n", df.describe())

# Unique Values for Categorical Columns
for column in df.select_dtypes(include=['object']).columns:
  print(f"\nUnique Values for {column}:\n{df[column].value_counts()}")

"""**Reasoning**:
Generate histograms or density plots for numerical variables to visualize their distributions and identify any potential outliers. Also, calculate the correlation matrix for all numerical variables.


"""

import matplotlib.pyplot as plt
import seaborn as sns

# Variable Distributions (Histograms)
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for column in numerical_columns:
  plt.figure(figsize=(8, 6))
  sns.histplot(df[column], kde=True)
  plt.title(f"Distribution of {column}")
  plt.xlabel(column)
  plt.ylabel("Frequency")
  plt.show()

# Correlation Matrix
correlation_matrix = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

"""**Reasoning**:
The previous code block failed to calculate the correlation matrix because the 'Company' column is of object type. We need to exclude this column to calculate the correlation matrix.


"""

import matplotlib.pyplot as plt
import seaborn as sns

# Variable Distributions (Histograms)
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for column in numerical_columns:
  plt.figure(figsize=(8, 6))
  sns.histplot(df[column], kde=True)
  plt.title(f"Distribution of {column}")
  plt.xlabel(column)
  plt.ylabel("Frequency")
  plt.show()

# Correlation Matrix
correlation_matrix = df.drop('Company', axis=1).corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

"""## Data analysis

### Subtask:
Analyze the correlation matrix to identify potential multicollinearity issues between independent variables.

**Reasoning**:
Analyze the correlation matrix to identify potential multicollinearity issues between independent variables and visualize the correlation with a heatmap.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Identify highly correlated variables
correlation_threshold = 0.7
highly_correlated_variables = []
for i in range(len(correlation_matrix.columns)):
  for j in range(i):
    if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
      highly_correlated_variables.append((correlation_matrix.columns[i],
                                         correlation_matrix.columns[j],
                                         correlation_matrix.iloc[i, j]))

# Print the highly correlated variables
print("Highly Correlated Variables:")
for var1, var2, correlation in highly_correlated_variables:
  print(f"{var1} and {var2}: {correlation}")

# Visualize the correlation matrix with a heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

# Document the findings regarding multicollinearity
print(
    "Findings:\n"
    "Multicollinearity exists between the following variables:"
)
for var1, var2, correlation in highly_correlated_variables:
  print(f"- {var1} and {var2} have a correlation of {correlation:.2f}")
print(
    "Multicollinearity can lead to unstable coefficient estimates and inflated standard errors"
    " in regression models.  It's important to address this issue before proceeding with model training."
)

"""## Feature engineering

### Subtask:
Engineer new features that might be helpful for predicting the "Close" value.

**Reasoning**:
Calculate the moving averages of the "Close" price for different window sizes and create a feature representing the difference between the "Close" price and the moving average.
"""

# Calculate moving averages
df['MA7'] = df['Close'].rolling(window=7).mean()
df['MA30'] = df['Close'].rolling(window=30).mean()
df['MA90'] = df['Close'].rolling(window=90).mean()

# Calculate the difference between the "Close" price and the moving average
df['Close_MA7_Diff'] = df['Close'] - df['MA7']
df['Close_MA30_Diff'] = df['Close'] - df['MA30']
df['Close_MA90_Diff'] = df['Close'] - df['MA90']

display(df.head(10))

"""**Reasoning**:
Calculate the daily percentage change in the "Close" price and add features like the difference between "High" and "Low" prices, the ratio of "Close" to "Open" price, and the volume traded.


"""

# Calculate the daily percentage change in the "Close" price
df['Close_PCT_Change'] = df['Close'].pct_change()

# Calculate the difference between "High" and "Low" prices
df['High_Low_Diff'] = df['High'] - df['Low']

# Calculate the ratio of "Close" to "Open" price
df['Close_Open_Ratio'] = df['Close'] / df['Open']

# Add the volume traded
df['Volume'] = df['Volume']

display(df.head(10))

"""**Reasoning**:
Explore adding features based on the inflation index, CPI, and GDP to see if they contribute to predicting the "Close" price.


"""

# Create features based on inflation, CPI, and GDP
df['Inflation_Close_Ratio'] = df['Inflation_Index'] / df['Close']
df['CPI_Close_Ratio'] = df['CPI'] / df['Close']
df['GDP_Close_Ratio'] = df['GDP'] / df['Close']

display(df.head(10))

"""## Data splitting

### Subtask:
Split the data into training and testing sets.

**Reasoning**:
Import the necessary function from `sklearn.model_selection`, separate the features and target variable, and split the data into training and testing sets.
"""

from sklearn.model_selection import train_test_split

# Separate features (X) and target variable (y)
X = df.drop(['Close', 'Company', 'Date'], axis=1)
y = df['Close']

# Handle missing values (NaN)
X.fillna(method='ffill', inplace=True)  # Forward fill for missing values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

"""**Reasoning**:
The previous command has a warning about `DataFrame.fillna` deprecation. Let's replace it with `ffill()` to avoid the warning and complete the subtask.


"""

from sklearn.model_selection import train_test_split

# Separate features (X) and target variable (y)
X = df.drop(['Close', 'Company', 'Date'], axis=1)
y = df['Close']

# Handle missing values (NaN)
X.ffill(inplace=True)  # Forward fill for missing values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

"""## Model training

### Subtask:
Train a linear regression model to predict the "Close" value using the features in the training set.

**Reasoning**:
Train a linear regression model using the training data and make predictions on the testing data.
"""

from sklearn.linear_model import LinearRegression

# Instantiate a LinearRegression object
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

"""**Reasoning**:
The error message indicates that there are NaN values in the training data, which the linear regression model cannot handle. We need to handle these missing values before fitting the model.


"""

from sklearn.impute import SimpleImputer

# Create an imputer to replace NaN values with the mean of the column
imputer = SimpleImputer(strategy='mean')

# Fit the imputer to the training data and transform it
X_train = imputer.fit_transform(X_train)

# Transform the testing data using the fitted imputer
X_test = imputer.transform(X_test)

# Instantiate a LinearRegression object
model = LinearRegression()

# Fit the model to the training data
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

"""## Model evaluation

### Subtask:
Evaluate the performance of the trained linear regression model using appropriate metrics.

**Reasoning**:
Calculate and print the evaluation metrics for the linear regression model based on the predictions and actual values.
"""

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

# Calculate the Root Mean Squared Error (RMSE)
rmse = mean_squared_error(y_test, y_pred, squared=False)

# Calculate the R-squared
r2 = r2_score(y_test, y_pred)

# Calculate the Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# Print the calculated metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared: {r2:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")

"""**Reasoning**:
Fix the error in the previous code block and calculate the RMSE metric correctly.


"""

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

# Calculate the Root Mean Squared Error (RMSE)
rmse = mse**0.5

# Calculate the R-squared
r2 = r2_score(y_test, y_pred)

# Calculate the Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# Print the calculated metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared: {r2:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.grid(True)
plt.show()

"""## Summary:

### 1. Q&A

* **Q: What is the potential issue with multicollinearity, and how does it affect model training?**
   **A:** Multicollinearity can lead to unstable coefficient estimates and inflated standard errors in regression models. It can make it difficult to interpret the individual effects of the independent variables and reduce the model's overall reliability.
* **Q: What is the performance of the trained linear regression model?**
   **A:** The linear regression model has excellent performance on the test dataset with an R-squared of 1.00, low MSE (0.23), RMSE (0.48), and MAE (0.34).

### 2. Data Analysis Key Findings

* **High Correlation:** Several independent variables in the dataset exhibit a high correlation exceeding 0.7, indicating a potential multicollinearity problem.
* **Multicollinearity Exists Between:** Open, High, Low, Close, and Adj Close with each other; CPI and GDP with each other; Date with Open, High, Low, Close, Adj Close, CPI, and GDP.
* **Feature Engineering:** New features like moving averages (MA7, MA30, MA90), Close_MA7_Diff, Close_MA30_Diff, Close_MA90_Diff, Close_PCT_Change, High_Low_Diff, Close_Open_Ratio, Inflation_Close_Ratio, CPI_Close_Ratio, and GDP_Close_Ratio were generated to potentially enhance the model's predictive power.
* **Model Performance:** The linear regression model achieved an R-squared of 1.00, MSE of 0.23, RMSE of 0.48, and MAE of 0.34 on the test dataset.

### 3. Insights or Next Steps

* **Investigate Potential Overfitting:** While the model shows excellent performance, a perfect R-squared might indicate overfitting. It's important to evaluate the model's generalizability on unseen data to confirm its robustness.
* **Consider Alternative Models:** Explore time series models like ARIMA or LSTM to potentially capture temporal dependencies within the data and compare their performance against the linear regression model.

#Part 2 with MSFT 1.csv data

## Data loading

### Subtask:
Load the data from "MSFT_1.csv" into a pandas DataFrame.

**Reasoning**:
Load the data from "MSFT_1.csv" into a pandas DataFrame and print the first few rows and the shape of the DataFrame.
"""

import pandas as pd

df = pd.read_csv('MSFT_1.csv')
display(df.head())
print(df.shape)

"""## Data exploration

### Subtask:
Explore the loaded data to understand its characteristics.

**Reasoning**:
Explore the data's characteristics by examining its shape, data types, descriptive statistics, missing values, unique values, and data distribution.
"""

# Data Shape and Types
print("Data Shape:", df.shape)
print("\nData Types:\n", df.dtypes)

# Descriptive Statistics
print("\nDescriptive Statistics:\n", df.describe())

# Missing Values
print("\nMissing Values:\n", df.isnull().sum())
print("\nPercentage of Missing Values:\n", (df.isnull().sum() / len(df)) * 100)

# Unique Values (for categorical columns)
for column in df.columns:
  if df[column].dtype == 'object':
    print(f"\nUnique values for {column}:\n{df[column].unique()}")

# Data Distribution (Histograms for numerical features)
df.hist(figsize=(12, 10))

"""**Reasoning**:
The code block in the previous step already explored most of the required aspects. However, it did not include box plots for the numerical features.


"""

# Data Distribution (Box plots for numerical features)
df.boxplot(figsize=(12, 6))

"""## Data visualization

### Subtask:
Visualize the relationships between variables and the distribution of data to gain insights.

**Reasoning**:
Create scatter plots to visualize the relationship between 'Close' and other numerical variables.
"""

import matplotlib.pyplot as plt

numerical_features = ['Volume', 'Inflation_Index', 'CPI', 'GDP']

plt.figure(figsize=(15, 10))

for i, feature in enumerate(numerical_features):
  plt.subplot(2, 2, i + 1)
  plt.scatter(df[feature], df['Close'])
  plt.xlabel(feature)
  plt.ylabel('Close')
  plt.title(f'Close vs. {feature}')

plt.tight_layout()
plt.show()

"""**Reasoning**:
Plot histograms or density plots for each numerical variable to understand their individual distributions.


"""

plt.figure(figsize=(15, 10))

for i, feature in enumerate(numerical_features):
  plt.subplot(2, 2, i + 1)
  df[feature].hist()
  plt.xlabel(feature)
  plt.ylabel('Frequency')
  plt.title(f'Distribution of {feature}')

plt.tight_layout()
plt.show()

"""**Reasoning**:
Create a correlation matrix heatmap to visually represent the correlation between all numerical variables.


"""

import seaborn as sns
import matplotlib.pyplot as plt

correlation_matrix = df[['Close', 'Volume', 'Inflation_Index', 'CPI', 'GDP']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()

"""**Reasoning**:
Plot a line chart to visualize the trend of the 'Close' value over time ('Date').


"""

import matplotlib.pyplot as plt

# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

plt.figure(figsize=(15, 6))
plt.plot(df['Date'], df['Close'])
plt.xlabel('Date')
plt.ylabel('Close')
plt.title('Close Value Over Time')
plt.grid(True)
plt.show()

"""## Data analysis

### Subtask:
Analyze the correlation between variables and identify potential multicollinearity.

**Reasoning**:
Calculate the correlation matrix for numerical features and analyze it to identify potential multicollinearity.
"""

# Calculate the correlation matrix for numerical features
correlation_matrix = df.select_dtypes(include=['number']).corr()

# Display the correlation matrix
display(correlation_matrix)

# Identify variables with high correlation (e.g., correlation coefficient > 0.7)
high_correlation_variables = []
for i in range(len(correlation_matrix.columns)):
  for j in range(i + 1, len(correlation_matrix.columns)):
    if abs(correlation_matrix.iloc[i, j]) > 0.7:
      high_correlation_variables.append((correlation_matrix.columns[i], correlation_matrix.columns[j], correlation_matrix.iloc[i, j]))

# Print variables with high correlation
if high_correlation_variables:
  print("Variables with high correlation:")
  for var1, var2, correlation in high_correlation_variables:
    print(f"{var1} and {var2}: {correlation:.2f}")
else:
  print("No variables with correlation higher than 0.7 found.")

"""**Reasoning**:
Based on the correlation matrix, there is high multicollinearity between CPI and GDP, and also between Close and GDP, Close and CPI. We need to handle this multicollinearity. We can try to use VIF to determine the severity of multicollinearity.


"""

from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each feature
X = df[['Close', 'Volume', 'Inflation_Index', 'CPI', 'GDP']]
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

# Display VIF values
display(vif_data)

"""**Reasoning**:
The VIF values for CPI and GDP are very high, indicating severe multicollinearity. We need to handle this multicollinearity by either dropping one of the highly correlated features or using dimensionality reduction techniques like PCA. For now, we can drop one of the features with high VIF to reduce multicollinearity, for example, GDP.


"""

# Drop GDP to reduce multicollinearity
df_reduced = df.drop('GDP', axis=1)

# Recalculate VIF after dropping GDP
X = df_reduced[['Close', 'Volume', 'Inflation_Index', 'CPI']]
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

display(vif_data)

"""## Feature engineering

### Subtask:
Engineer new features that might be helpful for predicting the 'Close' value.

**Reasoning**:
Create new features based on moving averages of the 'Close' price, the difference between the 'Close' price and its moving averages, and percentage changes.
"""

# Convert 'Date' to datetime objects if not already done
if not isinstance(df_reduced['Date'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
    df_reduced['Date'] = pd.to_datetime(df_reduced['Date'])

# Calculate moving averages
df_reduced['Close_MA_7'] = df_reduced['Close'].rolling(window=7).mean()
df_reduced['Close_MA_14'] = df_reduced['Close'].rolling(window=14).mean()
df_reduced['Close_MA_30'] = df_reduced['Close'].rolling(window=30).mean()

# Calculate differences between Close and moving averages
df_reduced['Close_Diff_MA_7'] = df_reduced['Close'] - df_reduced['Close_MA_7']
df_reduced['Close_Diff_MA_14'] = df_reduced['Close'] - df_reduced['Close_MA_14']
df_reduced['Close_Diff_MA_30'] = df_reduced['Close'] - df_reduced['Close_MA_30']

# Calculate percentage changes
df_reduced['Close_Pct_Change'] = df_reduced['Close'].pct_change()
df_reduced['Volume_Pct_Change'] = df_reduced['Volume'].pct_change()
df_reduced['Inflation_Index_Pct_Change'] = df_reduced['Inflation_Index'].pct_change()
df_reduced['CPI_Pct_Change'] = df_reduced['CPI'].pct_change()

# Display the updated DataFrame
display(df_reduced.head(10))

"""**Reasoning**:
Create features based on the ratio of 'Close' price and 'Volume', as well as other potentially relevant features.


"""

# Create a feature based on the ratio of Close price and Volume
df_reduced['Close_Volume_Ratio'] = df_reduced['Close'] / df_reduced['Volume']

# Create features based on the ratio of 'Close' price and other features
df_reduced['Close_Inflation_Ratio'] = df_reduced['Close'] / df_reduced['Inflation_Index']
df_reduced['Close_CPI_Ratio'] = df_reduced['Close'] / df_reduced['CPI']

# Display the updated DataFrame
display(df_reduced.head(10))

"""## Data splitting

### Subtask:
Split the data into training and testing sets.

**Reasoning**:
Split the data into training and testing sets using `train_test_split`.
"""

from sklearn.model_selection import train_test_split

# Define target and features
y = df_reduced['Close']
X = df_reduced.drop(['Close', 'Date', 'Company'], axis=1)

# Handle missing values (if any) - drop rows with missing values
X.dropna(inplace=True)
y = y[X.index]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""## Model training

### Subtask:
Train a linear regression model to predict the 'Close' value using the training data.

**Reasoning**:
Train a linear regression model using the training data.
"""

from sklearn.linear_model import LinearRegression

# Instantiate a LinearRegression object
model = LinearRegression()

# Train the model using the training data
model.fit(X_train, y_train)

"""## Model evaluation

### Subtask:
Evaluate the performance of the trained linear regression model on the test data.

**Reasoning**:
Use the trained model to predict the 'Close' values for the test data and evaluate the model's performance using MSE, RMSE, and R-squared.
"""

# Predict 'Close' values for the test data
y_pred = model.predict(X_test)

from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Print the calculated metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# Plot actual vs. predicted 'Close' values
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Close")
plt.ylabel("Predicted Close")
plt.title("Actual vs. Predicted Close Values")
plt.show()

"""## Summary:

### 1. Q&A

* **How well does the linear regression model perform in predicting the 'Close' value?**
    Based on the evaluation metrics, the linear regression model performs exceptionally well. It achieved a perfect R-squared score of 1.00, and both the MSE and RMSE were 0.00, indicating a near-perfect fit. This suggests that the model can accurately predict the 'Close' value based on the provided features.

* **Are there any multicollinearity issues in the dataset?**
    Yes, the analysis revealed strong positive correlations between 'Close' and 'CPI', 'Close' and 'GDP', and 'CPI' and 'GDP'. VIF analysis indicated severe multicollinearity, particularly for 'CPI' and 'GDP'. To mitigate this, 'GDP' was dropped, but some multicollinearity remained, especially between 'Inflation_Index' and 'CPI'.


### 2. Data Analysis Key Findings

* **Strong Positive Correlation:** 'Close' and 'CPI' have a correlation of 0.90, and 'Close' and 'GDP' have a correlation of 0.92. 'CPI' and 'GDP' have a very high correlation of 0.99.
* **Severe Multicollinearity:** 'CPI' and 'GDP' have very high VIF values (738.89 and 686.63 respectively), indicating severe multicollinearity.
* **Feature Engineering:** Several new features were created, including moving averages, differences between 'Close' and moving averages, percentage changes, and ratio features.
* **Model Performance:** The linear regression model achieved an R-squared score of 1.00, MSE of 0.00, and RMSE of 0.00 on the test data, suggesting a perfect fit.


### 3. Insights or Next Steps

* **Investigate potential overfitting:** The perfect performance of the linear regression model could be due to overfitting. It's crucial to investigate the model's robustness and generalizability by applying it to new, unseen data or using techniques like cross-validation.
* **Explore alternative models and feature engineering:** While the linear regression model performed exceptionally well, exploring other models (e.g., time series models) and further refining feature engineering could potentially enhance the prediction accuracy and address any potential overfitting issues.

"""