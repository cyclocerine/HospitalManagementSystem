from django.db import models
from .patient import Patient
from .doctor import Doctor

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    examination_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"MR-{self.id} | {self.patient.name}"