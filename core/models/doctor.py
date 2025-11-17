from django.db import models

class Doctor(models.Model):
    GENDER_CHOICES = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    sip_number = models.CharField(max_length=50, blank=True)  # No SIP
    str_number = models.CharField(max_length=50, blank=True)  # No STR
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    specialty = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Working hours
    working_hours_start = models.TimeField(default='08:00')
    working_hours_end = models.TimeField(default='17:00')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.name}"


class DoctorAvailability(models.Model):
    DAY_CHOICES = [
        (0, 'Senin'),
        (1, 'Selasa'),
        (2, 'Rabu'),
        (3, 'Kamis'),
        (4, 'Jumat'),
        (5, 'Sabtu'),
        (6, 'Minggu'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('doctor', 'day_of_week')
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.doctor.name} - {self.get_day_of_week_display()}: {self.start_time}-{self.end_time}"


class DoctorLeave(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.doctor.name} - {self.start_date} to {self.end_date}"
