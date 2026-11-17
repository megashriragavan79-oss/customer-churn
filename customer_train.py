import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ---------------------------
# 1. LOAD DATASET
# ---------------------------

DATA_PATH = Path("../Dataset/customer-churn-training.csv")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        "Dataset not found. Place customer-churn-training.csv "
        "in the same folder as this script or update DATA_PATH."
    )

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("CUSTOMER CHURN PREDICTION")
print("=" * 60)
print("\nDataset shape:", df.shape)
print("\nFirst five records:")
print(df.head())
print("\nDataset information:")
df.info()

# ---------------------------
# 2. DATA VALIDATION
# ---------------------------

TARGET = "churned"
ID_COLUMNS = ["customer_id"]

if TARGET not in df.columns:
    raise ValueError(f"Target column '{TARGET}' was not found.")

if df[TARGET].isna().any():
    raise ValueError("Target column contains missing values.")

if not set(df[TARGET].unique()).issubset({0, 1}):
    raise ValueError("Target must contain only 0 and 1.")

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# Remove exact duplicate rows, if any.
df = df.drop_duplicates().copy()

# Remove rows with missing target (already validated above).
df = df.dropna(subset=[TARGET]).copy()
df[TARGET] = df[TARGET].astype(int)

print("\nTarget distribution:")
print(df[TARGET].value_counts().sort_index())
print("\nTarget percentage:")
print((df[TARGET].value_counts(normalize=True) * 100).round(2))

# ---------------------------
# 3. EXPLORATORY DATA ANALYSIS
# ---------------------------

print("\nDescriptive statistics:")
print(df.describe(include="all").T)

plt.figure(figsize=(6, 4))
sns.countplot(data=df, x=TARGET)
plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = Retained, 1 = Churned)")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()

numeric_for_eda = df.select_dtypes(include=np.number).columns.tolist()
numeric_for_eda = [c for c in numeric_for_eda if c not in ID_COLUMNS + [TARGET]]

for column in numeric_for_eda:
    plt.figure(figsize=(7, 4))
    sns.boxplot(data=df, x=TARGET, y=column)
    plt.title(f"{column} vs Churn")
    plt.tight_layout()
    plt.show()

categorical_for_eda = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()
categorical_for_eda = [c for c in categorical_for_eda if c not in ID_COLUMNS]

for column in categorical_for_eda:
    if column == TARGET:
        continue
    plt.figure(figsize=(7, 4))
    sns.countplot(data=df, x=column, hue=TARGET)
    plt.title(f"{column} vs Churn")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

# ---------------------------
# 4. FEATURE / TARGET SEPARATION
# ---------------------------

# Identifiers are excluded to prevent the model learning customer IDs.
drop_columns = [TARGET] + [c for c in ID_COLUMNS if c in df.columns]

X = df.drop(columns=drop_columns)
y = df[TARGET]

if X.shape[1] == 0:
    raise ValueError("No predictor columns remain after removing target/ID.")

numeric_features = X.select_dtypes(include=np.number).columns.tolist()
categorical_features = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nNumeric features:", numeric_features)
print("Categorical features:", categorical_features)

# ---------------------------
# 5. TRAIN / TEST SPLIT
# ---------------------------

# Stratification keeps both target classes represented in train/test,
# where the dataset size permits it.
class_counts = y.value_counts()

if len(class_counts) != 2 or class_counts.min() < 2:
    raise ValueError(
        "Not enough examples in each class for a stratified train/test split."
    )

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# ---------------------------
# 6. DATA PREPROCESSING
# ---------------------------

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_transformer, numeric_features),
        ("categorical", categorical_transformer, categorical_features)
    ],
    remainder="drop"
)

# ---------------------------
# 7. MODEL DEFINITIONS
# ---------------------------

models = {
    "Majority Class Baseline": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=3,
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=3,
        random_state=42
    )
}

# ---------------------------
# 8. MODEL TRAINING & EVALUATION
# ---------------------------

results = []
trained_models = {}

for model_name, estimator in models.items():

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", estimator)
    ])

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    if hasattr(pipeline, "predict_proba") and y_test.nunique() == 2:
        probabilities = pipeline.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, probabilities)
    else:
        roc_auc = np.nan

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC AUC": roc_auc
    })

    trained_models[model_name] = pipeline

    print("\n" + "-" * 60)
    print(model_name)
    print("-" * 60)
    print(classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Retained", "Churned"],
        zero_division=0
    ))

results_df = pd.DataFrame(results)
print("\nMODEL COMPARISON")
print(results_df.round(3).to_string(index=False))

results_df.to_csv("model_comparison_results.csv", index=False)

# ---------------------------
# 9. CONFUSION MATRIX
# ---------------------------

# Logistic Regression is selected as the simple, interpretable
# demonstration model before looking at the test results.
final_model_name = "Logistic Regression"
final_model = trained_models[final_model_name]

final_predictions = final_model.predict(X_test)

cm = confusion_matrix(y_test, final_predictions, labels=[0, 1])

plt.figure(figsize=(6, 4))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Retained", "Churned"],
    yticklabels=["Retained", "Churned"]
)
plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

print("\nFinal model:", final_model_name)
print("\nFinal model classification report:")
print(classification_report(
    y_test,
    final_predictions,
    labels=[0, 1],
    target_names=["Retained", "Churned"],
    zero_division=0
))

# ---------------------------
# 10. SAVE TRAINED MODEL
# ---------------------------

joblib.dump(final_model, "customer_churn_model.joblib")
print("\nModel saved as customer_churn_model.joblib")

# ---------------------------
# 11. PREDICT ON NEW CUSTOMER DATA
# ---------------------------

# Example customer. Replace values with a real, valid record.
# Do not include customer_id because it is not a model feature.
new_customer = pd.DataFrame([{
    "tenure_months": 5,
    "support_tickets": 3,
    "monthly_spend_inr": 799,
    "last_login_days": 15,
    "plan_type": "Basic"
}])

# Keep exactly the feature columns used during training.
new_customer = new_customer.reindex(columns=X.columns)

loaded_model = joblib.load("customer_churn_model.joblib")

new_prediction = loaded_model.predict(new_customer)[0]
new_probability = loaded_model.predict_proba(new_customer)[0][1]

print("\nNEW CUSTOMER PREDICTION")
print("Prediction:", "Churn" if new_prediction == 1 else "Retained")
print("Estimated churn probability:", round(float(new_probability) * 100, 2), "%")

# ---------------------------
# 12. FINAL PROJECT SUMMARY
# ---------------------------

print("\n" + "=" * 60)
print("PROJECT SUMMARY")
print("=" * 60)
print("Dataset records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Predictor features:", list(X.columns))
print("Selected demonstration model:", final_model_name)
print("Target: churned (0 = Retained, 1 = Churned)")
print("\nGenerated files:")
print("1. customer_churn_model.joblib")
print("2. model_comparison_results.csv")
print("\nIMPORTANT:")
print(
    "This supplied dataset contains only 12 records. "
    "The test metrics are highly unstable and must not be treated "
    "as evidence of production performance. The model is for "
    "educational/submission demonstration only."
)
print("=" * 60)
