from src.preprocessing import FraudPreprocessor

preprocessor = FraudPreprocessor()

preprocessor.save_processed_data()

print("Preprocessing completed successfully.")