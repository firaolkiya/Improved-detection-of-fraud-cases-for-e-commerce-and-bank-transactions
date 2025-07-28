from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

# Separate features (X) and target (y) for the Fraud Data (dff)
dff = pd.read_csv("data/processed/dff.csv")
dfc = pd.read_csv("data/processed/dfc.csv")
if '_class' in dff.columns:
    X = dff.drop('class', axis=1)
    y = dff['class']

    # Perform a train-test split
    # We use stratify=y to ensure the class distribution is similar in both train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    print("Original data shape:", dff.shape)
    print("Features shape (X):", X.shape)
    print("Target shape (y):", y.shape)
    print("\nTraining set shape:")
    print("X_train:", X_train.shape)
    print("y_train:", y_train.shape)
    print("\nTesting set shape:")
    print("X_test:", X_test.shape)
    print("y_test:", y_test.shape)

elif 'Class' in dfc.columns:
    # Separate features (X) and target (y) for the Credit Card Data (dfc)
    Xc = dfc.drop('Class', axis=1)
    yc = dfc['Class']

    # Perform a train-test split
    # We use stratify=yc to ensure the class distribution is similar in both train and test sets
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(Xc, yc, test_size=0.3, random_state=42, stratify=yc)

    print("Original data shape (dfc):", dfc.shape)
    print("Features shape (Xc):", Xc.shape)
    print("Target shape (yc):", yc.shape)
    print("\nTraining set shape (dfc):")
    print("X_train_c:", X_train_c.shape)
    print("y_train_c:", y_train_c.shape)
    print("\nTesting set shape (dfc):")
    print("X_test_c:", X_test_c.shape)
    print("y_test_c:", y_test_c.shape)

else:
    print("Neither 'class' column found in dff nor 'Class' column found in dfc. Cannot perform train-test split.")


def train_model_log_reg():
    print("Training Logistic Regression Model...")
    log_reg_model = LogisticRegression(solver='liblinear', random_state=42) # Using liblinear solver for smaller datasets
    log_reg_model.fit(X_train_resampled, y_train_resampled) # type: ignore
    print("Logistic Regression Model trained.")

def train_model_rf():
    print("\nTraining Random Forest Model...")
    # You can adjust n_estimators, max_depth, etc. for tuning
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_resampled, y_train_resampled) # type: ignore
    print("Random Forest Model trained.")

def evaluate_log_reg(log_reg_model):
    
# Apply the same one-hot encoding and column dropping as done for X_train before SMOTE
    categorical_features = X.select_dtypes(include=['object']).columns # Assuming X is the original features df before split
    X_test_processed = pd.get_dummies(X_test.copy(), columns=categorical_features, drop_first=True) # type: ignore

    # Drop the same columns that were dropped from X_train before SMOTE
    columns_to_drop = ['signup_time', 'purchase_time', 'ip_address', 'ip_address_int', 'time_since_signup_bin']
    X_test_processed = X_test_processed.drop(columns_to_drop, axis=1, errors='ignore')

    # Align columns - this is crucial if the test set has categories not present in the training set (or vice versa)
    # Reindex X_test_processed to match the columns of X_train_resampled, filling missing values with 0
    X_test_processed = X_test_processed.reindex(columns=X_train_resampled.columns, fill_value=0) # type: ignore


    y_pred_log_reg = log_reg_model.predict(X_test_processed)
    y_prob_log_reg = log_reg_model.predict_proba(X_test_processed)[:, 1] # Probability of the positive class

    print("\n--- Logistic Regression Model Evaluation ---")
    print("Classification Report:")
    print(classification_report(y_test, y_pred_log_reg))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred_log_reg))

    roc_auc_log_reg = roc_auc_score(y_test, y_prob_log_reg)
    print(f"\nROC AUC Score: {roc_auc_log_reg:.4f}")

    # Plot ROC curve for Logistic Regression
    fpr_log_reg, tpr_log_reg, thresholds_log_reg = roc_curve(y_test, y_prob_log_reg)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr_log_reg, tpr_log_reg, label=f'Logistic Regression (AUC = {roc_auc_log_reg:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.show()

def evaluate_rand_for(rf_model):
    
# Apply the     same one-hot encoding and column dropping as done for X_train before SMOTE
    categorical_features = X.select_dtypes(include=['object']).columns # Assuming X is the original features df before split
    X_test_processed = pd.get_dummies(X_test.copy(), columns=categorical_features, drop_first=True) # type: ignore

    # Drop the same columns that were dropped from X_train before SMOTE
    columns_to_drop = ['signup_time', 'purchase_time', 'ip_address', 'ip_address_int', 'time_since_signup_bin']
    X_test_processed = X_test_processed.drop(columns_to_drop, axis=1, errors='ignore')

    # Reindex X_test_processed to match the columns of X_train_resampled, filling missing values with 0
    X_test_processed = X_test_processed.reindex(columns=X_train_resampled.columns, fill_value=0) # type: ignore


    y_pred_rf = rf_model.predict(X_test_processed)
    y_prob_rf = rf_model.predict_proba(X_test_processed)[:, 1] # Probability of the positive class

    print("\n--- Random Forest Model Evaluation ---")
    print("Classification Report:")
    print(classification_report(y_test, y_pred_rf))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred_rf))

    roc_auc_rf = roc_auc_score(y_test, y_prob_rf)
    print(f"\nROC AUC Score: {roc_auc_rf:.4f}")

    # Plot ROC curve for Random Forest
    fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, y_prob_rf)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {roc_auc_rf:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Guessing')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend()
    plt.show()



if "__name__"=="_main__":
    log_reg_model = train_model_log_reg()
    rf_model = train_model_rf()
    evaluate_log_reg(log_reg_model)
    evaluate_rand_for(rf_model)