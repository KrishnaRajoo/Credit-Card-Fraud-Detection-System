import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import RAW_DATA, FIGURE_DIR

plt.style.use("ggplot")


class FraudEDA:

    def __init__(self):
        self.df = pd.read_csv(RAW_DATA)

    def dataset_overview(self):
        print("=" * 60)
        print("DATASET OVERVIEW")
        print("=" * 60)

        print(f"Rows    : {self.df.shape[0]}")
        print(f"Columns : {self.df.shape[1]}")

        print("\nColumns")
        print(self.df.columns.tolist())

        print("\nData Types")
        print(self.df.dtypes)

        print("\nMissing Values")
        print(self.df.isnull().sum())

        print("\nSummary Statistics")
        print(self.df.describe())

    def save_class_distribution(self):

        counts = self.df["Class"].value_counts()

        plt.figure(figsize=(6,5))
        counts.plot(kind="bar")

        plt.title("Class Distribution")
        plt.xlabel("Class")
        plt.ylabel("Count")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "class_distribution.png"
            )
        )

        plt.close()

    def fraud_percentage(self):

        fraud = self.df["Class"].sum()
        total = len(self.df)

        percentage = fraud / total * 100

        print(f"Fraud Transactions : {fraud}")
        print(f"Genuine Transactions : {total - fraud}")
        print(f"Fraud Percentage : {percentage:.4f}%")

    def missing_values(self):

        missing = self.df.isnull().sum()

        print(missing)

        print()

        print("Total Missing :", missing.sum())

    def save_class_distribution(self):

        counts = self.df["Class"].value_counts()

        plt.figure(figsize=(6,5))

        ax = counts.plot(kind="bar")

        plt.title("Fraud vs Genuine Transactions")

        plt.xlabel("Class")

        plt.ylabel("Transactions")

        for p in ax.patches:
            ax.annotate(
                str(int(p.get_height())),
                (p.get_x()+0.2, p.get_height())
            )

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "class_distribution.png"
            )
        )

        plt.close()

    def amount_distribution(self):

        plt.figure(figsize=(10,5))

        plt.hist(
            self.df["Amount"],
            bins=60
        )

        plt.title("Transaction Amount Distribution")

        plt.xlabel("Amount")

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "amount_distribution.png"
            )
        )

        plt.close()

    def time_distribution(self):

        plt.figure(figsize=(10,5))

        plt.hist(
            self.df["Time"],
            bins=60
        )

        plt.title("Transaction Time Distribution")

        plt.xlabel("Time")

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "time_distribution.png"
            )
        )

        plt.close()

    def correlation_heatmap(self):

        plt.figure(figsize=(15,12))

        sns.heatmap(
            self.df.corr(),
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                FIGURE_DIR,
                "correlation_heatmap.png"
            )
        )

        plt.close()

    def save_summary(self):

        with open(
            os.path.join(
                "reports",
                "metrics",
                "eda_summary.txt"
            ),
            "w"
        ) as file:

            file.write("Credit Card Fraud Detection\n")

            file.write("="*40)

            file.write("\n\n")

            file.write(str(self.df.describe()))

            file.write("\n\n")

            file.write(str(self.df.dtypes))