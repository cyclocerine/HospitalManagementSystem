"""
Email notification utilities for the hospital management system.
Handles sending emails for various events (appointments, payments, etc.)
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from datetime import timedelta


def send_appointment_confirmation_email(patient, doctor, appointment):
    """
    Kirim email ketika dokter mengkonfirmasi appointment
    """
    subject = f"Appointment Anda Telah Dikonfirmasi - {doctor.name}"
    
    context = {
        'patient_name': patient.name,
        'doctor_name': doctor.name,
        'appointment_date': appointment.examination_date.strftime('%d %B %Y'),
        'appointment_time': appointment.examination_time.strftime('%H:%M'),
        'location': doctor.unit or 'Rumah Sakit',
        'notes': appointment.notes or 'Tidak ada catatan khusus'
    }
    
    html_message = f"""
    <h2>Appointment Anda Telah Dikonfirmasi</h2>
    <p>Halo {patient.name},</p>
    <p>Appointment Anda dengan Dr. {doctor.name} telah dikonfirmasi.</p>
    
    <h3>Rincian Appointment:</h3>
    <ul>
        <li><strong>Dokter:</strong> Dr. {doctor.name} ({doctor.specialty})</li>
        <li><strong>Tanggal:</strong> {context['appointment_date']}</li>
        <li><strong>Waktu:</strong> {context['appointment_time']}</li>
        <li><strong>Lokasi:</strong> {context['location']}</li>
    </ul>
    
    <p>Silakan datang 10 menit sebelum jadwal appointment Anda.</p>
    <p>Terima kasih telah menggunakan layanan kami.</p>
    """
    
    send_email(patient.phone or 'notification', subject, html_message)


def send_appointment_rejection_email(patient, doctor, appointment, reason):
    """
    Kirim email ketika dokter menolak appointment
    """
    subject = f"Appointment Anda Ditolak - {doctor.name}"
    
    html_message = f"""
    <h2>Pemberitahuan Appointment</h2>
    <p>Halo {patient.name},</p>
    <p>Mohon maaf, appointment Anda dengan Dr. {doctor.name} ditolak.</p>
    
    <h3>Alasan Penolakan:</h3>
    <p>{reason}</p>
    
    <p>Silakan melakukan booking ulang untuk jadwal lain. Kami tunggu kunjungan Anda.</p>
    """
    
    send_email(patient.phone or 'notification', subject, html_message)


def send_appointment_reminder_email(patient, doctor, appointment):
    """
    Kirim email reminder 1 hari sebelum appointment
    """
    subject = f"Pengingat: Appointment Anda Besok dengan {doctor.name}"
    
    html_message = f"""
    <h2>Pengingat Appointment</h2>
    <p>Halo {patient.name},</p>
    <p>Ini adalah pengingat untuk appointment Anda besok dengan Dr. {doctor.name}.</p>
    
    <h3>Rincian Appointment:</h3>
    <ul>
        <li><strong>Dokter:</strong> Dr. {doctor.name} ({doctor.specialty})</li>
        <li><strong>Tanggal:</strong> {appointment.examination_date.strftime('%d %B %Y')}</li>
        <li><strong>Waktu:</strong> {appointment.examination_time.strftime('%H:%M')}</li>
        <li><strong>Lokasi:</strong> {doctor.unit or 'Rumah Sakit'}</li>
    </ul>
    
    <p>Silakan datang 10 menit lebih awal. Terima kasih!</p>
    """
    
    send_email(patient.phone or 'notification', subject, html_message)


def send_payment_confirmation_email(patient, payment):
    """
    Kirim email konfirmasi pembayaran
    """
    subject = f"Konfirmasi Pembayaran - {payment.invoice_number}"
    
    html_message = f"""
    <h2>Konfirmasi Pembayaran</h2>
    <p>Halo {patient.name},</p>
    <p>Pembayaran Anda telah berhasil dicatat.</p>
    
    <h3>Rincian Pembayaran:</h3>
    <ul>
        <li><strong>No. Invoice:</strong> {payment.invoice_number}</li>
        <li><strong>Layanan:</strong> {payment.service_name}</li>
        <li><strong>Jumlah Pembayaran:</strong> Rp{payment.paid_amount:,.0f}</li>
        <li><strong>Total Tagihan:</strong> Rp{payment.amount:,.0f}</li>
        <li><strong>Sisa Pembayaran:</strong> Rp{payment.remaining_amount:,.0f}</li>
        <li><strong>Metode Pembayaran:</strong> {payment.get_method_display()}</li>
        <li><strong>Status:</strong> {payment.get_status_display()}</li>
    </ul>
    
    <p>Terima kasih atas pembayaran Anda!</p>
    """
    
    send_email(patient.phone or 'notification', subject, html_message)


def send_payment_reminder_email(patient, payment):
    """
    Kirim email reminder untuk pembayaran yang jatuh tempo
    """
    subject = f"Pengingat Pembayaran - {payment.invoice_number}"
    
    html_message = f"""
    <h2>Pengingat Pembayaran</h2>
    <p>Halo {patient.name},</p>
    <p>Ini adalah pengingat untuk pembayaran yang belum diselesaikan.</p>
    
    <h3>Rincian Tagihan:</h3>
    <ul>
        <li><strong>No. Invoice:</strong> {payment.invoice_number}</li>
        <li><strong>Layanan:</strong> {payment.service_name}</li>
        <li><strong>Total Tagihan:</strong> Rp{payment.amount:,.0f}</li>
        <li><strong>Sudah Dibayar:</strong> Rp{payment.paid_amount:,.0f}</li>
        <li><strong>Sisa Pembayaran:</strong> Rp{payment.remaining_amount:,.0f}</li>
        <li><strong>Batas Pembayaran:</strong> {payment.due_date.strftime('%d %B %Y')}</li>
    </ul>
    
    <p>Silakan selesaikan pembayaran Anda sebelum batas tanggal di atas.</p>
    """
    
    send_email(patient.phone or 'notification', subject, html_message)


def send_email(recipient, subject, html_message, fail_silently=True):
    """
    Fungsi utility untuk mengirim email
    Menggunakan EMAIL_BACKEND dari settings (console untuk dev, SMTP untuk prod)
    """
    try:
        send_mail(
            subject=subject,
            message=strip_tags(html_message),
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@rumahsakit.com',
            recipient_list=['test@example.com'],  # Untuk console backend
            html_message=html_message,
            fail_silently=fail_silently,
        )
    except Exception as e:
        if not fail_silently:
            raise e
