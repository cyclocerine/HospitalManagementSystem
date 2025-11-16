from django.db import models
from .medical_record import MedicalRecord
from .medicine import Medicine

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    prescription_date = models.DateField()
    dosage = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Resep untuk {self.medical_record.patient.name}"