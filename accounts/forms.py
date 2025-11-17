from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta
from .models import User
from core.models import Patient, Doctor, MedicalRecord, Schedule, Payment, DoctorAvailability, DoctorLeave


class LoginForm(forms.Form):
    """Form untuk login user (pasien atau dokter)"""
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan username Anda',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan password Anda',
            'autocomplete': 'current-password'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Username atau password salah."
                )
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache if hasattr(self, 'user_cache') else None


class PatientRegistrationForm(UserCreationForm):
    """Form untuk registrasi pasien"""
    
    # User fields
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan username',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan email Anda',
            'autocomplete': 'email'
        })
    )
    first_name = forms.CharField(
        label="Nama Depan",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nama depan'
        })
    )
    last_name = forms.CharField(
        label="Nama Belakang",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nama belakang'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan password (min 8 karakter)',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Konfirmasi Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Konfirmasi password Anda',
            'autocomplete': 'new-password'
        })
    )
    
    # Patient profile fields
    phone = forms.CharField(
        label="Nomor Telepon",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '081234567890',
            'type': 'tel'
        })
    )
    date_of_birth = forms.DateField(
        label="Tanggal Lahir",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    GENDER_CHOICES = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    gender = forms.ChoiceField(
        label="Jenis Kelamin",
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600'
        })
    )
    BLOOD_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ]
    blood_type = forms.ChoiceField(
        label="Golongan Darah",
        choices=BLOOD_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    address = forms.CharField(
        label="Alamat",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan alamat lengkap Anda',
            'rows': 3
        })
    )
    bpjs_status = forms.BooleanField(
        label="Saya memiliki BPJS",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 rounded cursor-pointer'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text from password fields
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Customize username help text
        self.fields['username'].help_text = ''
    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if phone and len(phone) < 10:
            self.add_error('phone', "Nomor telepon minimal 10 digit")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Kata sandi tidak cocok.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        user.role = 'patient'
        
        if commit:
            user.save()
            
            # Create patient profile
            patient = Patient.objects.create(
                name=f"{user.first_name} {user.last_name}".strip(),
                phone=self.cleaned_data.get('phone'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                blood_type=self.cleaned_data.get('blood_type') or '',
                address=self.cleaned_data.get('address') or '',
                bpjs_status=self.cleaned_data.get('bpjs_status', False)
            )
            user.patient_profile = patient
            user.save()
        
        return user


class DoctorRegistrationForm(UserCreationForm):
    """Form untuk registrasi dokter"""
    
    # User fields
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan username',
            'autocomplete': 'username'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan email Anda',
            'autocomplete': 'email'
        })
    )
    first_name = forms.CharField(
        label="Nama Depan",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nama depan'
        })
    )
    last_name = forms.CharField(
        label="Nama Belakang",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nama belakang'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan password (min 8 karakter)',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        label="Konfirmasi Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Konfirmasi password Anda',
            'autocomplete': 'new-password'
        })
    )
    
    # Doctor profile fields
    phone = forms.CharField(
        label="Nomor Telepon",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '081234567890',
            'type': 'tel'
        })
    )
    date_of_birth = forms.DateField(
        label="Tanggal Lahir",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    GENDER_CHOICES = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    gender = forms.ChoiceField(
        label="Jenis Kelamin",
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600'
        })
    )
    specialty = forms.CharField(
        label="Spesialisasi",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Contoh: Umum, Gigi, Anak, dll'
        })
    )
    sip_number = forms.CharField(
        label="No. SIP (Opsional)",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nomor Surat Izin Praktik'
        })
    )
    str_number = forms.CharField(
        label="No. STR (Opsional)",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Nomor Sertifikat Tanda Registrasi'
        })
    )
    position = forms.CharField(
        label="Posisi",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Contoh: Dokter Spesialis, Dokter Umum, dll'
        })
    )
    unit = forms.CharField(
        label="Unit / Departemen",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Contoh: Poliklinik Umum, IGD, Kamar Bersalin, dll'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if phone and len(phone) < 10:
            self.add_error('phone', "Nomor telepon minimal 10 digit")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Kata sandi tidak cocok.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        user.role = 'doctor'
        
        if commit:
            user.save()
            
            # Create doctor profile
            doctor = Doctor.objects.create(
                name=f"{user.first_name} {user.last_name}".strip(),
                email=user.email,
                phone=self.cleaned_data.get('phone'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                specialty=self.cleaned_data.get('specialty'),
                sip_number=self.cleaned_data.get('sip_number') or '',
                str_number=self.cleaned_data.get('str_number') or '',
                position=self.cleaned_data.get('position'),
                unit=self.cleaned_data.get('unit'),
                monthly_salary=0  # Will be set by admin
            )
            user.doctor_profile = doctor
            user.save()
        
        return user


class AppointmentBookingForm(forms.ModelForm):
    """Form untuk booking appointment"""
    
    doctor = forms.ModelChoiceField(
        label="Dokter",
        queryset=Doctor.objects.all().order_by('name'),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    examination_date = forms.DateField(
        label="Tanggal Pemeriksaan",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    
    examination_time = forms.TimeField(
        label="Waktu Pemeriksaan",
        widget=forms.TimeInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'time'
        })
    )
    
    notes = forms.CharField(
        label="Keluhan / Catatan (Opsional)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 3,
            'placeholder': 'Tuliskan keluhan atau alasan kunjungan...'
        })
    )
    
    class Meta:
        model = MedicalRecord
        fields = ('doctor', 'examination_date', 'examination_time', 'notes')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hapus field diagnosis dan treatment karena akan diisi dokter
        if 'diagnosis' in self.fields:
            del self.fields['diagnosis']
        if 'treatment' in self.fields:
            del self.fields['treatment']
    
    def clean(self):
        cleaned_data = super().clean()
        examination_date = cleaned_data.get('examination_date')
        examination_time = cleaned_data.get('examination_time')
        doctor = cleaned_data.get('doctor')
        
        # Validasi tanggal tidak boleh hari ini atau sebelumnya
        today = timezone.now().date()
        if examination_date and examination_date <= today:
            self.add_error('examination_date', "Tanggal harus minimal besok.")
        
        # Validasi tidak lebih dari 30 hari ke depan
        max_date = today + timedelta(days=30)
        if examination_date and examination_date > max_date:
            self.add_error('examination_date', "Booking hanya bisa hingga 30 hari ke depan.")
        
        # Validasi ketersediaan dokter
        if examination_date and examination_time and doctor:
            existing_appointment = MedicalRecord.objects.filter(
                doctor=doctor,
                examination_date=examination_date,
                examination_time=examination_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing_appointment:
                self.add_error(
                    None,
                    f"Dokter {doctor.name} tidak tersedia pada waktu tersebut. Silahkan pilih waktu lain."
                )
        
        return cleaned_data


class PaymentForm(forms.ModelForm):
    """Form untuk pembayaran/pembayaran sebagian"""
    
    class Meta:
        model = Payment
        fields = ('paid_amount', 'method', 'notes')
    
    paid_amount = forms.DecimalField(
        label="Jumlah Pembayaran",
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan jumlah pembayaran'
        })
    )
    
    method = forms.ChoiceField(
        label="Metode Pembayaran",
        choices=Payment.PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    notes = forms.CharField(
        label="Catatan (Opsional)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 2,
            'placeholder': 'Catatan pembayaran...'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        paid_amount = cleaned_data.get('paid_amount')
        
        if paid_amount and paid_amount <= 0:
            self.add_error('paid_amount', "Jumlah pembayaran harus lebih dari 0")
        
        return cleaned_data


class AppointmentConfirmationForm(forms.ModelForm):
    """Form untuk dokter approve/reject appointment"""
    
    class Meta:
        model = MedicalRecord
        fields = ('confirmation_status', 'rejection_reason')
    
    confirmation_status = forms.ChoiceField(
        label="Status Konfirmasi",
        choices=[('approved', 'Setujui'), ('rejected', 'Tolak')],
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600'
        })
    )
    
    rejection_reason = forms.CharField(
        label="Alasan Penolakan (jika ditolak)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 3,
            'placeholder': 'Tuliskan alasan penolakan...'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('confirmation_status')
        reason = cleaned_data.get('rejection_reason')
        
        if status == 'rejected' and not reason:
            self.add_error('rejection_reason', 'Alasan penolakan harus diisi jika menolak.')
        
        return cleaned_data


class MedicalRecordDiagnosisForm(forms.ModelForm):
    """Form untuk dokter input diagnosis dan treatment"""
    
    class Meta:
        model = MedicalRecord
        fields = ('diagnosis', 'treatment')
    
    diagnosis = forms.CharField(
        label="Diagnosis",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 4,
            'placeholder': 'Tuliskan diagnosis pasien...'
        })
    )
    
    treatment = forms.CharField(
        label="Rencana Pengobatan",
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 4,
            'placeholder': 'Tuliskan rencana pengobatan...'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form untuk update profil user"""
    
    first_name = forms.CharField(
        label="Nama Depan",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        })
    )
    
    last_name = forms.CharField(
        label="Nama Belakang",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        })
    )
    
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PatientProfileUpdateForm(ProfileUpdateForm):
    """Form untuk update profil pasien"""
    
    phone = forms.CharField(
        label="Nomor Telepon",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'tel'
        })
    )
    
    date_of_birth = forms.DateField(
        label="Tanggal Lahir",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date'
        })
    )
    
    GENDER_CHOICES = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    gender = forms.ChoiceField(
        label="Jenis Kelamin",
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600'
        })
    )
    
    BLOOD_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ]
    blood_type = forms.ChoiceField(
        label="Golongan Darah",
        choices=BLOOD_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    address = forms.CharField(
        label="Alamat",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 3
        })
    )
    
    bpjs_status = forms.BooleanField(
        label="Saya memiliki BPJS",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 rounded cursor-pointer'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.patient_profile:
            patient = self.instance.patient_profile
            self.fields['phone'].initial = patient.phone
            self.fields['date_of_birth'].initial = patient.date_of_birth
            self.fields['gender'].initial = patient.gender
            self.fields['blood_type'].initial = patient.blood_type
            self.fields['address'].initial = patient.address
            self.fields['bpjs_status'].initial = patient.bpjs_status
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if user.patient_profile:
            patient = user.patient_profile
            patient.phone = self.cleaned_data.get('phone')
            patient.date_of_birth = self.cleaned_data.get('date_of_birth')
            patient.gender = self.cleaned_data.get('gender')
            patient.blood_type = self.cleaned_data.get('blood_type')
            patient.address = self.cleaned_data.get('address')
            patient.bpjs_status = self.cleaned_data.get('bpjs_status')
            patient.save()
        return user


class DoctorProfileUpdateForm(ProfileUpdateForm):
    """Form untuk update profil dokter"""
    
    phone = forms.CharField(
        label="Nomor Telepon",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'tel'
        })
    )
    
    specialty = forms.CharField(
        label="Spesialisasi",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.doctor_profile:
            doctor = self.instance.doctor_profile
            self.fields['phone'].initial = doctor.phone
            self.fields['specialty'].initial = doctor.specialty
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if user.doctor_profile:
            doctor = user.doctor_profile
            doctor.phone = self.cleaned_data.get('phone')
            doctor.specialty = self.cleaned_data.get('specialty')
            doctor.save()
        return user


class ChangePasswordForm(forms.Form):
    """Form untuk change password"""
    
    old_password = forms.CharField(
        label="Password Lama",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan password lama',
            'autocomplete': 'current-password'
        })
    )
    
    new_password = forms.CharField(
        label="Password Baru",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan password baru',
            'autocomplete': 'new-password'
        })
    )
    
    confirm_password = forms.CharField(
        label="Konfirmasi Password Baru",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Konfirmasi password baru',
            'autocomplete': 'new-password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_pwd = cleaned_data.get('new_password')
        confirm_pwd = cleaned_data.get('confirm_password')
        
        if new_pwd and confirm_pwd and new_pwd != confirm_pwd:
            self.add_error('confirm_password', 'Password tidak cocok.')
        
        return cleaned_data


class DoctorAvailabilityForm(forms.ModelForm):
    """Form untuk mengatur jadwal kerja dokter per hari"""
    
    class Meta:
        model = DoctorAvailability
        fields = ('day_of_week', 'start_time', 'end_time', 'is_active')
    
    day_of_week = forms.ChoiceField(
        label="Hari",
        choices=DoctorAvailability.DAY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    
    start_time = forms.TimeField(
        label="Jam Mulai",
        widget=forms.TimeInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'type': 'time'
        })
    )
    
    end_time = forms.TimeField(
        label="Jam Selesai",
        widget=forms.TimeInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'type': 'time'
        })
    )
    
    is_active = forms.BooleanField(
        label="Aktif pada hari ini",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 rounded cursor-pointer'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', 'Jam selesai harus lebih besar dari jam mulai.')
        
        return cleaned_data


class DoctorLeaveForm(forms.ModelForm):
    """Form untuk mengatur hari libur/cuti dokter"""
    
    class Meta:
        model = DoctorLeave
        fields = ('start_date', 'end_date', 'reason')
    
    start_date = forms.DateField(
        label="Tanggal Mulai",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'type': 'date'
        })
    )
    
    end_date = forms.DateField(
        label="Tanggal Selesai",
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'type': 'date'
        })
    )
    
    reason = forms.CharField(
        label="Alasan (Opsional)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'rows': 3,
            'placeholder': 'Contoh: Cuti tahunan, Acara keluarga, dll'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'Tanggal selesai harus lebih besar dari tanggal mulai.')
        
        if start_date and start_date < timezone.now().date():
            self.add_error('start_date', 'Tanggal mulai tidak boleh di masa lalu.')
        
        return cleaned_data


