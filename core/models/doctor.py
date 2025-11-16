from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    sip_number = models.CharField(max_length=50, blank=True)  # No SIP
    str_number = models.CharField(max_length=50, blank=True)  # No STR
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    specialty = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.name}"