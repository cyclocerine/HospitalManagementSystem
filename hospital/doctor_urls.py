# hospital/doctor_urls.py
from django.urls import path
from .views import (
    doctor_patient_list,
    doctor_patient_detail,
    doctor_patient_appointments,
)

app_name = 'doctor'

urlpatterns = [
    path('patients/', doctor_patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', doctor_patient_detail, name='patient_detail'),
    path('appointments/', doctor_patient_appointments, name='appointments'),
]
