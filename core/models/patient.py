from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]
    BLOOD_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ]

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES, blank=True)
    bpjs_status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name