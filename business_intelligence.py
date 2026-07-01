import pandas as pd
import joblib
import os

# Import our custom cleaning function from Task 1
from data_cleaning import clean_data

# --- 1. Load the Production Artifacts ---
def load_artifacts():
    """Loads the saved model and scaler from Task 2."""
    try:
        model = joblib.load('models/logistic_model_vB.pkl')
        scaler = joblib.load('models/scaler_vB.pkl')
        return model, scaler
    except FileNotFoundError:
        print("Error: Could not find model files. Ensure you ran Task 2 first.")
        exit()

# --- 2. Feature Preparation ---
def prepare_features(df_clean, model):
    """
    Transforms the clean dataframe into the exact format the model expects.
    """
    # Dummy encode categorical variables
    cat_cols = ['gender', 'PhoneService', 'InternetService', 'Contract', 'PaperlessBilling', 'PaymentMethod']
    X = pd.get_dummies(df_clean, columns=cat_cols, drop_first=True)
    
    # Drop columns not used in Version B training
    cols_to_drop = ['Churn', 'TotalCharges']
    for c in cols_to_drop:
        if c in X.columns:
            X = X.drop(columns=[c])
            
    # CRITICAL FIX: Ensure the new data has the exact same columns as the training data
    # This prevents the script from crashing if a category is completely missing in new datasets.
    expected_columns = model.feature_names_in_
    X = X.reindex(columns=expected_columns, fill_value=0)
    
    return X

# --- 3. Business Logic Engine ---
def apply_business_rules(df):
    """
    Analyzes customer data and generates plain-English drivers and recommendations.
    """
    drivers = []
    recommendations = []
    
    for _, row in df.iterrows():
        driver_list = []
        rec_list = []
        
        # Rule 1: Contract Type
        if row['Contract'] == 'Month-to-month':
            driver_list.append("Month-to-Month Contract")
            rec_list.append("Offer Annual Contract")
        else:
            driver_list.append("Long-Term Contract")
            
        # Rule 2: Monthly Charges
        if row['MonthlyCharges'] >= 70:
            driver_list.append("High Monthly Charges")
            rec_list.append("Provide Loyalty Discount")
        elif row['MonthlyCharges'] <= 30:
            driver_list.append("Low Monthly Charges")
            
        # Rule 3: Tenure
        if row['tenure'] <= 12:
            driver_list.append("Short Customer Tenure")
            rec_list.append("Assign Retention Team")
            
        # Default recommendation if no specific flags are hit
        if not rec_list:
            rec_list.append("Offer Premium Support")
            
        # Join lists into readable strings
        drivers.append(" | ".join(driver_list))
        recommendations.append(" | ".join(rec_list))
        
    df['Churn_Driver_Explanation'] = drivers
    df['Retention_Recommendation'] = recommendations
    return df

# --- 4. The Core Pipeline ---
def generate_insights(input_data):
    """Runs the full end-to-end business intelligence pipeline.
    
    Args:
        input_data: Either a file path string (str) or a pandas DataFrame.
    """
    # Accept either a filepath or an in-memory DataFrame
    if isinstance(input_data, pd.DataFrame):
        raw_data = input_data.copy()
    else:
        raw_data = pd.read_csv(input_data)
    
    df_clean = clean_data(raw_data)
    
    # Load model and prepare features
    model, scaler = load_artifacts()
    X = prepare_features(df_clean, model)
    
    # Scale numeric features
    cols_to_scale = ['tenure', 'MonthlyCharges']
    X[cols_to_scale] = scaler.transform(X[cols_to_scale])
    
    # Predict Probabilities
    # predict_proba returns an array like [probability_stay, probability_churn]
    churn_probs = model.predict_proba(X)[:, 1] 
    
    # Build Business Dataframe
    business_df = df_clean.copy()
    business_df['Churn_Probability'] = churn_probs
    business_df['Risk_Score'] = (churn_probs * 100).round(1)
    
    # Categorize Risk
    def categorize_risk(score):
        if score >= 70: return 'High Risk'
        elif score >= 30: return 'Medium Risk'
        else: return 'Low Risk'
        
    business_df['Risk_Category'] = business_df['Risk_Score'].apply(categorize_risk)
    
    # Apply NLP/Business Rules
    business_df = apply_business_rules(business_df)
    
    return business_df


# --- 5. Executive Summary & Export ---
def print_executive_summary(df):
    """Generates a high-level summary for stakeholders."""
    total_customers = len(df)
    high_risk = len(df[df['Risk_Category'] == 'High Risk'])
    med_risk = len(df[df['Risk_Category'] == 'Medium Risk'])
    low_risk = len(df[df['Risk_Category'] == 'Low Risk'])
    avg_score = df['Risk_Score'].mean()
    expected_churn = int(df['Churn_Probability'].sum())
    
    print("\n" + "="*45)
    print(" EXECUTIVE SUMMARY: CHURN RISK REPORT") 
    print("="*45)
    print(f" Total Customers Analyzed:   {total_customers}")
    print(f" High Risk Customers:        {high_risk}")
    print(f" Medium Risk Customers:      {med_risk}")
    print(f" Low Risk Customers:         {low_risk}")
    print(f" Average Risk Score:         {avg_score:.1f} / 100")
    print(f" Expected Churn Count:       ~{expected_churn} customers")
    print("="*45 + "\n")

def export_reports(df):
    """Saves the final business datasets to CSV."""
    os.makedirs('outputs', exist_ok=True)
    
    # Export full dataset
    full_path = 'outputs/customer_risk_report.csv'
    df.to_csv(full_path, index=False)
    
    # Export targeted list for retention team
    high_risk_df = df[df['Risk_Category'] == 'High Risk'].sort_values(by='Risk_Score', ascending=False)
    high_path = 'outputs/high_risk_customers.csv'
    high_risk_df.to_csv(high_path, index=False)
    
    # Text-only success messages
    print(f"[SUCCESS] Generated full report: {full_path}")
    print(f"[SUCCESS] Generated target list: {high_path}\n")

# --- Run Script ---
if __name__ == "__main__":
    print("Initializing Business Intelligence Engine...\n")
    
    # Note: In a real environment, this might be a brand new dataset of current active customers.
    # We are testing it on our existing dataset.
    input_file = 'data/churnguard_data.csv' 
    
    final_business_df = generate_insights(input_file)
    print_executive_summary(final_business_df)
    export_reports(final_business_df)