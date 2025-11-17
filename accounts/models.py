# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin Rumah Sakit'),
        ('doctor', 'Dokter'),
        ('patient', 'Pasien'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    
    # Foreign key ke model Patient dan Doctor di core
    patient_profile = models.OneToOneField(
        'core.Patient', 
        null=True, blank=True, 
        on_delete=models.CASCADE,
        related_name='user_account'
    )
    doctor_profile = models.OneToOneField(
        'core.Doctor', 
        null=True, blank=True, 
        on_delete=models.CASCADE,
        related_name='user_account'
    )

    # Override groups dan user_permissions untuk menghindari clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_accounts',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_accounts',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
