import os
import joblib
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from src.feature_mapper import create_features

from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# Flask Configuration
# ==========================================================

app = Flask(__name__)


# ==========================================================
# Load Model and Scaler
# ==========================================================

MODEL_PATH = os.path.join(
    "saved_models",
    "fraud_detector.pkl"
)

SCALER_PATH = os.path.join(
    "data",
    "processed",
    "scaler.pkl"
)


model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)


print("Model loaded successfully")


# ==========================================================
# Home Route
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# Prediction API
# ==========================================================

@app.route(
    "/predict",
    methods=["POST"]
)

def predict():

    try:

        # ----------------------------------------------
        # Get Input Data
        # ----------------------------------------------

        data = request.get_json()


        amount = float(
            data["Amount"]
        )

        time = float(
            data["Time"]
        )

        transaction = create_features(
            data
        )


        transaction = pd.DataFrame(

            transaction,

            columns=[
                "Time"
            ]
            +
            [
                f"V{i}"
                for i in range(1,29)
            ]
            +
            [
                "Amount"
            ]

        )



        # ----------------------------------------------
        # Scale Amount
        # ----------------------------------------------

        transaction["Amount"] = scaler.transform(
            transaction[["Amount"]]
        )


        # ----------------------------------------------
        # Prediction
        # ----------------------------------------------

        prediction = model.predict(
            transaction
        )[0]


        probability = model.predict_proba(
            transaction
        )[0][1]

        merchant_risk = float(data["Merchant_Risk"])
        location_risk = float(data["Location_Risk"])
        device_risk = float(data["Device_Risk"])
        frequency = float(data["Transaction_Frequency"])
        amount = float(data["Amount"])



        # ----------------------------------------------
        # Risk Level
        # ----------------------------------------------
        risk_score = float(
            f"{float(probability) * 100:.2f}"
        )


        if risk_score >= 75:

            risk = "HIGH"
            message = ("This transaction shows multiple ""high-risk indicators and requires immediate review.")


        elif risk_score >= 40:

            risk = "MEDIUM"
            message = ("This transaction has suspicious ""patterns and should be monitored.")


        else:

            risk = "LOW"
            message = ("This transaction appears normal ""with low fraud probability.")

        insights = []

        if merchant_risk >= 70:
            insights.append("High merchant risk score detected.")

        if location_risk >= 70:
            insights.append("Transaction originated from a high-risk location.")

        if device_risk >= 70:
            insights.append("Device appears suspicious based on its risk score.")

        if frequency >= 20:
            insights.append("High transaction frequency detected.")

        if amount >= 5000:
            insights.append("Large transaction amount observed.")

        if len(insights) == 0:
            insights.append("No significant fraud indicators detected.")



        result = {

            "prediction":
                str(
                    "Fraud"
                    if int(prediction) == 1
                    else "Genuine"
                ),

            "probability":
                float(risk_score),

            "risk_score":
                float(risk_score),

            "risk":
                str(risk),

            "confidence":
                float(
                    round(
                        float(
                            max(
                                probability,
                                1 - probability
                            )
                        ) * 100,
                        2
                    )
                ),
            "insights": insights

        }

        return jsonify(result)



    except Exception as e:


        return jsonify(

            {
                "error":str(e)
            }

        ),500




# ==========================================================
# Health Check (For Deployment)
# ==========================================================

@app.route("/health")
def health():

    return jsonify(

        {
            "status":"running",
            "message":
            "Fraud Detection API is active"
        }

    )


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )