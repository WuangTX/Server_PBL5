from django.db import models
# Create your models here.


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    history = models.OneToOneField('history.History', on_delete=models.CASCADE, related_name='payment')
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)  # False = chưa thanh toán, True = đã thanh toán
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status_str = "Đã thanh toán" if self.status else "Chưa thanh toán"
        return f"Thanh toán cho History #{self.history.id} - {status_str}"
    class Meta:
        db_table = 'payments'