# core/admin.py
from django.contrib import admin
from .models import *

# Inline untuk relasi
class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    fields = ('medicine', 'prescription_date', 'dosage', 'notes')

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    extra = 0
    fields = ('doctor', 'examination_date', 'diagnosis', 'treatment')

class InpatientInline(admin.TabularInline):
    model = Inpatient
    extra = 0
    fields = ('room', 'admission_date', 'discharge_date', 'diagnosis')

# === Admin Models ===

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date_of_birth', 'gender', 'blood_type', 'bpjs_status')
    list_filter = ('gender', 'blood_type', 'bpjs_status')
    search_fields = ('name', 'phone')
    inlines = [MedicalRecordInline, InpatientInline]
    fieldsets = (
        (None, {'fields': ('name', 'phone', 'address')}),
        ('Data Pribadi', {'fields': ('date_of_birth', 'gender', 'blood_type')}),
        ('Asuransi', {'fields': ('bpjs_status',)}),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'unit', 'phone', 'email')
    list_filter = ('specialty', 'unit')
    search_fields = ('name', 'specialty')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone')}),
        ('Profesi', {'fields': ('sip_number', 'str_number', 'specialty', 'position', 'unit')}),
        ('Pribadi', {'fields': ('date_of_birth', 'gender', 'monthly_salary')}),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'capacity', 'daily_rate')
    list_filter = ('room_type',)
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'medicine_class', 'stock', 'price', 'expiry_date', 'supplier')
    list_filter = ('medicine_class', 'supplier', 'expiry_date')
    search_fields = ('name',)

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'examination_date', 'diagnosis')
    list_filter = ('examination_date', 'doctor')
    search_fields = ('patient__name', 'doctor__name')
    inlines = [PrescriptionInline]
    date_hierarchy = 'examination_date'

@admin.register(Inpatient)
class InpatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room', 'admission_date', 'discharge_date', 'cost')
    list_filter = ('room', 'admission_date')
    search_fields = ('patient__name',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'medicine', 'prescription_date', 'dosage')
    list_filter = ('prescription_date', 'medicine')
    search_fields = ('medical_record__patient__name', 'medicine__name')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'examination_date', 'examination_time')
    list_filter = ('examination_date', 'doctor')
    search_fields = ('doctor__name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'amount', 'paid_amount', 'status', 'method', 'created_at')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('patient__name', 'invoice_number')
    readonly_fields = ('invoice_number', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('invoice_number', 'patient', 'medical_record')}),
        ('Pembayaran', {'fields': ('service_name', 'amount', 'paid_amount', 'status', 'method')}),
        ('Tanggal', {'fields': ('due_date', 'payment_date')}),
        ('Catatan', {'fields': ('notes',)}),
        ('Sistem', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(MedicalTransaction)
class MedicalTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'medical_record', 'payment', 'total')
    search_fields = ('medical_record__patient__name',)