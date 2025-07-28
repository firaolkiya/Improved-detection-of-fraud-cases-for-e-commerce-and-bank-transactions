# Fraud Detection Data Analysis Report

This report summarizes the data cleaning and preprocessing steps, key insights and visualizations from exploratory data analysis (EDA), feature engineering choices, and the analysis and strategy for handling class imbalance for the provided fraud detection datasets (`Fraud_Data.csv`, `IpAddress_to_Country.csv`, and `creditcard.csv`).

## Data Cleaning and Preprocessing Summary

This report summarizes the initial data cleaning and preprocessing steps performed on the three datasets: 'Fraud data' (`dff`), 'Ip data' (`dfi`), and 'Credit card data' (`dfc`). The focus was on handling missing values, removing duplicate entries, and ensuring appropriate data types for subsequent analysis.

### Handling Missing Values

Missing values were checked across all columns in `dff`, `dfi`, and `dfc`. No missing values were found in any of the dataframes. Therefore, no imputation or removal of missing values was required.

### Removing Duplicates

Duplicate rows were identified and removed from each dataframe.
*   `dff`: No duplicate rows were found.
*   `dfi`: No duplicate rows were found.
*   `dfc`: 1081 duplicate rows were found in the 'Credit card data'. These duplicates were removed, resulting in a reduction in the number of rows from 284,807 to 283,726.

### Correcting Data Types

Data type correction was performed primarily on time-related columns to ensure they were in the correct datetime format for time-series analysis and feature engineering.
*   In `dff`, the 'signup_time' and 'purchase_time' columns were converted to datetime objects.
*   In `dfc`, the 'Time' column, which represented time in seconds since the epoch, was converted to datetime objects.
*   The data types in `dfi` were already suitable for the analysis, and no type conversions were necessary for this dataframe.

These steps ensured the data was clean, free of duplicates, and had the correct data types, preparing it for further exploration and modeling.

## Key Insights and Visualizations from EDA

Exploratory Data Analysis (EDA) was conducted through univariate and bivariate analysis to understand the distribution of features and the relationships between variables, particularly concerning the 'class' variable indicating fraud.

### Univariate Analysis Insights:

*   **`dff` DataFrame (Fraud Data):**
    *   **Purchase Value:** The distribution of `purchase_value` is right-skewed, with most purchases having a lower value. The mean purchase value is around $37.
    *   **Age:** The `age` distribution is also right-skewed, with a majority of users being in their early 30s. The mean age is approximately 33.
    *   **Categorical Features:**
        *   `source`: The 'SEO' and 'Ads' are the most common sources for users.
        *   `browser`: 'Chrome' is the most frequently used browser, followed by 'Safari'.
        *   `sex`: There is a relatively balanced distribution between male and female users.
*   **`dfc` DataFrame (Credit Card Data):**
    *   **Transaction Amount:** The distribution of `Amount` is heavily right-skewed, indicating most transactions are for small amounts.
    *   **Class:** The `Class` variable is highly imbalanced, with a vast majority of transactions being non-fraudulent (Class 0).
*   **`dfi` DataFrame (IP Address Data):**
    *   **Country Distribution:** The analysis of IP addresses shows that the United States has the highest number of users by a large margin.

### Bivariate Analysis Insights:

*   **Purchase Value and Age (`dff`):**
    *   The scatter plot of `purchase_value` vs. `age` doesn't show a clear linear relationship, suggesting that purchase amount is not strongly dependent on the user's age.
*   **Purchase Value and Class (`dff`):**
    *   The box plot of `purchase_value` by `class` reveals that fraudulent transactions (`class`=1) tend to have a similar median purchase value to non-fraudulent ones, but with a slightly wider interquartile range, indicating more variability in purchase amounts for fraudulent activities.
*   **Time between Signup and Purchase (`dff`):**
    *   The analysis of `time_since_signup` shows that fraudulent transactions often occur very shortly after account creation. This is a strong indicator of fraudulent behavior.
*   **Categorical Features and Class (`dff`):**
    *   **Source vs. Class:** The count plot shows that 'Direct' and 'SEO' sources have a noticeable number of fraudulent transactions.
    *   **Browser vs. Class:** 'Chrome' and 'FireFox' are the browsers most associated with fraudulent activities.
    *   **Sex vs. Class:** Both male and female users are victims of fraud, with no significant difference in proportion.
*   **Transaction Amount and Class (`dfc`):**
    *   The box plot of `Amount` by `Class` in the credit card dataset shows that while the median transaction amount for fraudulent and non-fraudulent transactions is similar, fraudulent transactions have a much wider range and a higher maximum value.
*   **Correlation Matrix (`dfc`):**
    *   The heatmap of the correlation matrix for the `dfc` dataframe (which contains PCA-transformed features `V1` to `V28`) shows that there is no strong multicollinearity among these anonymized features. Some weak correlations exist between `Amount` and a few of the `V` features (e.g., `V2`, `V4`, `V20`).

The EDA provided valuable insights into the data distributions and relationships, highlighting potential features and patterns relevant for fraud detection.

## Feature Engineering Details

The feature engineering process focused on creating new features from existing time and IP address data within the `dff` and `dfi` dataframes to enhance the predictive power for fraud detection.

**Temporal Features Extraction:**
Two temporal features were extracted from the 'purchase_time' column in the `dff` dataframe:
- `hour_of_day`: Extracted the hour (0-23) of the purchase time using `dff['purchase_time'].dt.hour`.
- `day_of_week`: Extracted the day of the week (0=Monday, 6=Sunday) of the purchase time using `dff['purchase_time'].dt.dayofweek`.
These features capture potential daily and weekly patterns in fraudulent activity.

