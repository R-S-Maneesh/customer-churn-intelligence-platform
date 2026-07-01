import os

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from data_cleaning import clean_data

CAT_COLS = [
    "gender",
    "PhoneService",
    "InternetService",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
NUM_COLS = ["tenure", "MonthlyCharges"]
PRODUCTION_MODEL_NAME = "Logistic Regression"


def _load_input(input_data):
    if isinstance(input_data, pd.DataFrame):
        return input_data.copy()
    return pd.read_csv(input_data)


def prepare_training_frame(input_data):
    """Clean and encode the active dataset for model training."""
    raw_data = _load_input(input_data)
    df = clean_data(raw_data)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.dropna(subset=["Churn"])

    if df["Churn"].nunique() < 2:
        raise ValueError("Model training requires both churn classes: Yes and No.")

    df = pd.get_dummies(df, columns=CAT_COLS, drop_first=True)
    X = df.drop(columns=["Churn", "TotalCharges"])
    y = df["Churn"].astype(int)
    return X, y


def _split_data(X, y):
    class_counts = y.value_counts()
    stratify = y if class_counts.min() >= 2 else None
    return train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )


def _scale_numeric_columns(X_train, X_test):
    scaler = StandardScaler()
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
    X_test[NUM_COLS] = scaler.transform(X_test[NUM_COLS])
    return X_train, X_test, scaler


def _scale_full_dataset(X):
    scaler = StandardScaler()
    X_scaled = X.copy()
    X_scaled[NUM_COLS] = scaler.fit_transform(X_scaled[NUM_COLS])
    return X_scaled, scaler


def _build_models():
    return {
        "Logistic Regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        ),
        "Decision Tree": DecisionTreeClassifier(
            class_weight="balanced",
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    }


def _clear_generated_images(image_dir):
    os.makedirs(image_dir, exist_ok=True)
    generated_names = [
        "roc_curve_comparison.png",
        "feature_importance.png",
        "confusion_matrix_logistic_regression.png",
        "confusion_matrix_decision_tree.png",
        "confusion_matrix_random_forest.png",
    ]
    for name in generated_names:
        path = os.path.join(image_dir, name)
        if os.path.exists(path):
            os.remove(path)


def _save_confusion_matrix(model_name, y_true, y_pred, image_dir):
    matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Stay", "Churn"],
        yticklabels=["Stay", "Churn"],
    )
    plt.title(f"Confusion Matrix - {model_name}")
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    filename = model_name.lower().replace(" ", "_")
    plt.savefig(
        os.path.join(image_dir, f"confusion_matrix_{filename}.png"),
        bbox_inches="tight",
        dpi=140,
    )
    plt.close()


def _save_roc_curve(models, X_test, y_test, image_dir):
    plt.figure(figsize=(8, 6))
    for name, model in models.items():
        y_prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        auc_score = roc_auc_score(y_test, y_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_score:.3f})")

    plt.plot([0, 1], [0, 1], "k--", label="Random Guessing")
    plt.title("ROC Curve Comparison")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.savefig(
        os.path.join(image_dir, "roc_curve_comparison.png"),
        bbox_inches="tight",
        dpi=140,
    )
    plt.close()


def _save_feature_importance(model, feature_names, image_dir):
    feature_df = pd.DataFrame(
        {"Feature": feature_names, "Importance": model.feature_importances_}
    ).sort_values(by="Importance", ascending=False)
    feature_df = feature_df.head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="Importance",
        y="Feature",
        data=feature_df,
        hue="Feature",
        palette="viridis",
        legend=False,
    )
    plt.title("Top 10 Most Important Features (Random Forest)")
    plt.xlabel("Relative Importance")
    plt.ylabel("Feature")
    plt.savefig(
        os.path.join(image_dir, "feature_importance.png"),
        bbox_inches="tight",
        dpi=140,
    )
    plt.close()


def _save_production_artifacts(X, y, model_dir):
    os.makedirs(model_dir, exist_ok=True)
    X_scaled, scaler = _scale_full_dataset(X)
    model = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    model.fit(X_scaled, y)
    joblib.dump(model, os.path.join(model_dir, "logistic_model_vB.pkl"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler_vB.pkl"))
    return model, scaler


def train_and_evaluate_models(
    input_data,
    output_dir="outputs",
    image_dir="outputs/images",
    model_dir="models",
):
    """
    Retrain all dashboard models from the active dataset and regenerate metrics,
    images, and production model artifacts.
    """
    os.makedirs(output_dir, exist_ok=True)
    _clear_generated_images(image_dir)

    X, y = prepare_training_frame(input_data)
    X_train, X_test, y_train, y_test = _split_data(X, y)
    X_train, X_test, _ = _scale_numeric_columns(X_train, X_test)

    models = _build_models()
    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        results.append(
            {
                "Model": name,
                "Accuracy": accuracy_score(y_test, y_pred),
                "Precision": precision_score(y_test, y_pred, zero_division=0),
                "Recall": recall_score(y_test, y_pred, zero_division=0),
                "F1 Score": f1_score(y_test, y_pred, zero_division=0),
                "ROC-AUC": roc_auc_score(y_test, y_prob),
            }
        )
        _save_confusion_matrix(name, y_test, y_pred, image_dir)

    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(output_dir, "model_comparison.csv"), index=False)

    _save_roc_curve(models, X_test, y_test, image_dir)
    _save_feature_importance(models["Random Forest"], X.columns, image_dir)
    production_model, production_scaler = _save_production_artifacts(X, y, model_dir)

    return {
        "comparison": results_df,
        "production_model": production_model,
        "production_scaler": production_scaler,
        "feature_count": len(X.columns),
        "training_rows": len(X),
    }


if __name__ == "__main__":
    print("Loading, training, and regenerating model analytics...")
    training_summary = train_and_evaluate_models("data/churnguard_data.csv")
    print("\n--- Model Comparison Table ---")
    print(training_summary["comparison"].to_string(index=False))
    print("\nSuccess! Model artifacts, metrics, and images were regenerated.")
