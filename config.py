import os

# ==========================================================
# Project Root
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# Data
# ==========================================================

RAW_DATA = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "creditcard.csv"
)

PROCESSED_DATA = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

# ==========================================================
# Saved Models
# ==========================================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "saved_models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "fraud_detector.pkl"
)

# ==========================================================
# Reports
# ==========================================================

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

FIGURE_DIR = os.path.join(
    REPORT_DIR,
    "figures"
)

EXPLAIN_DIR = os.path.join(
    REPORT_DIR,
    "explainability"
)

METRIC_DIR = os.path.join(
    REPORT_DIR,
    "metrics"
)

LOG_DIR = os.path.join(
    REPORT_DIR,
    "logs"
)

# ==========================================================
# Random State
# ==========================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

# ==========================================================
# Training
# ==========================================================

CV_FOLDS = 5

SCORING = "f1"

SMOTE_RANDOM_STATE = 42