**Time Since Signup Calculation:**
The `time_since_signup` feature was calculated as the time difference between `purchase_time` and `signup_time` in hours.
This was done by subtracting the `signup_time` datetime object from the `purchase_time` datetime object, getting the total seconds of the timedelta, and then dividing by 3600 to convert to hours.
The calculation used `(dff['purchase_time'] - dff['signup_time']).dt.total_seconds() / 3600`.
Negative values, which could occur if purchase_time was before signup_time (potentially data errors), were handled by setting them to 0 using `.apply(lambda x: max(0, x))`.
This feature aims to identify transactions that occur suspiciously quickly after account creation, which can be indicative of fraudulent accounts.

**IP Address to Country Mapping:**
To enrich the `dff` dataframe with geographical information, IP addresses were mapped to countries using the `dfi` dataframe (IpAddress_to_Country).
The steps involved were:
a. **IP Address Conversion:** The `ip_address` column in `dff` was converted from a float/string representation to an integer using a custom function `ip_to_int`. This is necessary because the IP ranges in `dfi` are represented as integers.
b. **Sorting IP Ranges:** The `dfi` dataframe was sorted by the `lower_bound_ip_address` to enable efficient searching for the corresponding country for each IP.
c. **Country Lookup:** A custom function `find_country` was applied to each integer IP address in `dff`. This function uses `searchsorted` on the sorted `dfi['lower_bound_ip_address']` to quickly find the potential range where the IP might fall.
d. **Range Verification:** The function then verifies if the IP integer is indeed within the `lower_bound_ip_address` and `upper_bound_ip_address` of the identified row in `dfi`. If a match is found, the corresponding `country` is returned; otherwise, `None` is returned.
This process effectively added a `country` column to the `dff` dataframe, allowing for geographical analysis of fraudulent activities.

**Rationale for Feature Creation:**
These new features were created based on the understanding that fraudulent activities often exhibit specific temporal and geographical patterns:
- **Temporal Features (hour_of_day, day_of_week, time_since_signup):** Fraudulent transactions may be concentrated at certain times of the day or days of the week, or occur immediately after account creation. Capturing these temporal aspects can help a model identify suspicious timing.
- **Geographical Feature (country):** The origin country of a transaction's IP address can be a strong indicator of fraud, as certain countries may have higher fraud rates or be associated with specific fraud rings. Mapping IP addresses to countries provides this crucial geographical context.
These features provide valuable information that is not directly available in the raw data and are expected to improve the performance of a fraud detection model.

## Class Imbalance Handling Strategy

**1. Understanding Class Imbalance:**
In fraud detection datasets like 'Fraud data' (dff) and 'Credit card data' (dfc), class imbalance is a significant issue.
It refers to the unequal distribution of observations across different classes, where the minority class (fraudulent transactions) is substantially less represented than the majority class (non-fraudulent transactions).
As observed in the EDA and confirmed during the class imbalance check:
- In `dff`, the minority class ('1', fraud) constitutes only 9.36% of the data, while the majority class ('0', non-fraud) is 90.64%.
- In `dfc`, the minority class ('1', fraud) constitutes only 0.1727% of the data, while the majority class ('0', non-fraud) is 99.8273%.

**2. Why Class Imbalance is a Problem:**
Standard machine learning models are often designed assuming a balanced class distribution.
When faced with imbalanced data, these models tend to be biased towards the majority class.
They might achieve high overall accuracy by simply predicting the majority class for most instances, but they perform poorly in identifying the minority class, which is the class of interest (fraud) in this problem.
This leads to a high number of false negatives (missing fraudulent transactions), which is undesirable in fraud detection.

**3. Chosen Strategy: SMOTE**
To address the class imbalance, the Synthetic Minority Over-sampling Technique (SMOTE) was chosen.
SMOTE is an oversampling technique that aims to balance the class distribution by increasing the number of instances in the minority class.

**4. How SMOTE Works (High Level):**
Instead of simply duplicating existing minority class samples, SMOTE creates *synthetic* samples.
It works by selecting a minority class instance and finding its k-nearest neighbors.
Synthetic samples are then generated along the line segments connecting the minority instance and its selected neighbors.
This process helps to create a more diverse set of minority class samples, making the decision boundary for the minority class more robust.

**5. Application of SMOTE to Training Data:**
It is crucial to apply SMOTE *only* to the training data.
The dataset was first split into training and testing sets (e.g., 70% train, 30% test) using `train_test_split` with stratification to maintain the original class distribution in both sets.
SMOTE was then applied exclusively to the training set (`X_train`, `y_train`).
This prevents data leakage, where information from the test set could influence the training process, leading to overly optimistic performance estimates.

**6. Effect of SMOTE on Class Distribution:**
After applying SMOTE to the training data, the class distribution was significantly altered.
The number of minority class samples was increased to match the number of majority class samples.
For `dff`, the training data went from a minority class count of 9905 and majority class count of 95872 to a balanced distribution where both classes have 95872 samples.
The percentage distribution became approximately 50.00% for class 0 and 50.00% for class 1.
For `dfc`, the training data went from a minority class count of 344 and majority class count of 198607 to a balanced distribution where both classes have 198607 samples.
The percentage distribution became approximately 50.00% for class 0 and 50.00% for class 1.
This balanced training set is now suitable for training machine learning models, as it provides sufficient examples of the minority class for the model to learn the patterns associated with fraud.
The model will then be evaluated on the original, imbalanced test set (`X_test`, `y_test` or `X_test_c`, `y_test_c`) to get a realistic estimate of its performance on unseen, real-world data.
