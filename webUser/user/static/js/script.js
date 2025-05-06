document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });

    // Payment method selection
    const paymentOptions = document.querySelectorAll('.payment-option input[type="radio"]');
    paymentOptions.forEach(option => {
        option.addEventListener('change', function() {
            // Hide all payment details
            document.querySelectorAll('.payment-details').forEach(detail => {
                detail.classList.remove('active');
            });
            
            // Show selected payment details
            const detailsId = this.id + 'Details';
            const details = document.getElementById(detailsId);
            if (details) {
                details.classList.add('active');
            }
        });
    });

    // Login form submission
    // const loginForm = document.getElementById('loginForm');
    // if (loginForm) {
    //     loginForm.addEventListener('submit', function(e) {
    //         e.preventDefault();
            
    //         const email = document.getElementById('email').value;
    //         const password = document.getElementById('password').value;
            
    //         // Simple validation
    //         if (!email || !password) {
    //             alert('Vui lòng nhập đầy đủ thông tin đăng nhập!');
    //             return;
    //         }
            
    //         // Simulate login success
    //         alert('Đăng nhập thành công!!!!');
    //         // In a real application, you would send this data to the server
    //         // window.location.href = 'index.html';
    //     });
    // }

    // Registration form submission
    // const registerForm = document.getElementById('registerForm');
    // if (registerForm) {
    //     registerForm.addEventListener('submit', function(e) {
    //         e.preventDefault();
            
    //         const fullName = document.getElementById('fullName').value;
    //         const email = document.getElementById('regEmail').value;
    //         const phone = document.getElementById('phone').value;
    //         const password = document.getElementById('regPassword').value;
    //         const confirmPassword = document.getElementById('confirmPassword').value;
    //         const termsAgree = document.getElementById('termsAgree').checked;
            
    //         // Simple validation
    //         if (!fullName || !email || !phone || !password || !confirmPassword) {
    //             alert('Vui lòng nhập đầy đủ thông tin đăng ký!');
    //             return;
    //         }
            
    //         if (password !== confirmPassword) {
    //             alert('Mật khẩu xác nhận không khớp!');
    //             return;
    //         }
            
    //         if (!termsAgree) {
    //             alert('Vui lòng đồng ý với điều khoản dịch vụ!');
    //             return;
    //         }
            
    //         // Simulate registration success
    //         alert('Đăng ký thành công! Vui lòng đăng nhập.');
    //         // In a real application, you would send this data to the server
    //         // window.location.href = 'login.html';
    //     });
    // }

    // History page filtering
    // const filterButton = document.getElementById('filterButton');
    // if (filterButton) {
    //     filterButton.addEventListener('click', function() {
    //         const timeFilter = document.getElementById('timeFilter').value;
    //         const statusFilter = document.getElementById('statusFilter').value;
    //         const searchInput = document.getElementById('searchInput').value.toLowerCase();
            
    //         // In a real application, you would send these filters to the server
    //         // and update the table with the filtered results
    //         alert(`Đang lọc: Thời gian - ${timeFilter}, Trạng thái - ${statusFilter}, Tìm kiếm - ${searchInput}`);
    //     });
    // }

    // Vehicle search in payment page
    // const searchVehicleBtn = document.getElementById('searchVehicleBtn');
    // if (searchVehicleBtn) {
    //     searchVehicleBtn.addEventListener('click', function() {
    //         const vehicleSearch = document.getElementById('vehicleSearch').value;
            
    //         if (!vehicleSearch) {
    //             alert('Vui lòng nhập biển số xe!');
    //             return;
    //         }
            
    //         // In a real application, you would send this search to the server
    //         // and update the vehicle details with the results
    //         alert(`Đang tìm kiếm xe với biển số: ${vehicleSearch}`);
            
    //         // Show vehicle details (this would normally happen after a successful search)
    //         const vehicleDetails = document.getElementById('vehicleDetails');
    //         if (vehicleDetails) {
    //             vehicleDetails.style.display = 'block';
    //         }
    //     });
    // }

    

    // Update current time in payment page
    // const currentTimeElement = document.getElementById('currentTime');
    // if (currentTimeElement) {
    //     const updateCurrentTime = () => {
    //         const now = new Date();
    //         const day = String(now.getDate()).padStart(2, '0');
    //         const month = String(now.getMonth() + 1).padStart(2, '0');
    //         const year = now.getFullYear();
    //         const hours = String(now.getHours()).padStart(2, '0');
    //         const minutes = String(now.getMinutes()).padStart(2, '0');
            
    //         currentTimeElement.textContent = `${day}/${month}/${year} ${hours}:${minutes}`;
    //     };
        
    //     updateCurrentTime();
    //     setInterval(updateCurrentTime, 60000); // Update every minute
    // }

    // Pagination buttons
    // const paginationButtons = document.querySelectorAll('.pagination-btn');
    // paginationButtons.forEach(button => {
    //     if (!button.disabled) {
    //         button.addEventListener('click', function() {
    //             // Remove active class from all buttons
    //             paginationButtons.forEach(btn => btn.classList.remove('active'));
                
    //             // Add active class to clicked button
    //             this.classList.add('active');
                
    //             // In a real application, you would load the corresponding page data
    //             // For now, we'll just show an alert
    //             const page = this.textContent;
    //             if (page !== '<' && page !== '>') {
    //                 alert(`Đang chuyển đến trang ${page}`);
    //             }
    //         });
    //     }
    // });
});