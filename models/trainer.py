import os
import json
import joblib
import warnings

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.evaluation import ModelEvaluator

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from imblearn.over_sampling import SMOTE

from xgboost import XGBClassifier

from config import (
    PROCESSED_DATA,
    MODEL_PATH,
    METRIC_DIR,
    RANDOM_STATE,
    SMOTE_RANDOM_STATE
)

warnings.filterwarnings("ignore")

class FraudTrainer:

    def __init__(self):

        self.models = {}

        self.results = {}

    def load_data(self):

        X_train = pd.read_csv(
            os.path.join(PROCESSED_DATA, "X_train.csv")
        )

        X_test = pd.read_csv(
            os.path.join(PROCESSED_DATA, "X_test.csv")
        )

        y_train = pd.read_csv(
            os.path.join(PROCESSED_DATA, "y_train.csv")
        ).values.ravel()

        y_test = pd.read_csv(
            os.path.join(PROCESSED_DATA, "y_test.csv")
        ).values.ravel()

        return X_train, X_test, y_train, y_test

    def balance_data(self, X_train, y_train):

        smote = SMOTE(
            random_state=SMOTE_RANDOM_STATE
        )

        X_resampled, y_resampled = smote.fit_resample(
            X_train,
            y_train
        )

        print()

        print("Before SMOTE")

        print(pd.Series(y_train).value_counts())

        print()

        print("After SMOTE")

        print(pd.Series(y_resampled).value_counts())

        return X_resampled, y_resampled

    def initialize_models(self):

        self.models = {

            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=RANDOM_STATE
            ),

            "Random Forest": RandomForestClassifier(
                n_estimators=200,
                random_state=RANDOM_STATE
            ),

            "XGBoost": XGBClassifier(
                random_state=RANDOM_STATE,
                eval_metric="logloss"
            )
        }

    def evaluate(
        self,
        model,
        X_test,
        y_test
    ):

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:, 1]

        metrics = {

            "Accuracy": accuracy_score(
                y_test,
                predictions
            ),

            "Precision": precision_score(
                y_test,
                predictions
            ),

            "Recall": recall_score(
                y_test,
                predictions
            ),

            "F1 Score": f1_score(
                y_test,
                predictions
            ),

            "ROC AUC": roc_auc_score(
                y_test,
                probabilities
            )
        }

        return metrics

    def train_models(self):

        X_train, X_test, y_train, y_test = self.load_data()

        X_train, y_train = self.balance_data(
            X_train,
            y_train
        )

        self.initialize_models()

        best_f1 = 0

        best_model = None

        for name, model in self.models.items():

            print("=" * 60)

            print(name)

            model.fit(
                X_train,
                y_train
            )

            predictions = model.predict(X_test)

            probabilities = model.predict_proba(X_test)[:,1]


            metrics = self.evaluate(
                model,
                X_test,
                y_test
            )

            self.results[name] = metrics

            print(metrics)

            if metrics["F1 Score"] > best_f1:

                best_f1 = metrics["F1 Score"]

                best_model = model

                best_predictions = predictions

                best_probabilities = probabilities

        joblib.dump(
            best_model,
            MODEL_PATH
        )

        evaluator = ModelEvaluator(

            best_model,

            X_test,

            y_test,

            best_predictions,

            best_probabilities

        )

        evaluator.evaluate()

        print()

        print("Best model saved successfully.")

        pd.DataFrame(self.results).T.to_csv(

            os.path.join(

                METRIC_DIR,

                "model_comparison.csv"

            )

        )

    def save_metrics(self):

        output_file = os.path.join(
            METRIC_DIR,
            "model_metrics.json"
        )

        with open(
            output_file,
            "w"
        ) as file:

            json.dump(
                self.results,
                file,
                indent=4
            )

        print("Metrics saved.")