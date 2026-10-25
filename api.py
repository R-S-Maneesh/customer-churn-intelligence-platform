
"""FastAPI inference API for the existing churn Logistic Regression model."""

from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "logistic_model_vB.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler_vB.pkl"

# Match the categorical columns and category order used during training.
CATEGORICAL_LEVELS: dict[str, tuple[str, ...]] = {
    "gender": ("Female", "Male"),
    "PhoneService": ("No", "Yes"),
    "InternetService": ("DSL", "Fiber optic", "No"),
    "Contract": ("Month-to-month", "One year", "Two year"),
    "PaperlessBilling": ("No", "Yes"),
    "PaymentMethod": (
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ),
}

CATEGORICAL_COLUMNS = list(CATEGORICAL_LEVELS)
NUMERIC_COLUMNS = ["tenure", "MonthlyCharges"]

# Compatibility fallback for older models without feature_names_in_.
# pandas places the non-categorical columns first when the training code
# calls get_dummies(..., columns=CAT_COLS, drop_first=True).
FALLBACK_FEATURE_NAMES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "gender_Male",
    "PhoneService_Yes",
    "InternetService_Fiber optic",
    "InternetService_No",
    "Contract_One year",
    "Contract_Two year",
    "PaperlessBilling_Yes",
    "PaymentMethod_Credit card (automatic)",
    "PaymentMethod_Electronic check",
    "PaymentMethod_Mailed check",
]


class CustomerFeatures(BaseModel):
    """Validated customer features used by the trained model.

    TotalCharges is intentionally omitted because the repository's training
    pipeline drops it before fitting the production model.
    """

    model_config = ConfigDict(extra="forbid")

    gender: Literal["Female", "Male"]
    SeniorCitizen: int = Field(strict=True, ge=0, le=1)
    tenure: int = Field(ge=1, le=72)
    PhoneService: Literal["No", "Yes"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["No", "Yes"]
    PaymentMethod: Literal[
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ]
    MonthlyCharges: float = Field(ge=10, le=200)


class PredictionResponse(BaseModel):
    predicted_churn: Literal["No", "Yes"]
    churn_probability: float = Field(ge=0.0, le=1.0)
    model_name: str


app = FastAPI(
    title="Customer Churn Prediction API",
    description=(
        "Serves predictions using the saved Logistic Regression model "
        "and its matching numeric scaler."
    ),
    version="1.0.0",
)


@lru_cache(maxsize=1)
def _load_artifacts() -> tuple[Any, Any, list[str]]:
    """Load the model once and verify its expected input schema."""
    missing = [
        str(path.relative_to(BASE_DIR))
        for path in (MODEL_PATH, SCALER_PATH)
        if not path.is_file()
    ]

    if missing:
        raise FileNotFoundError(
            f"Missing model artifact(s): {', '.join(missing)}. "
            "Generate them using the repository's training pipeline."
        )

    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
    except Exception as exc:
        raise RuntimeError(
            f"Could not load model artifacts ({type(exc).__name__}). "
            "Check that the saved artifacts and installed scikit-learn "
            "versions are compatible."
        ) from exc

    if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
        raise RuntimeError(
            "The saved model must support predict() and predict_proba()."
        )

    if not hasattr(model, "classes_"):
        raise RuntimeError("The saved model has no trained class labels.")

    if not hasattr(scaler, "transform"):
        raise RuntimeError("The saved scaler does not support transform().")

    saved_features = getattr(model, "feature_names_in_", None)

    if saved_features is not None:
        feature_names = [str(name) for name in saved_features]
    else:
        expected_count = getattr(model, "n_features_in_", None)

        if expected_count != len(FALLBACK_FEATURE_NAMES):
            raise RuntimeError(
                "The saved model's feature schema cannot be identified "
                "safely. Regenerate its artifacts using the repository's "
                "training code."
            )

        feature_names = FALLBACK_FEATURE_NAMES.copy()

    if not set(NUMERIC_COLUMNS).issubset(feature_names):
        raise RuntimeError(
            "The model schema must contain tenure and MonthlyCharges."
        )

    scaler_features = getattr(scaler, "feature_names_in_", None)

    if (
        scaler_features is not None
        and list(scaler_features) != NUMERIC_COLUMNS
    ):
        raise RuntimeError(
            "The scaler's input columns must be tenure and MonthlyCharges "
            "in that order."
        )

    return model, scaler, feature_names


def _build_model_input(
    customer: CustomerFeatures,
    scaler: Any,
    expected_features: list[str],
) -> pd.DataFrame:
    """Encode one customer using the training pipeline's conventions."""
    row = pd.DataFrame([customer.model_dump()])

    # Explicit categories are essential for single-row inference:
    # otherwise get_dummies could omit columns that the model expects.
    for column, levels in CATEGORICAL_LEVELS.items():
        row[column] = pd.Categorical(
            row[column],
            categories=list(levels),
        )

    encoded = pd.get_dummies(
        row,
        columns=CATEGORICAL_COLUMNS,
        drop_first=True,
        dtype=float,
    )

    # Match the exact feature names and order captured by the trained model.
    features = encoded.reindex(
        columns=expected_features,
        fill_value=0,
    ).astype(float)

    if not set(NUMERIC_COLUMNS).issubset(features.columns):
        raise RuntimeError(
            "The model schema is missing required numeric features."
        )

    features.loc[:, NUMERIC_COLUMNS] = scaler.transform(
        features[NUMERIC_COLUMNS]
    )

    return features


@app.get("/health")
def health() -> dict[str, Any]:
    """Report API liveness and whether model files are present."""
    model_ready = MODEL_PATH.is_file() and SCALER_PATH.is_file()

    return {
        "status": "ok" if model_ready else "degraded",
        "model_ready": model_ready,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerFeatures) -> PredictionResponse:
    """Return the predicted churn class and its estimated probability."""
    try:
        model, scaler, feature_names = _load_artifacts()

        features = _build_model_input(
            customer,
            scaler,
            feature_names,
        )

        classes = list(model.classes_)

        if 1 not in classes:
            raise RuntimeError(
                "The saved model does not contain the positive churn class 1."
            )

        positive_class_index = classes.index(1)

        churn_probability = float(
            model.predict_proba(features)[0][positive_class_index]
        )
        predicted_class = int(model.predict(features)[0])

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Prediction is unavailable because the saved model artifacts "
                f"could not be used ({type(exc).__name__}: {exc})."
            ),
        ) from exc

    return PredictionResponse(
        predicted_churn="Yes" if predicted_class == 1 else "No",
        churn_probability=round(churn_probability, 4),
        model_name="Logistic Regression",
    )
