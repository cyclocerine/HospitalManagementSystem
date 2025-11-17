from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from core.models import (
    Doctor, Patient, MedicalRecord, Schedule, 
    Inpatient, Room, Medicine, Prescription, Payment,
    DoctorAvailability, DoctorLeave
)
from datetime import datetime, timedelta
from .forms import (
    LoginForm, PatientRegistrationForm, DoctorRegistrationForm, 
    AppointmentBookingForm, PaymentForm, AppointmentConfirmationForm,
    MedicalRecordDiagnosisForm, PatientProfileUpdateForm, DoctorProfileUpdateForm,
    ChangePasswordForm, DoctorAvailabilityForm, DoctorLeaveForm
)
from .emails import (
    send_appointment_confirmation_email, send_appointment_rejection_email,
    send_appointment_reminder_email, send_payment_confirmation_email,
    send_payment_reminder_email
)
from .utils import paginate_queryset


# ==================== AUTHENTICATION VIEWS ====================

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Login view untuk pasien dan dokter"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Login gagal. Periksa username dan password Anda.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def register_patient_view(request):
    """Register view untuk pasien"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Selamat datang di rumah sakit kami.')
            return redirect('patient_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'accounts/register_patient.html', {'form': form})


@require_http_methods(["GET", "POST"])
def register_doctor_view(request):
    """Register view untuk dokter"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi dokter berhasil! Selamat datang di sistem rumah sakit.')
            return redirect('doctor_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'accounts/register_doctor.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    """Logout view untuk semua user"""
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('home')


# ==================== DASHBOARD REDIRECT ====================

@login_required(login_url='login')
def dashboard_redirect(request):
    """Redirect ke dashboard sesuai role user"""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        return redirect('patient_dashboard')
    return redirect('home')


# ==================== ADMIN DASHBOARD ====================

@login_required(login_url='login')
def admin_dashboard(request):
    """Dashboard untuk admin"""
    if request.user.role != 'admin':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('dashboard')
    
    # Statistik
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_inpatients = Inpatient.objects.filter(discharge_date__isnull=True).count()
    total_rooms = Room.objects.count()
    
    # Data terbaru
    recent_records = MedicalRecord.objects.select_related('patient', 'doctor').order_by('-examination_date')[:5]
    recent_inpatients = Inpatient.objects.select_related('patient', 'room').order_by('-admission_date')[:5]
    
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_inpatients': total_inpatients,
        'total_rooms': total_rooms,
        'recent_records': recent_records,
        'recent_inpatients': recent_inpatients,
    }
    return render(request, 'dashboards/admin.html', context)


# ==================== DOCTOR DASHBOARD ====================

@login_required(login_url='login')
def doctor_dashboard(request):
    """Dashboard untuk dokter"""
    if request.user.role != 'doctor':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('dashboard')
    
    # Ambil dokter profile
    try:
        doctor = request.user.doctor_profile
    except:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    if not doctor:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    # Statistik
    total_patients = MedicalRecord.objects.filter(doctor=doctor).values('patient').distinct().count()
    total_records = MedicalRecord.objects.filter(doctor=doctor).count()
    
    # Jadwal hari ini
    today = datetime.now().date()
    today_schedule = Schedule.objects.filter(
        doctor=doctor,
        examination_date=today
    ).order_by('examination_time')
    
    # Jadwal minggu ini
    week_start = today
    week_end = today + timedelta(days=7)
    week_schedule = Schedule.objects.filter(
        doctor=doctor,
        examination_date__range=[week_start, week_end]
    ).order_by('examination_date', 'examination_time')
    
    # Rekam medis terbaru
    recent_records = MedicalRecord.objects.filter(doctor=doctor).select_related('patient').order_by('-examination_date')[:5]
    
    # Resep terbaru
    recent_prescriptions = Prescription.objects.filter(
        medical_record__doctor=doctor
    ).select_related('medical_record', 'medicine').order_by('-prescription_date')[:5]
    
    # Pasien yang perlu follow-up
    pending_patients = MedicalRecord.objects.filter(
        doctor=doctor,
        diagnosis__isnull=False,
        treatment__isnull=True
    ).select_related('patient').order_by('-examination_date')[:5]
    
    context = {
        'doctor': doctor,
        'total_patients': total_patients,
        'total_records': total_records,
        'today_schedule': today_schedule,
        'week_schedule': week_schedule,
        'recent_records': recent_records,
        'recent_prescriptions': recent_prescriptions,
        'pending_patients': pending_patients,
        'today': today,
    }
    return render(request, 'dashboards/doctor.html', context)


