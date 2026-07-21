import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay,
    classification_report
)

from config import FIGURE_DIR, METRIC_DIR

class ModelEvaluator:

    def __init__(
        self,
        model,
        X_test,
        y_test,
        predictions,
        probabilities
    ):

        self.model = model

        self.X_test = X_test

        self.y_test = y_test

        self.predictions = predictions

        self.probabilities = probabilities

    def confusion_matrix_plot(self):

        cm = confusion_matrix(
            self.y_test,
            self.predictions
        )

        fig, ax = plt.subplots(figsize=(6,6))

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm
        )

        disp.plot(ax=ax)

        plt.title("Confusion Matrix")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "confusion_matrix.png"
            )
        )

        plt.close()

    def roc_curve(self):

        fig, ax = plt.subplots(figsize=(7,6))

        RocCurveDisplay.from_predictions(

            self.y_test,

            self.probabilities,

            ax=ax

        )

        plt.title("ROC Curve")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "roc_curve.png"
            )
        )

        plt.close()

    def precision_recall_curve(self):

        fig, ax = plt.subplots(figsize=(7,6))

        PrecisionRecallDisplay.from_predictions(

            self.y_test,

            self.probabilities,

            ax=ax

        )

        plt.title("Precision Recall Curve")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "precision_recall_curve.png"
            )
        )

        plt.close()

    def save_classification_report(self):

        report = classification_report(

            self.y_test,

            self.predictions

        )

        with open(

            os.path.join(

                METRIC_DIR,

                "classification_report.txt"

            ),

            "w"

        ) as file:

            file.write(report)

    def feature_importance(self):

        importance = self.model.feature_importances_

        columns = self.X_test.columns

        indices = np.argsort(importance)[::-1]

        plt.figure(figsize=(12,8))

        plt.bar(

            range(len(indices)),

            importance[indices]

        )

        plt.xticks(

            range(len(indices)),

            columns[indices],

            rotation=90

        )

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.savefig(

            os.path.join(

                FIGURE_DIR,

                "feature_importance.png"

            )

        )

        plt.close()

    def evaluate(self):

        self.confusion_matrix_plot()

        self.roc_curve()

        self.precision_recall_curve()

        self.feature_importance()

        self.save_classification_report()

        print("Evaluation completed.")