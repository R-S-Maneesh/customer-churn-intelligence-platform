from model_comparison import train_and_evaluate_models


if __name__ == "__main__":
    print("Training production models from data/churnguard_data.csv...")
    summary = train_and_evaluate_models("data/churnguard_data.csv")
    print("\n--- Model Comparison Table ---")
    print(summary["comparison"].to_string(index=False))
    print("\nSuccess! Model, scaler, metrics, and images were regenerated.")