# ==================== APPOINTMENT BOOKING ====================

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def book_appointment(request):
    """View untuk booking appointment"""
    if request.user.role != 'patient':
        messages.error(request, 'Hanya pasien yang bisa booking appointment.')
        return redirect('home')
    
    try:
        patient = request.user.patient_profile
    except:
        messages.error(request, 'Profil pasien tidak ditemukan.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            # Buat appointment
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = 'pending'
            appointment.save()
            
            messages.success(
                request, 
                f'Janji temu dengan {appointment.doctor.name} berhasil dibuat! '
                f'Tanggal: {appointment.examination_date.strftime("%d-%m-%Y")}, '
                f'Waktu: {appointment.examination_time.strftime("%H:%M")}'
            )
            return redirect('patient_dashboard')
        else:
            for field, errors in form.errors.items():
                if field == '__all__':
                    for error in errors:
                        messages.error(request, str(error))
                else:
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        form = AppointmentBookingForm()
    
    context = {
        'form': form,
        'page_title': 'Booking Janji Temu'
    }
    return render(request, 'accounts/book_appointment.html', context)


# ==================== PAYMENT & BILLING ====================

@login_required(login_url='login')
def patient_bills(request):
    """View untuk melihat tagihan pasien"""
    if request.user.role != 'patient':
        messages.error(request, 'Hanya pasien yang bisa melihat tagihan.')
        return redirect('home')
    
    try:
        patient = request.user.patient_profile
    except:
        messages.error(request, 'Profil pasien tidak ditemukan.')
        return redirect('home')
    
    # Ambil semua pembayaran pasien
    all_payments = Payment.objects.filter(patient=patient).order_by('-created_at')
    
    # Statistik
    total_amount = sum([p.amount for p in all_payments])
    total_paid = sum([p.paid_amount for p in all_payments])
    pending_amount = total_amount - total_paid
    
    # Filter berdasarkan status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        all_payments = all_payments.filter(status=status_filter)
    
    context = {
        'payments': all_payments,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'pending_amount': pending_amount,
        'status_filter': status_filter,
        'page_title': 'Tagihan Saya'
    }
    return render(request, 'accounts/patient_bills.html', context)


@login_required(login_url='login')
def payment_detail(request, payment_id):
    """View untuk detail pembayaran dan melakukan pembayaran"""
    if request.user.role != 'patient':
        messages.error(request, 'Hanya pasien yang bisa mengakses halaman ini.')
        return redirect('home')
    
    try:
        patient = request.user.patient_profile
        payment = Payment.objects.get(id=payment_id, patient=patient)
    except Payment.DoesNotExist:
        messages.error(request, 'Pembayaran tidak ditemukan.')
        return redirect('patient_bills')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            # Update pembayaran
            paid_amount = form.cleaned_data.get('paid_amount')
            old_paid = payment.paid_amount
            payment.paid_amount += paid_amount
            payment.method = form.cleaned_data.get('method')
            payment.notes = form.cleaned_data.get('notes')
            
            # Update status
            if payment.paid_amount >= payment.amount:
                payment.status = 'paid'
                payment.payment_date = timezone.now()
            else:
                payment.status = 'partial'
            
            payment.save()
            
            # Send payment confirmation email
            send_payment_confirmation_email(payment.patient, payment)
            
            messages.success(
                request,
                f'Pembayaran sebesar Rp{paid_amount:,.0f} berhasil dicatat! '
                f'Sisa pembayaran: Rp{payment.remaining_amount:,.0f}. Email konfirmasi telah dikirim.'
            )
            return redirect('patient_bills')
    else:
        form = PaymentForm()
    
    context = {
        'payment': payment,
        'form': form,
        'page_title': f'Detail Pembayaran {payment.invoice_number}'
    }
    return render(request, 'accounts/payment_detail.html', context)


# ==================== APPOINTMENT CONFIRMATION ====================

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def doctor_appointments(request):
    """View untuk dokter melihat daftar appointment yang perlu dikonfirmasi"""
    if request.user.role != 'doctor':
        messages.error(request, 'Hanya dokter yang bisa mengakses halaman ini.')
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
    except:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Appointment yang menunggu konfirmasi
    pending_appointments = MedicalRecord.objects.filter(
        doctor=doctor,
        confirmation_status='pending'
    ).select_related('patient').order_by('-created_at')
    
    if search_query:
        pending_appointments = pending_appointments.filter(
            patient__name__icontains=search_query
        )
    
    # Paginate pending appointments
    pending_paginated = paginate_queryset(pending_appointments, request, items_per_page=10)
    
    # Appointment yang sudah dikonfirmasi
    confirmed_appointments = MedicalRecord.objects.filter(
        doctor=doctor,
        confirmation_status='approved'
    ).select_related('patient').order_by('-examination_date')[:10]
    
    # Appointment yang ditolak
    rejected_appointments = MedicalRecord.objects.filter(
        doctor=doctor,
        confirmation_status='rejected'
    ).select_related('patient').order_by('-created_at')[:5]
    
    context = {
        'doctor': doctor,
        'pending_appointments': pending_paginated['items'],
        'page_obj': pending_paginated['page_obj'],
        'paginator': pending_paginated['paginator'],
        'is_paginated': pending_paginated['is_paginated'],
        'confirmed_appointments': confirmed_appointments,
        'rejected_appointments': rejected_appointments,
        'pending_count': MedicalRecord.objects.filter(
            doctor=doctor,
            confirmation_status='pending'
        ).count(),
        'search_query': search_query,
        'page_title': 'Konfirmasi Appointment'
    }
    return render(request, 'accounts/doctor_appointments.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def confirm_appointment(request, appointment_id):
    """View untuk dokter approve/reject appointment"""
    if request.user.role != 'doctor':
        messages.error(request, 'Hanya dokter yang bisa mengakses halaman ini.')
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
        appointment = MedicalRecord.objects.get(id=appointment_id, doctor=doctor)
    except MedicalRecord.DoesNotExist:
        messages.error(request, 'Appointment tidak ditemukan.')
        return redirect('doctor_appointments')
    
    if request.method == 'POST':
        form = AppointmentConfirmationForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            if appointment.confirmation_status == 'approved':
                appointment.status = 'confirmed'
                # Send confirmation email
                send_appointment_confirmation_email(
                    appointment.patient,
                    appointment.doctor,
                    appointment
                )
                messages.success(
                    request,
                    f'Appointment untuk {appointment.patient.name} pada '
                    f'{appointment.examination_date.strftime("%d-%m-%Y")} '
                    f'{appointment.examination_time.strftime("%H:%M")} telah disetujui. Email notifikasi telah dikirim.'
                )
            else:
                # Send rejection email
                send_appointment_rejection_email(
                    appointment.patient,
                    appointment.doctor,
                    appointment,
                    appointment.rejection_reason
                )
                messages.warning(
                    request,
                    f'Appointment untuk {appointment.patient.name} telah ditolak. Email notifikasi telah dikirim.'
                )
            
            appointment.save()
            return redirect('doctor_appointments')
    else:
        form = AppointmentConfirmationForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
        'patient': appointment.patient,
        'page_title': f'Konfirmasi Appointment - {appointment.patient.name}'
    }
    return render(request, 'accounts/confirm_appointment.html', context)


# ==================== MEDICAL RECORD DIAGNOSIS ====================

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def add_diagnosis(request, appointment_id):
    """View untuk dokter menambahkan diagnosis dan treatment"""
    if request.user.role != 'doctor':
        messages.error(request, 'Hanya dokter yang bisa mengakses halaman ini.')
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
        appointment = MedicalRecord.objects.get(id=appointment_id, doctor=doctor, confirmation_status='approved')
    except MedicalRecord.DoesNotExist:
        messages.error(request, 'Appointment tidak ditemukan atau belum dikonfirmasi.')
        return redirect('doctor_appointments')
    
    if request.method == 'POST':
        form = MedicalRecordDiagnosisForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(
                request,
                f'Diagnosis dan rencana pengobatan untuk {appointment.patient.name} berhasil disimpan.'
            )
            return redirect('doctor_appointments')
    else:
        form = MedicalRecordDiagnosisForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
        'patient': appointment.patient,
        'page_title': f'Tambah Diagnosis - {appointment.patient.name}'
    }
    return render(request, 'accounts/add_diagnosis.html', context)


