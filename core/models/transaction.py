from django.db import models
from .medical_record import MedicalRecord
from .payment import Payment

class MedicalTransaction(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    details = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaksi MR-{self.medical_record.id}"