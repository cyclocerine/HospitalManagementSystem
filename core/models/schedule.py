from django.db import models
from .doctor import Doctor

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('available', 'Tersedia'),
        ('booked', 'Terbooking'),
        ('unavailable', 'Tidak Tersedia'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    examination_date = models.DateField()
    examination_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'examination_date', 'examination_time')
        ordering = ['examination_date', 'examination_time']

    def __str__(self):
        return f"{self.doctor.name} - {self.examination_date} {self.examination_time} ({self.status})"
