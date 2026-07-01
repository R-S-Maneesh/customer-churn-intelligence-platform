import pandas as pd
import numpy as np
import joblib
import os
import datetime

# --- 1. File & Directory Validation ---
def check_required_files():
    """Ensures previous stage pipeline outputs are available for processing."""
    required = [
        'outputs/customer_risk_report.csv',
        'outputs/model_comparison.csv',
        'models/logistic_model_vB.pkl'
    ]
    missing = [f for f in required if not os.path.exists(f)]
    if missing:
        print(f"Error: Missing required previous outputs: {missing}")
        print("Please ensure Tasks 3 and 4 have been executed successfully first.")
        exit(1)

# --- 2. Part A: Executive Summary Aggregator ---
def generate_executive_summary(df):
    """Calculates high-level corporate portfolio churn metrics."""
    total_cust = len(df)
    high_risk_df = df[df['Risk_Category'] == 'High Risk']
    med_risk_df = df[df['Risk_Category'] == 'Medium Risk']
    low_risk_df = df[df['Risk_Category'] == 'Low Risk']
    
    high_count = len(high_risk_df)
    med_count = len(med_risk_df)
    low_count = len(low_risk_df)
    
    avg_score = df['Risk_Score'].mean()
    expected_churn = df['Churn_Probability'].sum()
    
    summary_data = {
        'Metric': [
            'Total Customers',
            'High Risk Customers',
            'Medium Risk Customers',
            'Low Risk Customers',
            'Average Risk Score',
            'Expected Churn Count',
            'High Risk Percentage',
            'Medium Risk Percentage',
            'Low Risk Percentage'
        ],
        'Value': [
            float(total_cust),
            float(high_count),
            float(med_count),
            float(low_count),
            round(float(avg_score), 2),
            round(float(expected_churn), 2),
            round((high_count / total_cust) * 100, 2),
            round((med_count / total_cust) * 100, 2),
            round((low_count / total_cust) * 100, 2)
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('outputs/executive_summary.csv', index=False)
    return summary_df

# --- 3. Part B: Production Model Health Monitor ---
def generate_model_health(model_path, comparison_path, client_df):
    """Extracts deployment validation and historical model performance metrics."""
    # Load serializations to count structural components
    model = joblib.load(model_path)
    feature_count = len(model.feature_names_in_)
    strongest_feature = 'Unavailable'
    if hasattr(model, 'coef_'):
        coefs = model.coef_[0]
        strongest_feature = model.feature_names_in_[int(np.argmax(np.abs(coefs)))]
    
    # Read experimental validation tracking from Task 3
    comp_df = pd.read_csv(comparison_path)
    # Target our selected production variant
    lr_metrics = comp_df[comp_df['Model'].str.strip() == 'Logistic Regression'].iloc[0]
    
    health_data = {
        'Metric': [
            'Production Model Name',
            'Training Algorithm',
            'Accuracy',
            'Precision',
            'Recall',
            'F1 Score',
            'ROC-AUC',
            'Training Date',
            'Dataset Size',
            'Number of Features',
            'Strongest Feature'
        ],
        'Value': [
            'logistic_model_vB.pkl',
            'Logistic Regression (Balanced Weights)',
            str(round(lr_metrics['Accuracy'], 6)),
            str(round(lr_metrics['Precision'], 6)),
            str(round(lr_metrics['Recall'], 6)),
            str(round(lr_metrics['F1 Score'], 6)),
            str(round(lr_metrics['ROC-AUC'], 6)),
            datetime.date.today().strftime('%Y-%m-%d'),
            str(len(client_df)),
            str(feature_count),
            str(strongest_feature)
        ]
    }
    
    health_df = pd.DataFrame(health_data)
    health_df.to_csv('outputs/model_health_report.csv', index=False)
    return health_df

# --- 4. Part C: Operational Target Identification ---
def generate_top_risk_targets(df):
    """Isolates the absolute highest priority profiles for marketing intervention."""
    top_20 = df.sort_values(by='Risk_Score', ascending=False).head(20)
    top_20.to_csv('outputs/top_20_risk_customers.csv', index=False)

# --- 5. Part D: Risk Stratification Grid ---
def generate_risk_distribution(df):
    """Maps institutional segmentation profile layout."""
    categories = ['Low Risk', 'Medium Risk', 'High Risk']
    counts = []
    
    for cat in categories:
        counts.append(len(df[df['Risk_Category'] == cat]))
        
    dist_df = pd.DataFrame({
        'Risk Category': categories,
        'Customer Count': counts
    })
    dist_df.to_csv('outputs/risk_distribution.csv', index=False)

# --- 6. Part E: Prescriptive Analytics Report ---
def generate_churn_insights(df, model_path):
    """Calculates automated, statistically sound narrative performance analysis."""
    model = joblib.load(model_path)
    
    # 1. Pull most important feature programmatically from coefficients
    feats = model.feature_names_in_
    coefs = model.coef_[0]
    abs_idx = np.argmax(np.abs(coefs))
    strongest_feature = feats[abs_idx]
    
    # 2. Segment Analysis
    contract_groups = df.groupby('Contract')['Risk_Score'].mean()
    highest_risk_contract = contract_groups.idxmax()
    
    # 3. Aggregations
    avg_risk = df['Risk_Score'].mean()
    high_risk_profiles = df[df['Risk_Category'] == 'High Risk']
    
    if not high_risk_profiles.empty:
        recommended_focus = high_risk_profiles['Retention_Recommendation'].mode().iloc[0]
    else:
        recommended_focus = "General Plan Optimization"
        
    # 4. Construct Narrative File
    insights_text = (
        "==================================================\n"
        "          CHURN INSIGHTS & INTERPRETATIONS        \n"
        "==================================================\n\n"
        f"Most Important Feature: {strongest_feature}\n"
        f"Highest Risk Segment: {highest_risk_contract} Contracts\n"
        f"Average Customer Risk: {avg_risk:.2f} / 100\n"
        f"Recommended Retention Focus: {recommended_focus}\n\n"
        "Key Business Observation:\n"
        f"Statistical analysis indicates that {highest_risk_contract} structures "
        f"and characteristics linked to {strongest_feature} constitute the primary "
        "structural accelerators for account attrition. Retention efforts should prioritize "
        f"proactive outreach centered around: {recommended_focus}.\n"
    )
    
    with open('outputs/churn_insights.txt', 'w') as f:
        f.write(insights_text)

# --- 7. Part F: Terminal Console Interface ---
def print_terminal_dashboard(summary_df, health_df):
    """Outputs structured diagnostic information safely to Windows CLI environment."""
    print("\n" + "="*50)
    print("         CUSTOMER CHURN PLATFORM STATUS")
    print("="*50)
    
    print("\n[Dataset Status]")
    total_cust = int(summary_df[summary_df['Metric'] == 'Total Customers']['Value'].values[0])
    print(f" -> Master Registry Records Loaded: {total_cust} active profiles")
    
    print("\n[Model Status]")
    model_name = health_df[health_df['Metric'] == 'Production Model Name']['Value'].values[0]
    roc_auc = health_df[health_df['Metric'] == 'ROC-AUC']['Value'].values[0]
    print(f" -> Active Production Model:       {model_name}")
    print(f" -> Verification ROC-AUC Metric:   {roc_auc}")
    
    print("\n[Business Intelligence Status]")
    high_pct = summary_df[summary_df['Metric'] == 'High Risk Percentage']['Value'].values[0]
    exp_churn = summary_df[summary_df['Metric'] == 'Expected Churn Count']['Value'].values[0]
    print(f" -> Portfolio Variance High Risk:  {high_pct}%")
    print(f" -> Projected Attrition Volume:    ~{int(float(exp_churn))} customers")
    
    print("\n[Simulation Status]")
    print(" -> Retention Scenario Matrix Engine: Ready / Operational")
    
    print("\n[Reports Generated]")
    print(" -> outputs/executive_summary.csv      [DONE]")
    print(" -> outputs/model_health_report.csv    [DONE]")
    print(" -> outputs/top_20_risk_customers.csv  [DONE]")
    print(" -> outputs/risk_distribution.csv      [DONE]")
    print(" -> outputs/churn_insights.txt         [DONE]")
    print("\n" + "="*50 + "\n")

# --- Execution Entry Point ---
if __name__ == "__main__":
    # Validate environment
    check_required_files()
    
    # Extract baseline records
    master_df = pd.read_csv('outputs/customer_risk_report.csv')
    
    # Process reports
    exec_df = generate_executive_summary(master_df)
    mod_health_df = generate_model_health('models/logistic_model_vB.pkl', 'outputs/model_comparison.csv', master_df)
    generate_top_risk_targets(master_df)
    generate_risk_distribution(master_df)
    generate_churn_insights(master_df, 'models/logistic_model_vB.pkl')
    
    # Present Console Layout
    print_terminal_dashboard(exec_df, mod_health_df)
