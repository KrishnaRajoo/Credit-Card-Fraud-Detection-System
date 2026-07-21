# ==========================================================
# Fraud Feature Mapper
# Converts business inputs into model-compatible features
# ==========================================================

import numpy as np


def create_features(user_data):

    """
    Convert:

    Time
    Amount
    Merchant Risk
    Location Risk
    Device Risk
    Transaction Frequency

    into:

    Time + V1-V28 + Amount

    required by trained model
    """


    # -------------------------------
    # User Inputs
    # -------------------------------

    time = float(
        user_data["Time"]
    )


    amount = float(
        user_data["Amount"]
    )


    merchant_risk = float(
        user_data["Merchant_Risk"]
    )


    location_risk = float(
        user_data["Location_Risk"]
    )


    device_risk = float(
        user_data["Device_Risk"]
    )


    frequency = float(
        user_data["Transaction_Frequency"]
    )



    # -------------------------------
    # Overall Risk Score
    # -------------------------------

    risk_score = (

        merchant_risk * 0.25 +

        location_risk * 0.20 +

        device_risk * 0.35 +

        frequency * 0.20

    ) / 100



    # -------------------------------
    # Generate V1-V28 patterns
    # -------------------------------


    if risk_score >= 0.70:

        # High fraud pattern

        v_features = [

            -2.5, 1.8, -3.2, 3.5,
            -1.9, -2.0, -3.1, 1.4,
            -2.8, -3.5, 2.7, -3.8,
            -1.4, -4.5, 1.2, -2.9,
            -3.7, -1.9, 0.8, -0.7,
            1.5, -2.0, 0.3, -1.4,
            0.5, -1.2, 0.6, -0.5

        ]


    elif risk_score >= 0.40:


        # Medium risk pattern

        v_features = [

            -1.0,0.7,-1.4,1.2,
            -0.8,-0.6,-1.1,0.5,
            -1.2,-1.4,1.0,-1.6,
            -0.5,-1.8,0.4,-1.1,
            -1.5,-0.6,0.3,-0.2,
            0.4,-0.8,0.2,-0.5,
            0.2,-0.4,0.2,-0.2

        ]


    else:


        # Normal transaction pattern

        v_features = np.random.normal(

            loc=0,

            scale=0.25,

            size=28

        )



    features = [

        time,

        *v_features,

        amount

    ]


    return np.array(
        features
    ).reshape(1,-1)