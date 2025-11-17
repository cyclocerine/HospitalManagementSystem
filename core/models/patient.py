from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
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
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES, blank=True)
    bpjs_status = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.name