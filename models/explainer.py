import os
import joblib
import shap
import matplotlib.pyplot as plt
import pandas as pd

from config import (
    MODEL_PATH,
    PROCESSED_DATA,
    EXPLAIN_DIR
)
class FraudExplainer:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        self.X_train = pd.read_csv(

            os.path.join(

                PROCESSED_DATA,

                "X_train.csv"

            )

        )

        self.X_test = pd.read_csv(

            os.path.join(

                PROCESSED_DATA,

                "X_test.csv"

            )

        )

    def create_explainer(self):

        self.explainer = shap.TreeExplainer(
            self.model
        )

        self.shap_values = self.explainer.shap_values(
            self.X_test
        )

    def summary_plot(self):

        shap.summary_plot(

            self.shap_values,

            self.X_test,

            show=False

        )

        plt.tight_layout()

        plt.savefig(

            os.path.join(

                EXPLAIN_DIR,

                "shap_summary.png"

            )

        )

        plt.close()

    def bar_plot(self):

        shap.summary_plot(

            self.shap_values,

            self.X_test,

            plot_type="bar",

            show=False

        )

        plt.tight_layout()

        plt.savefig(

            os.path.join(

                EXPLAIN_DIR,

                "shap_bar.png"

            )

        )

        plt.close()

    def waterfall_plot(self):

        explanation = self.explainer(

            self.X_test.iloc[[0]]

        )

        shap.plots.waterfall(

            explanation[0],

            show=False

        )

        plt.savefig(

            os.path.join(

                EXPLAIN_DIR,

                "shap_waterfall.png"

            )

        )

        plt.close()

    def force_plot(self):

        force = shap.force_plot(

            self.explainer.expected_value,

            self.shap_values[0],

            self.X_test.iloc[0],

            matplotlib=False

        )

        shap.save_html(

            os.path.join(

                EXPLAIN_DIR,

                "shap_force.html"

            ),

            force

        )

    def save_values(self):

        joblib.dump(

            self.shap_values,

            os.path.join(

                EXPLAIN_DIR,

                "shap_values.pkl"

            )

        )

    def explain(self):

        self.create_explainer()

        self.summary_plot()

        self.bar_plot()

        self.waterfall_plot()

        self.force_plot()

        self.save_values()

        print("Explainability completed.")