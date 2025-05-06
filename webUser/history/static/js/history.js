    // script phàn tìm kiếm biển dáp ứng 90% (chỉ có phần tìm kiếm)
            // document.getElementById('searchInput').addEventListener('input', function() {
            //     const query = this.value;
            //     fetchHistoryData(query, 1);
            // });
            
            // function fetchHistoryData(query, page) {
            //     fetch(`/history/search/?query=${encodeURIComponent(query)}&page=${page}`)
            //         .then(response => response.json())
            //         .then(data => {
            //             const tableBody = document.getElementById('historyTableBody');
            //             tableBody.innerHTML = '';
            
            //             data.histories.forEach((history, index) => {
            //                 const row = document.createElement('tr');
            //                 row.innerHTML = `
            //                     <td>${index + 1}</td>
            //                     <td>${history.license_plate}</td>
            //                     <td>${history.time_in}</td>
            //                     <td>${history.time_out}</td>
            //                     <td>${history.duration}</td>
            //                     <td>${history.fee}</td>
            //                     <td><span class="status-${history.status === 'Đang đỗ' ? 'parking' : history.status === 'Đã thanh toán' ? 'paid' : 'unpaid'}">${history.status}</span></td>
            //                 `;
            //                 tableBody.appendChild(row);
            //             });
            
            //             // Cập nhật phân trang
            //             document.querySelector('.pagination').innerHTML = data.pagination_html || '';
                        
            //             // Thêm sự kiện click cho các nút phân trang mới
            //             document.querySelectorAll('.pagination-btn[data-page]').forEach(btn => {
            //                 btn.addEventListener('click', function(e) {
            //                     e.preventDefault();
            //                     const page = this.getAttribute('data-page');
            //                     const query = document.getElementById('searchInput').value;
            //                     fetchHistoryData(query, page);
            //                 });
            //             });
            //         });
            // }
            
            // // Khởi tạo sự kiện click cho phân trang ban đầu
            // document.querySelectorAll('.pagination-btn[data-page]').forEach(btn => {
            //     btn.addEventListener('click', function(e) {
            //         e.preventDefault();
            //         const page = this.getAttribute('data-page');
            //         const query = document.getElementById('searchInput').value;
            //         fetchHistoryData(query, page);
            //     });
            // });
           




                        
                        // phần tìm kiếm biển số xe và lọc trạng thái
                        // Biến lưu trạng thái hiện tại
                        // let currentState = {
                        //     isSearching: false,
                        //     query: '',
                        //     status: 'all',
                        //     page: 1
                        // };
                        
                        // // Khởi tạo sự kiện khi DOM tải xong
                        // document.addEventListener('DOMContentLoaded', function() {
                        //     // Sự kiện tìm kiếm
                        //     document.getElementById('searchInput').addEventListener('input', function() {
                        //         currentState.query = this.value.trim();
                        //         currentState.isSearching = currentState.query !== '';
                        //         currentState.page = 1; // Reset về trang 1 khi có thay đổi
                                
                        //         if (currentState.isSearching) {
                        //             fetchHistoryData();
                        //         } else {
                        //             // Nếu xóa hết search, tải lại trang gốc
                        //             window.location.href = window.location.pathname;
                        //         }
                        //     });
                        
                        //     // Sự kiện lọc trạng thái
                        //     document.getElementById('statusFilter').addEventListener('change', function() {
                        //         currentState.status = this.value;
                        //         currentState.page = 1; // Reset về trang 1 khi có thay đổi
                        //         fetchHistoryData();
                        //     });
                        
                        //     // Sự kiện nút lọc
                        //     document.getElementById('filterButton').addEventListener('click', function() {
                        //         fetchHistoryData();
                        //     });
                        
                        //     // Gán sự kiện phân trang (sử dụng event delegation)
                        //     document.querySelector('.pagination').addEventListener('click', function(e) {
                        //         const paginationBtn = e.target.closest('.pagination-btn[data-page]');
                        //         if (paginationBtn) {
                        //             e.preventDefault();
                        //             currentState.page = paginationBtn.getAttribute('data-page');
                        //             fetchHistoryData();
                        //         }
                        //     });
                        // });
                        
                        // function fetchHistoryData() {
                        //     let url = `/history/search/?page=${currentState.page}`;
                            
                        //     if (currentState.isSearching) {
                        //         url += `&query=${encodeURIComponent(currentState.query)}`;
                        //     }
                            
                        //     if (currentState.status !== 'all') {
                        //         url += `&status=${currentState.status}`;
                        //     }
                            
                        //     fetch(url)
                        //         .then(response => response.json())
                        //         .then(data => {
                        //             updateTable(data.histories);
                        //             updatePagination(data);
                        //         });
                        // }
                        
                        // function updateTable(histories) {
                        //     const tableBody = document.getElementById('historyTableBody');
                        //     tableBody.innerHTML = '';
                        
                        //     histories.forEach((history, index) => {
                        //         const row = document.createElement('tr');
                        //         row.innerHTML = `
                        //             <td>${index + 1}</td>
                        //             <td>${history.license_plate}</td>
                        //             <td>${history.time_in}</td>
                        //             <td>${history.time_out}</td>
                        //             <td>${history.duration}</td>
                        //             <td>${history.fee}</td>
                        //             <td><span class="status-${history.status === 'Đang đỗ' ? 'parking' : 
                        //                 history.status === 'Đã thanh toán' ? 'paid' : 'unpaid'}">
                        //                 ${history.status}
                        //             </span></td>
                        //         `;
                        //         tableBody.appendChild(row);
                        //     });
                        // }
                        
                        // function updatePagination(data) {
                        //     const paginationContainer = document.querySelector('.pagination');
                            
                        //     if (data.pagination_html) {
                        //         paginationContainer.innerHTML = data.pagination_html;
                        //     } else if (currentState.isSearching || currentState.status !== 'all') {
                        //         // Tạo phân trang đơn giản nếu không có từ server và đang trong chế độ tìm kiếm/lọc
                        //         paginationContainer.innerHTML = `
                        //             <button class="pagination-btn" ${data.current_page == 1 ? 'disabled' : ''}
                        //                 data-page="${data.current_page - 1}">
                        //                 <i class="fas fa-chevron-left"></i>
                        //             </button>
                        //             <button class="pagination-btn active">${data.current_page}</button>
                        //             <button class="pagination-btn" ${!data.has_next ? 'disabled' : ''}
                        //                 data-page="${data.current_page + 1}">
                        //                 <i class="fas fa-chevron-right"></i>
                        //             </button>
                        //         `;
                        //     }
                            
                        //     // Gán lại sự kiện cho các nút phân trang mới
                        //     document.querySelectorAll('.pagination-btn[data-page]').forEach(btn => {
                        //         btn.addEventListener('click', function(e) {
                        //             e.preventDefault();
                        //             currentState.page = this.getAttribute('data-page');
                        //             fetchHistoryData();
                        //         });
                        //     });
                        // }
                    


