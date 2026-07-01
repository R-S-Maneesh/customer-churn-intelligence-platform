# Project Documentation

## Overall Workflow

The application starts on the workspace initialization page in `app.py`. A user uploads a CSV file, the app validates the schema, stores the uploaded dataframe in Streamlit session state, and waits for the user to launch the dashboard. Launching the dashboard runs the full analytics pipeline for the active dataset.

The production workflow is:

```text
Upload CSV
  -> validate_enterprise_dataset()
  -> run_ingestion_pipeline()
  -> train_and_evaluate_models()
  -> generate_insights()
  -> executive report generation
  -> dashboard pages read current outputs
```

## Folder Structure

```text
data/
  Source and sample CSV datasets.

models/
  Current production model and scaler:
  - logistic_model_vB.pkl
  - scaler_vB.pkl

outputs/
  Generated analytics reports consumed by the dashboard.

outputs/images/
  Regenerated model evaluation charts:
  - roc_curve_comparison.png
  - feature_importance.png
  - confusion_matrix_logistic_regression.png
  - confusion_matrix_decision_tree.png
  - confusion_matrix_random_forest.png
```

## Pipeline

### 1. Upload And Validation

`app.py` handles the Streamlit upload widget and validates required columns through `validate_enterprise_dataset()`. The accepted schema contains 11 mandatory fields and an optional `customerID`.

### 2. Dataset Fingerprinting

The uploaded file bytes are hashed with SHA-256. The fingerprint is stored in `st.session_state["active_dataset_info"]` and in `outputs/pipeline_manifest.json` after successful generation. If the same dataset is launched again and all required artifacts exist, the pipeline reuses the existing artifacts. If the dataset changes, all generated model/report artifacts are rebuilt.

### 3. Cleaning

`data_cleaning.py` normalizes raw CRM-style exports:

- drops `customerID` before modeling
- removes duplicate rows
- trims selected categorical fields
- normalizes `Contract`, `InternetService`, yes/no, and churn values
- converts `TotalCharges` to numeric
- filters invalid tenure and monthly charge values
- imputes missing numeric values

### 4. Training And Evaluation

`model_comparison.py` owns the training pipeline. `train_and_evaluate_models()` accepts either a dataframe or CSV path, cleans it, encodes categorical variables, splits the data, scales numeric fields, trains all supported models, writes `outputs/model_comparison.csv`, regenerates all model images, and saves the production Logistic Regression model and scaler.

### 5. Customer Scoring

`business_intelligence.py` loads the current model artifacts from `models/`, prepares the cleaned data with the exact expected feature columns, applies scaling, and generates churn probabilities. It adds:

- `Churn_Probability`
- `Risk_Score`
- `Risk_Category`
- `Churn_Driver_Explanation`
- `Retention_Recommendation`

### 6. Reporting

`executive_reporting.py` generates:

- executive summary metrics
- risk distribution
- top 20 highest-risk targets
- model health report
- churn insight narrative

The app also regenerates `outputs/scenario_simulation_report.csv` from the current dataset's highest-risk profile.

## Module Communication

- `app.py` orchestrates upload, pipeline execution, and dashboard rendering.
- `model_comparison.py` produces model artifacts, model metrics, and model images.
- `business_intelligence.py` consumes the current model artifacts and produces customer-level risk reports.
- `executive_reporting.py` consumes the risk report and model comparison output to produce executive summaries.
- `scenario_simulator.py` consumes the current model and scaler to simulate customer intervention scenarios.

## Where Models Are Trained

Models are trained in `model_comparison.py` by `train_and_evaluate_models()`. The app calls this function during `run_ingestion_pipeline()` whenever a new uploaded dataset is detected.

## Where Reports Are Generated

Reports are generated in:

- `business_intelligence.export_reports()`
- `executive_reporting.generate_executive_summary()`
- `executive_reporting.generate_model_health()`
- `executive_reporting.generate_top_risk_targets()`
- `executive_reporting.generate_risk_distribution()`
- `executive_reporting.generate_churn_insights()`
- `app._export_current_scenario_report()`

## Where Dashboards Obtain Data

Dashboard pages in `app.py` read CSV reports and image files from `outputs/` and `outputs/images/`. These artifacts are regenerated during upload pipeline execution so the displayed analytics correspond to the current uploaded dataset.

## Current Dataset Guarantee

For every changed upload, the pipeline removes previously generated model/report artifacts, retrains models, regenerates evaluation images, recreates reports, and writes a fresh manifest. This prevents stale PNGs, cached metrics, or old model outputs from appearing in the submitted dashboard.
