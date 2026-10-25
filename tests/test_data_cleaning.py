import pandas as pd
from data_cleaning import clean_data

def sample_df():
    return pd.DataFrame({
        "customerID": ["C001", "C002"],
        "gender": [" Female ", "Male"],
        "SeniorCitizen": [0, 0],
        "tenure": [12, 24],
        "PhoneService": [" Yes ", "No"],
        "InternetService": ["DSL", "fibre optic"],
        "Contract": ["Month-to-month", "One year"],
        "PaperlessBilling": [" yes ", "no"],
        "PaymentMethod": [
            " Credit card (automatic) ",
            "Electronic check",
        ],
        "MonthlyCharges": [70.0, 80.0],
        "TotalCharges": ["840.0", "1920.0"],
        "Churn": [" Yes ", "No"],
    })


def test_removes_customer_id():
    result = clean_data(sample_df())
    assert "customerID" not in result.columns


def test_removes_duplicate_rows():
    row = sample_df().iloc[[0]]
    data = pd.concat([row, row], ignore_index=True)
    result = clean_data(data)
    assert len(result) == 1


def test_standardizes_categorical_values():
    result = clean_data(sample_df())
    assert result.loc[0, "gender"] == "Female"
    assert result.loc[0, "PaymentMethod"] == "Credit card (automatic)"
    assert result.loc[0, "Churn"] == "Yes"
    assert result.loc[0, "PhoneService"] == "Yes"
    assert result.loc[0, "PaperlessBilling"] == "Yes"


def test_normalizes_contract_values():
    data = sample_df()
    data["Contract"] = ["month to month", "1 year"]
    result = clean_data(data)
    assert result["Contract"].tolist() == [
        "Month-to-month", "One year"
    ]


def test_normalizes_internet_service_values():
    data = sample_df()
    data["InternetService"] = ["fibre optic", "none"]
    result = clean_data(data)
    assert result["InternetService"].tolist() == [
        "Fiber optic", "No"
    ]


def test_converts_and_imputes_invalid_total_charges():
    data = sample_df()
    data["TotalCharges"] = ["100", "invalid"]
    result = clean_data(data)
    assert pd.api.types.is_numeric_dtype(result["TotalCharges"])
    assert result["TotalCharges"].tolist() == [100.0, 100.0]


def test_removes_zero_tenure_rows():
    data = sample_df()
    data["tenure"] = [0, 24]
    result = clean_data(data)
    assert result["tenure"].tolist() == [24]


def test_removes_monthly_charge_outliers():
    data = pd.concat(
        [sample_df(), sample_df().iloc[[0]]],
        ignore_index=True,
    )
    data["MonthlyCharges"] = [9.0, 70.0, 250.0]
    data["tenure"] = [12, 24, 36]
    data["TotalCharges"] = ["108", "1680", "9000"]

    result = clean_data(data)
    assert len(result) == 1
    assert result["tenure"].tolist() == [24]


def test_imputes_missing_numeric_and_internet_values():
    data = sample_df()
    data["MonthlyCharges"] = [None, 80.0]
    data["TotalCharges"] = [None, "1920"]
    data["tenure"] = [None, 24]
    data["InternetService"] = [None, "DSL"]

    result = clean_data(data)

    assert result[
        ["MonthlyCharges", "TotalCharges", "tenure", "InternetService"]
    ].notna().all().all()
    assert result.loc[0, "MonthlyCharges"] == 80.0
    assert result.loc[0, "TotalCharges"] == 1920.0
    assert result.loc[0, "tenure"] == 24
    assert result.loc[0, "InternetService"] == "DSL"
