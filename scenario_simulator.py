import pandas as pd
import joblib
import os

# Importing cleaning function from Task 1
from data_cleaning import clean_data

# --- 1. Load Artifacts ---
def load_artifacts():
    """Loads the production model and scaler."""
    try:
        model = joblib.load('models/logistic_model_vB.pkl')
        scaler = joblib.load('models/scaler_vB.pkl')
        return model, scaler
    except FileNotFoundError:
        print("Error: Could not find model files. Ensure you ran Task 2 first.")
        exit()

# --- 2. Interactive Input ---
def get_customer_input():
    """Gets customer data via manual input or default test profile."""
    print("\n--- Customer Retention Scenario Simulator ---")
    choice = input("Use default high-risk customer for testing? (y/n): ").strip().lower()
    
    if choice == 'y' or choice == '':
        print("[INFO] Using default high-risk profile...\n")
        return {
            'gender': 'Male',
            'SeniorCitizen': 1,
            'tenure': 2,
            'PhoneService': 'Yes',
            'InternetService': 'Fiber optic',
            'Contract': 'Month-to-month',
            'PaperlessBilling': 'Yes',
            'PaymentMethod': 'Electronic check',
            'MonthlyCharges': 95.50,
            # Dummies required so clean_data() doesn't crash
            'TotalCharges': 191.0, 
            'Churn': 'No' 
        }
    
    # Manual Input Fallback
    print("\n--- Enter Customer Details ---")
    return {
        'gender': input("Gender (Male/Female): "),
        'SeniorCitizen': int(input("Senior Citizen? (1 = Yes, 0 = No): ")),
        'tenure': int(input("Tenure (months): ")),
        'PhoneService': input("Phone Service (Yes/No): "),
        'InternetService': input("Internet Service (DSL/Fiber optic/No): "),
        'Contract': input("Contract (Month-to-month/One year/Two year): "),
        'PaperlessBilling': input("Paperless Billing (Yes/No): "),
        'PaymentMethod': input("Payment Method (e.g., Electronic check): "),
        'MonthlyCharges': float(input("Monthly Charges ($): ")),
        'TotalCharges': 0.0, # Dummy
        'Churn': 'No' # Dummy
    }

# --- 3. Prediction Engine ---
def predict_risk(df_row, model, scaler):
    """Formats a single row, scales it, and returns churn probability."""
    # Dummy encode categorical variables
    cat_cols = ['gender', 'PhoneService', 'InternetService', 'Contract', 'PaperlessBilling', 'PaymentMethod']
    X = pd.get_dummies(df_row, columns=cat_cols)
    
    # Drop unused columns
    for c in ['Churn', 'TotalCharges', 'customerID']:
        if c in X.columns:
            X = X.drop(columns=[c])
            
    # CRITICAL: Reindex to exactly match model's expected features
    expected_columns = model.feature_names_in_
    X = X.reindex(columns=expected_columns, fill_value=0)
    
    # Scale numeric features
    X[['tenure', 'MonthlyCharges']] = scaler.transform(X[['tenure', 'MonthlyCharges']])
    
    # Predict Probability
    probability = model.predict_proba(X)[0][1]
    return probability

def get_category(prob):
    """Translates probability into business risk categories."""
    score = prob * 100
    if score >= 70: return 'High Risk'
    elif score >= 30: return 'Medium Risk'
    else: return 'Low Risk'

# --- 4. Simulation Engine ---
def run_simulations(customer_dict, model, scaler):
    """Runs the base scenario and 4 alternative realities."""
    # Convert dict to DataFrame and clean it using our existing pipeline
    raw_df = pd.DataFrame([customer_dict])
    
    print("\n[INFO] Running Data Cleaning Pipeline on input...")
    clean_df = clean_data(raw_df) 
    
    results = []
    
    # Baseline (Current)
    base_prob = predict_risk(clean_df.copy(), model, scaler)
    results.append({
        'Scenario': 'Current (Baseline)',
        'Probability': base_prob,
        'Risk Category': get_category(base_prob),
        'Risk Reduction %': 0.0
    })
    
    # Scenario A: One Year Contract
    df_A = clean_df.copy()
    df_A['Contract'] = 'One year'
    prob_A = predict_risk(df_A, model, scaler)
    
    # Scenario B: Two Year Contract
    df_B = clean_df.copy()
    df_B['Contract'] = 'Two year'
    prob_B = predict_risk(df_B, model, scaler)
    
    # Scenario C: 15% Discount
    df_C = clean_df.copy()
    df_C['MonthlyCharges'] = df_C['MonthlyCharges'] * 0.85
    prob_C = predict_risk(df_C, model, scaler)
    
    # Scenario D: +12 Months Tenure
    df_D = clean_df.copy()
    df_D['tenure'] = df_D['tenure'] + 12
    prob_D = predict_risk(df_D, model, scaler)
    
    # Calculate Reductions and add to results
    scenarios = [
        ('Convert to One-Year Contract', prob_A),
        ('Convert to Two-Year Contract', prob_B),
        ('Apply 15% Discount Plan', prob_C),
        ('Increase Tenure by 12 Months', prob_D)
    ]
    
    for name, prob in scenarios:
        reduction = ((base_prob - prob) / base_prob) * 100
        # If risk goes up, cap reduction at 0 for clean reporting
        reduction = max(0, reduction) 
        
        results.append({
            'Scenario': name,
            'Probability': prob,
            'Risk Category': get_category(prob),
            'Risk Reduction %': round(reduction, 1)
        })
        
    return pd.DataFrame(results)

# --- 5. Export and Print Summary ---
def present_results(results_df):
    """Prints the final summary and exports to CSV."""
    os.makedirs('outputs', exist_ok=True)
    export_path = 'outputs/scenario_simulation_report.csv'
    results_df.to_csv(export_path, index=False)
    
    # Format for printing
    print("\n" + "="*80)
    print(" SIMULATION RESULTS: CUSTOMER RETENTION SCENARIOS")
    print("="*80)
    
    for _, row in results_df.iterrows():
        prob_pct = row['Probability'] * 100
        print(f" {row['Scenario']:<30} | Risk: {prob_pct:.1f}% ({row['Risk Category']})     | Reduction: {row['Risk Reduction %']}%")
        
    print("="*80)
    
    # Identify Best Strategy (Excluding the baseline)
    strategy_df = results_df.iloc[1:]
    best_strategy = strategy_df.loc[strategy_df['Risk Reduction %'].idxmax()]
    
    print("\n [RECOMMENDATION] BEST RETENTION STRATEGY:")
    print(f" -> {best_strategy['Scenario']}")
    print(f" -> Risk Reduced by {best_strategy['Risk Reduction %']}%\n")
    
    print(f"[SUCCESS] Simulation exported to: {export_path}\n")

# --- Run Script ---
if __name__ == "__main__":
    # Load model artifacts
    model, scaler = load_artifacts()
    
    # Get user input
    customer_data = get_customer_input()
    
    # Run simulations
    simulation_results = run_simulations(customer_data, model, scaler)
    
    # Present results
    present_results(simulation_results)
