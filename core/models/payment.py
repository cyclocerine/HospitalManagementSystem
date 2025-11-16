from django.db import models

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Transfer Bank', 'Transfer Bank'),
        ('Debit Card', 'Debit Card'),
        ('BPJS', 'BPJS'),
    ]

    payment_date = models.DateField()
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pembayaran {self.id} - {self.method}"