from django.db import models
from .doctor import Doctor

class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    examination_date = models.DateField()
    examination_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.examination_date} {self.examination_time}"