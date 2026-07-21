import os

from config import (
    PROCESSED_DATA,
    MODEL_DIR,
    REPORT_DIR,
    FIGURE_DIR,
    EXPLAIN_DIR,
    METRIC_DIR,
    LOG_DIR
)


def create_directories():
    """
    Create all required project directories.
    """

    directories = [
        PROCESSED_DATA,
        MODEL_DIR,
        REPORT_DIR,
        FIGURE_DIR,
        EXPLAIN_DIR,
        METRIC_DIR,
        LOG_DIR
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("Project directories are ready.")