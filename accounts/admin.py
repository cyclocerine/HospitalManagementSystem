from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('Informasi Login', {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Profil', {'fields': ('role', 'patient_profile', 'doctor_profile')}),
        ('Izin Akses', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tanggal', {'fields': ('last_login', 'date_joined')}),
    )
