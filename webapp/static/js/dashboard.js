// Initialize socket connection
const socket = io.connect();
socket.emit("request_live_data");

// Initialize gauges with consistent options
const gaugeOptions = {
    angle: 0.15,
    lineWidth: 0.2
};

const tempGauge = new Gauge(document.getElementById("tempGauge")).setOptions({
    ...gaugeOptions,
    colorStart: "rgb(70, 87, 48)",
    colorStop: "rgb(70, 87, 48)"
});

const heartRateGauge = new Gauge(document.getElementById("heartRateGauge")).setOptions({
    ...gaugeOptions,
    colorStart: "rgb(45, 92, 86)",
    colorStop: "rgb(45, 92, 86)"
});

const oxygenGauge = new Gauge(document.getElementById("oxygenGauge")).setOptions({
    ...gaugeOptions,
    colorStart: "rgb(101, 50, 56)",
    colorStop: "rgb(101, 50, 56)"
});

// Initialize data stores for charts
const riskScoreData = { labels: [], values: [] };
const survivalProbData = { labels: [], values: [] };

// Create initial charts
const riskScoreChart = createLineChart("riskScoreChart", "Risk Score Over Time", riskScoreData);
const survivalProbChart = createLineChart("survivalProbability", "Survival Probability Over Time", survivalProbData);

// Handle data updates from server
socket.on("update_live_data", function (data) {
    console.log("Received Data:", data);

    if (!data || !data.patient_data) {
        console.error("❌ No data received from server!");
        return;
    }

    latestPatientData = data;

    // Update gauges with new values
    tempGauge.set(data.patient_data["Body Temperature"]);
    heartRateGauge.set(data.patient_data["Heart Rate"]);
    oxygenGauge.set(data.patient_data["Oxygen Saturation"]);

    // Update text displays
    document.getElementById("tempValue").textContent = data.patient_data["Body Temperature"] + " °C";
    document.getElementById("heartRateValue").textContent = data.patient_data["Heart Rate"] + " bpm";
    document.getElementById("oxygenValue").textContent = data.patient_data["Oxygen Saturation"] + " %";

    // Update risk category and charts
    updateRiskCategory(data["risk_score"]);
    updateChart("riskFactorsBar", "bar", Object.values(data.risk_factors), Object.keys(data.risk_factors));
    updateProgressiveChart(riskScoreChart, riskScoreData, data["risk_score"]);
    updateProgressiveChart(survivalProbChart, survivalProbData, data["survival_probability"]);
});

// Function to update risk category display
function updateRiskCategory(score) {
    const riskMarker = document.getElementById("riskMarker");
    const riskLabel = document.getElementById("riskLabel");

    // Map riskScore (0-100) to percentage width of the bar
    const position = (score / 100) * 100;
    riskMarker.style.left = position + "%";

    // Define risk levels
    let riskText = "Low Risk";
    if (score >= 70) riskText = "High Risk";
    else if (score >= 40) riskText = "Moderate Risk";

    // Update label
    riskLabel.textContent = riskText + " (" + score.toFixed(1) + "%)";
}

// Function to update or create a chart
function updateChart(canvasId, type, data, labels = ["Data"]) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    if (window[canvasId] instanceof Chart) {
        window[canvasId].destroy();
    }

    window[canvasId] = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    "rgb(56, 84, 46)",
                    "rgb(52, 100, 90)",
                    "rgb(88, 45, 77)",
                    "#4BC0C0",
                    "rgb(123, 122, 42)",
                    "#FF9F40"
                ],
                borderColor: "#fff",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Function to create a line chart
function createLineChart(canvasId, label, dataStore) {
    const ctx = document.getElementById(canvasId).getContext("2d");
    return new Chart(ctx, {
        type: "line",
        data: {
            labels: dataStore.labels,
            datasets: [{
                label: label,
                data: dataStore.values,
                borderColor: "rgb(56, 84, 46)",
                fill: false,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Value"
                    }
                }
            }
        }
    });
}

// Function to update progressive charts (line charts with time-based data)
function updateProgressiveChart(chart, dataStore, newValue) {
    const now = new Date().toLocaleTimeString();

    // Maintain a fixed window of data points
    if (dataStore.labels.length >= 20) {
        dataStore.labels.shift();
        dataStore.values.shift();
    }

    dataStore.labels.push(now);
    dataStore.values.push(newValue);
    chart.update();
}