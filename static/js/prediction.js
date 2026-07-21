function loadHistory(){

    const history =
    JSON.parse(
        localStorage.getItem("fraudHistory")
    ) || [];

    const tbody =
    document.getElementById("history-body");

    tbody.innerHTML = "";

    history.forEach(function(item){

        tbody.innerHTML += `

        <tr>

            <td>${item.time}</td>

            <td>₹ ${item.amount}</td>

            <td class="${
                item.prediction==="Fraud"
                ? "fraud"
                : "genuine"
            }">

                ${item.prediction}

            </td>

            <td>

                ${item.risk}

            </td>

        </tr>

        `;

    });

}



function saveHistory(item){

    let history =
    JSON.parse(
        localStorage.getItem("fraudHistory")
    ) || [];

    history.unshift(item);

    history = history.slice(0,5);

    localStorage.setItem(

        "fraudHistory",

        JSON.stringify(history)

    );

    loadHistory();

}

document
.getElementById("prediction-form")
.addEventListener(
"submit",
async function(e){

    e.preventDefault();

    // ----------------------------------
    // Collect User Inputs
    // ----------------------------------

    let data = {};

    data["Time"] =
    document.getElementById("Time").value;

    data["Amount"] =
    document.getElementById("Amount").value;

    data["Merchant_Risk"] =
    document.getElementById("Merchant_Risk").value;

    data["Location_Risk"] =
    document.getElementById("Location_Risk").value;

    data["Device_Risk"] =
    document.getElementById("Device_Risk").value;

    data["Transaction_Frequency"] =
    document.getElementById("Transaction_Frequency").value;


    try{

        // ----------------------------------
        // Send Request
        // ----------------------------------

        const response =
        await fetch(
            "/predict",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(data)
            }
        );

        const result =
        await response.json();

        if(result.error){

            alert(result.error);
            return;

        }

        // ----------------------------------
        // Result Card
        // ----------------------------------

        const predictionText =
        document.getElementById("prediction-text");

        const resultCard =
        document.getElementById("result-card");

        predictionText.innerHTML =
        result.prediction;

        if(result.prediction==="Fraud"){

            resultCard.style.border =
            "2px solid #E50914";

            resultCard.style.boxShadow =
            "0 0 40px rgba(229,9,20,.50)";

        }

        else{

            resultCard.style.border =
            "2px solid #00ff84";

            resultCard.style.boxShadow =
            "0 0 40px rgba(0,255,132,.35)";

        }

        // ----------------------------------
        // Prediction Values
        // ----------------------------------

        document.getElementById("probability").innerHTML =
        result.probability + "%";

        document.getElementById("risk").innerHTML =
        result.risk;

        document.getElementById("confidence").innerHTML =
        result.confidence + "%";

        // ----------------------------------
        // Risk Score
        // ----------------------------------

        const riskScore =
        document.getElementById("riskScore");

        if(riskScore){

            riskScore.innerHTML =
            result.risk_score + "%";

        }

        // ----------------------------------
        // AI Message
        // ----------------------------------

        const message =
        document.getElementById("messageText");

        if(message){

            message.innerHTML =
            result.message;

        }

        // ----------------------------------
        // Risk Circle
        // ----------------------------------

        const riskCircle =
        document.querySelector(".risk-circle");

        if(riskCircle){

            const degree =
            result.risk_score * 3.6;

            let color =
            "#00ff84";

            if(result.risk==="MEDIUM"){

                color="#FFD700";

            }

            if(result.risk==="HIGH"){

                color="#E50914";

            }

            riskCircle.style.background =
            `conic-gradient(${color} ${degree}deg,#222 ${degree}deg)`;

        }

        // ----------------------------------
        // Transaction Summary
        // ----------------------------------

        document.getElementById("summary-time").textContent =
        data.Time;

        document.getElementById("summary-amount").textContent =
        "₹ " + Number(data.Amount).toLocaleString("en-IN");

        document.getElementById("summary-merchant").textContent =
        data.Merchant_Risk + " / 100";

        document.getElementById("summary-location").textContent =
        data.Location_Risk + " / 100";

        document.getElementById("summary-device").textContent =
        data.Device_Risk + " / 100";

        document.getElementById("summary-frequency").textContent =
        data.Transaction_Frequency;

        // ----------------------------------
        // AI Decision Insights
        // ----------------------------------

        const insightsList =
        document.getElementById("insights-list");

        if(insightsList){

            insightsList.innerHTML = "";

            if(result.insights &&
                result.insights.length>0){

                result.insights.forEach(function(item){

                    const li =
                    document.createElement("li");

                    li.innerHTML =
                    "✔ " + item;

                    insightsList.appendChild(li);

                });

            }

        }
        saveHistory({

            time:new Date().toLocaleTimeString(),

            amount:Number(data.Amount).toLocaleString("en-IN"),

            prediction:result.prediction,

            risk:result.risk

        });

    }

    catch(error){

        console.error(error);

        alert(
            "Unable to connect to the server."
        );

    }

});
loadHistory();