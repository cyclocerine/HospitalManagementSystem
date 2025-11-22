from django.db import models
from .medical_record import MedicalRecord
from .patient import Patient
from django.utils import timezone

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash / Tunai'),
        ('transfer', 'Transfer Bank'),
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
        ('bpjs', 'BPJS'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu Pembayaran'),
        ('paid', 'Sudah Dibayar'),
        ('partial', 'Pembayaran Sebagian'),
        ('overdue', 'Terlambat'),
        ('cancelled', 'Dibatalkan'),
    ]

    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    service_name = models.CharField(max_length=255, blank=True, default='Konsultasi Medis')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    invoice_number = models.CharField(max_length=50, unique=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Generate invoice number jika belum ada"""
        if not self.invoice_number:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.invoice_number = f"INV-{timestamp}-{self.patient_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        patient_name = self.patient.name if self.patient else "Unknown Patient"
        return f"INV-{self.invoice_number} | {patient_name} - Rp{self.amount:,.0f}"
    
    @property
    def remaining_amount(self):
        """Hitung sisa pembayaran"""
        return self.amount - self.paid_amount
    
    @property
    def is_overdue(self):
        """Cek apakah sudah jatuh tempo"""
        if self.due_date and self.status == 'pending':
            return timezone.now().date() > self.due_date
        return False


