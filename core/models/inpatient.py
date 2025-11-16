from django.db import models
from .patient import Patient
from .room import Room

class Inpatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    diagnosis = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rawat Inap: {self.patient.name}"