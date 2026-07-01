# Customer Churn Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Customer Churn Intelligence Platform is a Streamlit analytics application for telecom churn prediction, portfolio risk monitoring, and retention strategy planning. It accepts a customer dataset, cleans and validates the data, retrains machine learning models, regenerates model analytics, scores customers, and produces executive-ready reports from the active uploaded dataset.

## Features

- Enterprise CSV upload with schema and data-quality validation.
- Data cleaning for common CRM export issues such as spacing, casing, missing values, and string-based charge fields.
- Automatic model retraining when a new dataset is uploaded.
- Model comparison across Logistic Regression, Decision Tree, and Random Forest.
- Regenerated ROC curve, feature importance, and confusion matrix image assets.
- Customer-level churn probability, risk scoring, churn drivers, and retention recommendations.
- Executive overview, customer intelligence, high-risk command center, scenario simulator, and insights dashboard pages.
- Exportable CSV reports for executive summary, customer risk, high-risk targets, top priority accounts, model health, and scenario simulations.

## Architecture

```text
CSV Upload
     │
     ▼
Validation
     │
     ▼
Data Cleaning
     │
     ▼
Model Training
     │
     ▼
Business Intelligence
     │
     ▼
Executive Reports
     │
     ▼
Interactive Dashboard
```

## Screenshots

Please refer to `screenshots` folder in the root directory


## Project Structure

```text
.
├── app.py
├── data_cleaning.py
├── model_comparison.py
├── train_models.py
├── business_intelligence.py
├── executive_reporting.py
├── scenario_simulator.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
├── data/
├── screenshots/
├── models/
└── outputs/
    └── images/
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Requirements

The project requires Python 3.10+ and the packages listed in `requirements.txt`.

## Running The Application

```bash
streamlit run app.py
```

Upload a valid telecom churn CSV on the initialization screen, wait for the analytics pipeline to complete, then launch the dashboard.

## Dataset Format

Required columns:

```text
gender, SeniorCitizen, tenure, PhoneService, InternetService, Contract,
PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn
```

Optional supported column:

```text
customerID
```

The application expects Telco-style values such as `Male/Female`, `Yes/No`, `DSL/Fiber optic/No`, `Month-to-month/One year/Two year`, and churn labels of `Yes` or `No`. Natural CRM export imperfections such as extra spaces, mixed capitalization, and string `TotalCharges` are handled by the cleaning pipeline.

## How Model Training Works

Each new uploaded dataset is fingerprinted. If the fingerprint is unchanged and all required artifacts exist, the app reuses the current artifacts. If the dataset changes, the app automatically:

1. Cleans the uploaded data.
2. Encodes categorical variables.
3. Splits the data into train/test partitions.
4. Trains Logistic Regression, Decision Tree, and Random Forest models.
5. Saves model comparison metrics to `outputs/model_comparison.csv`.
6. Regenerates ROC, feature importance, and confusion matrix PNGs in `outputs/images/`.
7. Saves the production Logistic Regression model and scaler in `models/`.

## Dashboard Explanation

- Executive Overview summarizes portfolio risk distribution and expected churn.
- Model Analytics displays model health, comparison metrics, ROC analysis, and feature importance from the current uploaded dataset.
- Customer Intelligence shows customer-level risk scores, drivers, and recommendations.
- High Risk Command Center focuses on the highest-priority retention targets.
- Insights Center provides strategic summaries and report downloads.

## Scenario Simulator

The Scenario Simulator estimates how contract changes, discounts, and tenure changes may affect churn risk for a selected customer profile. The pipeline also regenerates `outputs/scenario_simulation_report.csv` from the current dataset's highest-risk profile after each new upload.

## Report Generation

Generated reports are written to `outputs/`:

- `customer_risk_report.csv`
- `high_risk_customers.csv`
- `top_20_risk_customers.csv`
- `executive_summary.csv`
- `model_health_report.csv`
- `model_comparison.csv`
- `risk_distribution.csv`
- `scenario_simulation_report.csv`
- `churn_insights.txt`

## Technologies Used

- Streamlit
- pandas
- NumPy
- scikit-learn
- Plotly
- Matplotlib
- Seaborn
- Joblib

## Future Improvements

- Add authentication and role-based dashboard access.
- Persist model runs in a database-backed model registry.
- Add SHAP-based feature explanations.
- Add automated tests for upload, training, and report generation.
- Add cloud deployment configuration.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

Maneesh
