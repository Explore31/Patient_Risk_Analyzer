function filterPatients(inputType) {
    const patients = JSON.parse(document.getElementById("patient-data").getAttribute("data-patients"));
    let input = document.getElementById(inputType);
    let dropdown = document.getElementById(inputType + "_dropdown");
    let filter = input.value.toLowerCase();
    dropdown.innerHTML = "";

    if (!filter) {
        dropdown.style.display = "none";
        return;
    }

    let matches = patients.filter(patient =>
        (inputType === "patient_id" ? patient.id : patient.name).toLowerCase().includes(filter)
    );

    matches.forEach(patient => {
        let option = document.createElement("div");
        option.textContent = inputType === "patient_id" ? patient.id : patient.name;
        option.onclick = function () {
            input.value = this.textContent;
            dropdown.style.display = "none";
        };
        dropdown.appendChild(option);
    });

    dropdown.style.display = matches.length > 0 ? "block" : "none";
}

document.addEventListener("click", function (e) {
    if (!e.target.matches("input")) {
        document.getElementById("patient_id_dropdown").style.display = "none";
        document.getElementById("patient_name_dropdown").style.display = "none";
    }
});


