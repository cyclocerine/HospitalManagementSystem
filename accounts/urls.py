# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from hospital.views import patient_dashboard

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_patient_view, name='register_patient'),
    path('register-doctor/', views.register_doctor_view, name='register_doctor'),
    path('logout/', views.logout_view, name='logout'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Appointment
    path('appointment/book/', views.book_appointment, name='book_appointment'),
    path('appointment/confirm/', views.doctor_appointments, name='doctor_appointments'),
    path('appointment/<int:appointment_id>/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('appointment/<int:appointment_id>/diagnosis/', views.add_diagnosis, name='add_diagnosis'),
    
    # Billing & Payment
    path('bills/', views.patient_bills, name='patient_bills'),
    path('payment/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    
    # Profile Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/patient/', views.patient_profile_view, name='patient_profile'),
    path('profile/doctor/', views.doctor_profile_view, name='doctor_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Doctor Availability
    path('doctor/availability/', views.doctor_availability_view, name='doctor_availability'),
    
    # Dashboards
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/patient/', patient_dashboard, name='patient_dashboard'),
]