# ==================== PROFILE MANAGEMENT ====================

@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """View untuk melihat dan edit profil user"""
    if request.user.role == 'patient':
        return patient_profile_view(request)
    elif request.user.role == 'doctor':
        return doctor_profile_view(request)
    else:
        messages.error(request, 'Akses ditolak.')
        return redirect('home')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def patient_profile_view(request):
    """View untuk profil pasien"""
    if request.method == 'POST':
        form = PatientProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('profile')
    else:
        form = PatientProfileUpdateForm(instance=request.user)
    
    patient = request.user.patient_profile
    context = {
        'form': form,
        'patient': patient,
        'page_title': 'Profil Saya'
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def doctor_profile_view(request):
    """View untuk profil dokter"""
    if request.method == 'POST':
        form = DoctorProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('profile')
    else:
        form = DoctorProfileUpdateForm(instance=request.user)
    
    doctor = request.user.doctor_profile
    context = {
        'form': form,
        'doctor': doctor,
        'page_title': 'Profil Saya'
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def change_password(request):
    """View untuk change password"""
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password berhasil diubah!')
                return redirect('profile')
            else:
                messages.error(request, 'Password lama tidak sesuai.')
    else:
        form = ChangePasswordForm()
    
    context = {
        'form': form,
        'page_title': 'Ubah Password'
    }
    return render(request, 'accounts/change_password.html', context)


# ==================== DOCTOR AVAILABILITY ====================

@login_required(login_url='login')
@require_http_methods(["GET"])
def doctor_availability_view(request):
    """View untuk dokter mengatur jadwal kerja"""
    if request.user.role != 'doctor':
        messages.error(request, 'Hanya dokter yang bisa mengakses halaman ini.')
        return redirect('dashboard')
    
    try:
        doctor = request.user.doctor_profile
    except:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    availabilities = DoctorAvailability.objects.filter(doctor=doctor).order_by('day_of_week')
    leaves = DoctorLeave.objects.filter(doctor=doctor).order_by('-start_date')
    
    context = {
        'doctor': doctor,
        'availabilities': availabilities,
        'leaves': leaves,
        'page_title': 'Atur Jadwal Kerja'
    }
    return render(request, 'accounts/doctor_availability.html', context)

