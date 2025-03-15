document.getElementById("printReportBtn").addEventListener("click", function (event) {
    event.preventDefault();

    const { jsPDF } = window.jspdf;
    let doc = new jsPDF("p", "mm", "a4");

    let patientData = latestPatientData.patient_data || {};
    let patientName = patientData["Name"] || "N/A";
    let age = patientData["Age"] || "N/A";
    let gender = sessionStorage.getItem("gender") || "N/A";
    let DoA = patientData["Date of Admission"] || "N/A";
    let bloodGroup = patientData["Blood Group"] || "N/A";

    let temperature = patientData["Body Temperature"] || "N/A";
    let heartRate = patientData["Heart Rate"] || "N/A";
    let oxygenSaturation = patientData["Oxygen Saturation"] || "N/A";

    let riskScore = latestPatientData["risk_score"] || "N/A";

    let riskFactors = latestPatientData["risk_factors"] || {};

    // Find the maximum risk factor
    let maxRiskFactor = "N/A";
    let maxRiskPercentage = 0;
    for (let factor in riskFactors) {
        if (riskFactors[factor] > maxRiskPercentage) {
            maxRiskFactor = factor;
            maxRiskPercentage = riskFactors[factor];
        }
    }

    let survivalProbability = latestPatientData["survival_probability"] || "N/A";

    // let doctorName = sessionStorage.getItem("doctor_name") || "N/A";
    let generateID = sessionStorage.getItem("generate_id") || "N/A";

    // Get current timestamp
    let generatedAt = new Date().toLocaleString();

    let img = new Image();
    img.src = "static/images/patientreport.png";
    img.onload = function () {
        doc.addImage(img, "PNG", 0, 0, 210, 297);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);

        doc.text(`${patientName}`, 50, 54);
        doc.text(`${age}`, 50, 63);
        doc.text(`${gender}`, 50, 72);
        doc.text(`${DoA}`, 150, 54);
        doc.text(`${bloodGroup}`, 150, 63);

        doc.text(`${temperature} °C`, 80, 98);
        doc.text(`${heartRate} bpm`, 80, 107);
        doc.text(`${oxygenSaturation} %`, 80, 116);
        doc.text(`${riskScore}`, 80, 134);
        doc.text(`${maxRiskFactor} ${maxRiskPercentage}%`, 80, 143);
        doc.text(`${survivalProbability} %`, 80, 152);

        doc.setFont("helvetica", "italic");
        doc.setFontSize(10); 
        doc.text(`${generatedAt}`, 46, 243);
        doc.text(`${generateID}`, 148, 243);

        doc.save(`Patient_Report_${patientName}.pdf`);
    };
});