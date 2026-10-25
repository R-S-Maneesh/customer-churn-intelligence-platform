
"""Unit tests for API validation and prediction preprocessing."""

import pytest
from pydantic import ValidationError

import api


VALID_CUSTOMER = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "tenure": 24,
    "PhoneService": "Yes",
    "InternetService": "Fiber optic",
    "Contract": "One year",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.0,
}

EXPECTED_FEATURES = api.FALLBACK_FEATURE_NAMES.copy()


class FakeScaler:
    def __init__(self):
        self.seen_columns = None

    def transform(self, frame):
        self.seen_columns = list(frame.columns)
        return frame.to_numpy(dtype=float)


class FakeModel:
    classes_ = [0, 1]

    def __init__(self):
        self.seen_features = None

    def predict_proba(self, frame):
        self.seen_features = frame.copy()
        return [[0.25, 0.75]]

    def predict(self, frame):
        self.seen_features = frame.copy()
        return [1]


def test_predict_encodes_one_customer_and_aligns_training_features(
    monkeypatch,
):
    model = FakeModel()
    scaler = FakeScaler()

    monkeypatch.setattr(
        api,
        "_load_artifacts",
        lambda: (model, scaler, EXPECTED_FEATURES.copy()),
    )

    response = api.predict_churn(
        api.CustomerFeatures(**VALID_CUSTOMER)
    )

    assert response.predicted_churn == "Yes"
    assert response.churn_probability == 0.75
    assert response.model_name == "Logistic Regression"

    assert list(model.seen_features.columns) == EXPECTED_FEATURES
    assert scaler.seen_columns == ["tenure", "MonthlyCharges"]

    assert model.seen_features.loc[0, "gender_Male"] == 1.0
    assert model.seen_features.loc[0, "PhoneService_Yes"] == 1.0
    assert model.seen_features.loc[
        0, "InternetService_Fiber optic"
    ] == 1.0
    assert model.seen_features.loc[0, "Contract_One year"] == 1.0
    assert model.seen_features.loc[
        0, "PaymentMethod_Electronic check"
    ] == 1.0


def test_validation_rejects_out_of_range_tenure():
    invalid_customer = {
        **VALID_CUSTOMER,
        "tenure": 0,
    }

    with pytest.raises(ValidationError):
        api.CustomerFeatures(**invalid_customer)


def test_validation_rejects_unknown_fields():
    invalid_customer = {
        **VALID_CUSTOMER,
        "customerID": "C0001",
    }

    with pytest.raises(ValidationError):
        api.CustomerFeatures(**invalid_customer)


def test_committed_model_artifacts_can_score_a_customer():
    """Test actual saved artifacts when they exist in the repository."""
    if not api.MODEL_PATH.is_file() or not api.SCALER_PATH.is_file():
        pytest.skip(
            "Committed model artifacts are not present in this checkout."
        )

    model, scaler, feature_names = api._load_artifacts()

    features = api._build_model_input(
        api.CustomerFeatures(**VALID_CUSTOMER),
        scaler,
        feature_names,
    )

    assert list(features.columns) == feature_names

    probabilities = model.predict_proba(features)[0]

    assert len(probabilities) == len(model.classes_)
    assert all(
        0.0 <= float(value) <= 1.0
        for value in probabilities
    )
    assert sum(float(value) for value in probabilities) == pytest.approx(
        1.0,
        abs=1e-6,
    )
