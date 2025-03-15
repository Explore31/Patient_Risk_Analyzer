document.getElementById("login-form").addEventListener("submit", function (e) {
    e.preventDefault(); // Stop form from reloading the page
    let formData = new FormData(this);

    fetch(LOGIN_URL, {  // Use the predefined URL
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.text(); // Get error message
        }
        window.location.href = SUCCESS_URL; // Redirect on success
    })
    .then(errorMessage => {
        if (errorMessage) {
            let errorDiv = document.getElementById("error-message");
            errorDiv.textContent = errorMessage;
            errorDiv.style.display = "block"; // Show error message above the form

            document.getElementById("email").value = "";
            document.getElementById("password").value = "";
        }
    });
});
