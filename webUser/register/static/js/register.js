    document.getElementById('registerButton').addEventListener('click', function () {
       
        const form = document.getElementById('registerForm');
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                Swal.fire({
                    title: 'Thành công!',
                    text: data.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = loginUrl;
                    }
                });
            } else if (data.error) {
                Swal.fire({
                    title: 'Lỗi!',
                    text: data.error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .catch(error => {
            Swal.fire({
                title: 'Lỗi!',
                text: 'Đã xảy ra lỗi, vui lòng thử lại.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        });
    });
