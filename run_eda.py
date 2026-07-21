from src.eda import FraudEDA

eda = FraudEDA()

eda.dataset_overview()

eda.fraud_percentage()

eda.missing_values()

eda.save_class_distribution()

eda.amount_distribution()

eda.time_distribution()

eda.correlation_heatmap()

eda.save_summary()

print("EDA Completed Successfully.")