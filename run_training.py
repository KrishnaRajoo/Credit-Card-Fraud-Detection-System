from models.trainer import FraudTrainer

trainer = FraudTrainer()

trainer.train_models()

trainer.save_metrics()

print()

print("Training Completed Successfully.")