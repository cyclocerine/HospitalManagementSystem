from django.db import models
from .patient import Patient
from .doctor import Doctor

class MedicalRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('confirmed', 'Terkonfirmasi'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    CONFIRMATION_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    examination_date = models.DateField()
    examination_time = models.TimeField(null=True, blank=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmation_status = models.CharField(max_length=20, choices=CONFIRMATION_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"MR-{self.id} | {self.patient.name} - {self.status}"
