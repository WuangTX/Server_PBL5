from django.db import models
# Create your models here.

class History(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey('user.Vehicle', on_delete=models.CASCADE, related_name='histories', null=False, blank=True)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Lịch sử gửi xe của {self.vehicle.license_plate} lúc {self.time_in}"
    
    class Meta:
        db_table = 'histories'

    def get_parking_duration(self):
            """Tính thời gian đỗ, trả về dạng 'X giờ Y phút'."""
            if not self.time_out:
                return 0, 0
            
            # Tính khoảng thời gian đỗ
            duration = self.time_out - self.time_in
            
            # Chuyển đổi sang giây
            total_seconds = duration.total_seconds()
            
            # Tính số giờ và phút
            hours = int(total_seconds // 3600)  # Số giây chia 3600 để ra giờ
            minutes = int((total_seconds % 3600) // 60)  # Số giây còn lại chia 60 để ra phút
            
            return int(hours), int(minutes)

    def calculate_fee(self):
            """Tính phí dựa trên thời gian đỗ, với 167 VNĐ/phút."""
            if not self.time_out:
                return 0  # Nếu chưa có time_out, trả về 0
            
            # Tính khoảng thời gian đỗ
            duration = self.time_out - self.time_in
            
            # Tính tổng số phút
            total_minutes = duration.total_seconds() // 60
            
            # Tính phí: số phút × 167 VNĐ
            fee = int(total_minutes * 167)
            
            return fee