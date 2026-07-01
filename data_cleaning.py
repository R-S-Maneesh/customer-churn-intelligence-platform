import pandas as pd

def clean_data(df, verbose=False):
    """
    Takes a raw dataframe, applies all cleaning steps, 
    and returns a production-ready dataframe.
    """
    # --- Existing Cleaning ---
    
    # Remove customerID
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])
        
    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize categorical values
    df['gender'] = df['gender'].str.strip()
    df['PaymentMethod'] = df['PaymentMethod'].str.strip()
    df['Churn'] = df['Churn'].str.strip().str.title()
    df['PhoneService'] = df['PhoneService'].str.strip().str.title()
    df['PaperlessBilling'] = df['PaperlessBilling'].str.strip().str.title()

    # Fix Contract values
    contract_map = {
        'month to month': 'Month-to-month', 'month-to-month': 'Month-to-month',
        'monthly': 'Month-to-month', 'one year': 'One year', '1 year': 'One year',
        'two year': 'Two year', '2 year': 'Two year'
    }
    df['Contract'] = df['Contract'].str.lower().str.strip().replace(contract_map)

    # Fix InternetService values
    internet_map = {
        'dsl': 'DSL', 'fibre optic': 'Fiber optic', 'fiberoptic': 'Fiber optic',
        'fiber optic': 'Fiber optic', 'none': 'No', 'no': 'No'
    }
    df['InternetService'] = df['InternetService'].str.lower().str.strip().replace(internet_map)

    # Convert TotalCharges to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Handle invalid tenure values
    df = df[df['tenure'].isna() | (df['tenure'] > 0)]
    
    # Handle MonthlyCharges outliers
    df = df[df['MonthlyCharges'].isna() | ((df['MonthlyCharges'] >= 10) & (df['MonthlyCharges'] <= 200))]

    # Fill missing numeric values
    df['MonthlyCharges'] = df['MonthlyCharges'].fillna(df['MonthlyCharges'].mean())
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].mean())
    tenure_median = round(df['tenure'].median())
    df['tenure'] = df['tenure'].fillna(tenure_median).astype(int)

    # --- Additional Improvements ---
    
    # Fill remaining missing values in InternetService using mode imputation
    internet_mode = df['InternetService'].mode()[0]
    df['InternetService'] = df['InternetService'].fillna(internet_mode)

    if verbose:
        print("\n--- Final Data Quality Report ---")
        print(f"Dataset Shape: {df.shape}")
        print("\nRemaining Missing Values:")
        print(df.isna().sum())
        print(f"\nDuplicate Count: {df.duplicated().sum()}")
        print("\nClass Distribution (Churn):")
        print(df['Churn'].value_counts())
        print("---------------------------------\n")

    return df

# Test block: This only runs if you execute this file directly
if __name__ == "__main__":
    raw_data = pd.read_csv('data/churnguard_data.csv')
    clean_df = clean_data(raw_data, verbose=True)
