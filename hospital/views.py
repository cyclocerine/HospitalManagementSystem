# hospital/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Doctor, MedicalRecord, Prescription, Inpatient, Schedule, Patient
from datetime import datetime

def home(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def patient_dashboard(request):
    """Dashboard untuk pasien"""
    if request.user.role != 'patient':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('home')
    
    # Ambil patient profile
    try:
        patient = request.user.patient_profile
    except:
        patient = None
    
    if not patient:
        messages.error(request, 'Profil pasien tidak ditemukan.')
        return redirect('home')
    
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        if doctor_id and date:
            doctor = Doctor.objects.get(id=doctor_id)
            MedicalRecord.objects.create(
                patient=patient,
                doctor=doctor,
                examination_date=date,
                diagnosis="",
                treatment=""
            )
            messages.success(request, 'Janji temu berhasil dibuat! Dokter akan menghubungi Anda.')
            return redirect('patient_dashboard')
    
    # Statistik
    total_records = MedicalRecord.objects.filter(patient=patient).count()
    total_prescriptions = Prescription.objects.filter(
        medical_record__patient=patient
    ).count()
    inpatient_status = Inpatient.objects.filter(
        patient=patient,
        discharge_date__isnull=True
    ).first()
    
    # Rekam medis
    medical_records = MedicalRecord.objects.filter(
        patient=patient
    ).select_related('doctor').order_by('-examination_date')[:10]
    
    # Resep
    prescriptions = Prescription.objects.filter(
        medical_record__patient=patient
    ).select_related('medical_record', 'medicine').order_by('-prescription_date')[:5]
    
    # Dokter tersedia
    doctors = Doctor.objects.all()
    
    context = {
        'patient': patient,
        'total_records': total_records,
        'total_prescriptions': total_prescriptions,
        'inpatient_status': inpatient_status,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'doctors': doctors,
    }
    return render(request, 'dashboards/patient.html', context)


@login_required(login_url='login')
def doctor_patient_list(request):
    """View untuk dokter melihat list pasien yang pernah berobat"""
    if request.user.role != 'doctor':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('home')
    
    # Ambil dokter profile
    try:
        doctor = request.user.doctor_profile
    except:
        doctor = None
    
    if not doctor:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    # Ambil semua pasien yang pernah diperiksa dokter
    patients = Patient.objects.filter(
        medicalrecord__doctor=doctor
    ).distinct().order_by('name')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        patients = patients.filter(name__icontains=search_query)
    
    context = {
        'doctor': doctor,
        'patients': patients,
        'search_query': search_query,
        'total_patients': patients.count(),
    }
    return render(request, 'doctor/patient_list.html', context)


@login_required(login_url='login')
def doctor_patient_detail(request, patient_id):
    """View untuk dokter melihat detail rekam medis pasien"""
    if request.user.role != 'doctor':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('home')
    
    # Ambil dokter profile
    try:
        doctor = request.user.doctor_profile
    except:
        doctor = None
    
    if not doctor:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    # Ambil pasien
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Cek apakah dokter pernah memeriksa pasien
    if not MedicalRecord.objects.filter(patient=patient, doctor=doctor).exists():
        messages.error(request, 'Anda tidak memiliki akses ke data pasien ini.')
        return redirect('doctor_patient_list')
    
    # Rekam medis pasien untuk dokter ini
    medical_records = MedicalRecord.objects.filter(
        patient=patient,
        doctor=doctor
    ).order_by('-examination_date')
    
    # Semua resep untuk pasien dari dokter ini
    prescriptions = Prescription.objects.filter(
        medical_record__patient=patient,
        medical_record__doctor=doctor
    ).select_related('medical_record', 'medicine').order_by('-prescription_date')
    
    # Status rawat inap terkini
    inpatient = Inpatient.objects.filter(
        patient=patient,
        discharge_date__isnull=True
    ).first()
    
    context = {
        'doctor': doctor,
        'patient': patient,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'inpatient': inpatient,
        'total_visits': medical_records.count(),
    }
    return render(request, 'doctor/patient_detail.html', context)


@login_required(login_url='login')
def doctor_patient_appointments(request):
    """View untuk dokter melihat janji temu pasien"""
    if request.user.role != 'doctor':
        messages.error(request, 'Anda tidak memiliki akses ke halaman ini.')
        return redirect('home')
    
    # Ambil dokter profile
    try:
        doctor = request.user.doctor_profile
    except:
        doctor = None
    
    if not doctor:
        messages.error(request, 'Profil dokter tidak ditemukan.')
        return redirect('home')
    
    # Ambil jadwal pasien yang akan diperiksa dokter ini
    appointments = MedicalRecord.objects.filter(
        doctor=doctor
    ).select_related('patient').order_by('-examination_date')
    
    # Filter berdasarkan status (belum diperiksa/sudah diperiksa)
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        appointments = appointments.filter(diagnosis__isnull=True)
    elif status_filter == 'completed':
        appointments = appointments.filter(diagnosis__isnull=False)
    
    # Search pasien
    search_query = request.GET.get('q', '')
    if search_query:
        appointments = appointments.filter(patient__name__icontains=search_query)
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'status_filter': status_filter,
        'search_query': search_query,
        'pending_count': MedicalRecord.objects.filter(
            doctor=doctor,
            diagnosis__isnull=True
        ).count(),
        'completed_count': MedicalRecord.objects.filter(
            doctor=doctor,
            diagnosis__isnull=False
        ).count(),
    }
    return render(request, 'doctor/appointments.html', context)