import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from config import (
    RAW_DATA,
    PROCESSED_DATA,
    RANDOM_STATE,
    TEST_SIZE
)

class FraudPreprocessor:

    def __init__(self):
        self.df = pd.read_csv(RAW_DATA)
        self.scaler = StandardScaler()

    def prepare_features(self):

        X = self.df.drop("Class", axis=1)
        y = self.df["Class"]

        return X, y

    def split_data(self):

        X, y = self.prepare_features()

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y
        )

        return X_train, X_test, y_train, y_test

    def scale_features(self):

        X_train, X_test, y_train, y_test = self.split_data()

        X_train = X_train.copy()
        X_test = X_test.copy()

        X_train["Amount"] = self.scaler.fit_transform(
            X_train[["Amount"]]
        )

        X_test["Amount"] = self.scaler.transform(
            X_test[["Amount"]]
        )

        return X_train, X_test, y_train, y_test

    def save_processed_data(self):

        X_train, X_test, y_train, y_test = self.scale_features()

        X_train.to_csv(
            os.path.join(PROCESSED_DATA, "X_train.csv"),
            index=False
        )

        X_test.to_csv(
            os.path.join(PROCESSED_DATA, "X_test.csv"),
            index=False
        )

        y_train.to_csv(
            os.path.join(PROCESSED_DATA, "y_train.csv"),
            index=False
        )

        y_test.to_csv(
            os.path.join(PROCESSED_DATA, "y_test.csv"),
            index=False
        )

        joblib.dump(
            self.scaler,
            os.path.join(PROCESSED_DATA, "scaler.pkl")
        )

        print("Processed data saved successfully.")