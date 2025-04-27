document.getElementById('addPatientForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = this;

    fetch(form.action, {
        method: 'POST',
        credentials: 'same-origin',               // ← include cookies
        headers: {
            'X-Requested-With': 'XMLHttpRequest'    // ← mark as AJAX
        },
        body: new FormData(form)
    })
        .then(response => {
            if (!response.ok) {
                // If server returned e.g. 400 or 500, read text to show
                return response.text().then(text => {
                    throw new Error(text || response.statusText);
                });
            }
            return response.json();
        })
        .then(json => {
            if (json.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Patient added!',
                    showConfirmButton: false,
                    timer: 1500,
                    willClose: () => {
                        window.location.href = SUCCESS_URL;
                    }
                });
            } else {
                Swal.fire('Error', json.error || 'Unknown error', 'error');
            }
        })
        .catch(err => {
            Swal.fire('Error', err.message, 'error');
        });
});