# 🧪 Testing Guide - Hospital Management System Features

## Complete Testing Instructions

**Date:** November 17, 2025  
**Features to Test:** 5 major + quick wins  
**Estimated Time:** 30-45 minutes  

---

## ✅ Pre-Testing Checklist

Before starting tests:
- [ ] Server is running: `python manage.py runserver 0.0.0.0:8000`
- [ ] System check passed: `python manage.py check` → 0 errors
- [ ] Migrations applied: `python manage.py migrate` → OK
- [ ] Browser ready: Navigate to http://localhost:8000

---

## 🎯 Test Suite 1: Appointment Confirmation System

### Test 1.1: View Pending Appointments
**Steps:**
1. Login as doctor
2. Click "Dashboard" → "Konfirmasi Appointment"
3. Should see list of pending appointments

**Expected Results:**
- ✅ Page loads without errors
- ✅ Shows patient names and appointment details
- ✅ Shows "Menunggu Konfirmasi" tab active
- ✅ "Konfirmasi" button visible on each appointment

---

### Test 1.2: Search Appointments
**Steps:**
1. From doctor appointments page
2. Enter patient name in search box
3. Click "Cari" button

**Expected Results:**
- ✅ List filters to matching appointments only
- ✅ Search term shown in search box
- ✅ "Reset" button appears
- ✅ Reset clears search and shows all appointments

---

### Test 1.3: Pagination
**Steps:**
1. (If more than 10 pending appointments exist)
2. Check bottom of appointments list
3. Click "Next" page button

**Expected Results:**
- ✅ Pagination controls visible (if 10+ items)
- ✅ Page numbers displayed
- ✅ Next/Previous navigation works
- ✅ Search term preserved across pages

---

### Test 1.4: Approve Appointment
**Steps:**
1. Click "Konfirmasi" button on a pending appointment
2. Select "Setujui" (Approve)
3. Click "Simpan Keputusan"

**Expected Results:**
- ✅ Success message shows
- ✅ Redirected back to appointments list
- ✅ Appointment moves to "Terkonfirmasi" tab
- ✅ **Console shows email notification** (development mode)

**Check Email Console Output:**
```
Subject: Appointment Anda Telah Dikonfirmasi - Dr. [Name]
To: test@example.com
[HTML email content with appointment details]
```

---

### Test 1.5: Reject Appointment
**Steps:**
1. Click "Konfirmasi" on another pending appointment
2. Select "Tolak" (Reject)
3. Enter rejection reason (required)
4. Click "Simpan Keputusan"

**Expected Results:**
- ✅ Rejection reason field required if "Tolak" selected
- ✅ Success message shows rejection
- ✅ Redirected back to appointments
- ✅ Appointment moves to "Ditolak" tab
- ✅ **Console shows rejection email**

---

### Test 1.6: Add Diagnosis
**Steps:**
1. From "Terkonfirmasi" tab, click "Tambah Diagnosis" button
2. Fill in diagnosis details
3. Fill in treatment plan
4. Click "Simpan Diagnosis & Pengobatan"

**Expected Results:**
- ✅ Form displays with patient context
- ✅ Both diagnosis and treatment fields required
- ✅ Success message shows
- ✅ Appointment status changes to "Selesai"

---

## 🎯 Test Suite 2: Email Notifications

### Test 2.1: Appointment Confirmation Email
**Steps:**
1. Approve an appointment (Test 1.4)
2. Check terminal/server console

**Expected Results:**
- ✅ Console shows email output
- ✅ Subject includes doctor name
- ✅ Body includes:
  - Doctor name and specialty
  - Appointment date and time
  - Location/unit information
  - Arrival instructions

**Development Mode Output:**
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Appointment Anda Telah Dikonfirmasi - Dr. John Doe
From: noreply@rumahsakit.com
To: test@example.com

[HTML Email Body with appointment details]
```

---

### Test 2.2: Payment Confirmation Email
**Steps:**
1. Login as patient
2. Go to "Tagihan Saya" (Bills)
3. Click on a bill
4. Enter payment amount
5. Click "Bayar Sekarang"

**Expected Results:**
- ✅ Console shows payment confirmation email
- ✅ Email includes:
  - Invoice number
  - Amount paid
  - Remaining balance
  - Payment method

---

## 🎯 Test Suite 3: Profile Updates

### Test 3.1: Patient Profile Update
**Steps:**
1. Login as patient
2. Click "Profil" in navbar
3. Update name, email, phone
4. Click "Simpan Perubahan"

**Expected Results:**
- ✅ Form pre-populates with current data
- ✅ Changes save successfully
- ✅ Success message appears
- ✅ Dashboard reflects updated info

---

### Test 3.2: Doctor Profile Update
**Steps:**
1. Login as doctor
2. Click "Profil" in navbar
3. Update specialty or phone
4. Click "Simpan Perubahan"

**Expected Results:**
- ✅ Form shows doctor-specific fields
- ✅ Changes save successfully
- ✅ Database updated

---

### Test 3.3: Change Password
**Steps:**
1. Click "Profil" in navbar
2. Click "Ubah Password Anda" or link to change password
3. Enter old password (required)
4. Enter new password
5. Confirm new password
6. Click "Ubah Password"

**Expected Results:**
- ✅ Old password validation required
- ✅ New password and confirm must match
- ✅ Success message shows
- ✅ User remains logged in (session updated)
- ✅ Password change works on next login

---

## 🎯 Test Suite 4: Doctor Availability

### Test 4.1: View Availability
**Steps:**
1. Login as doctor
2. Click "Dashboard" → "Atur Jadwal Kerja"

**Expected Results:**
- ✅ Page shows current availability status
- ✅ Working hours displayed (08:00 - 17:00 default)
- ✅ Weekly schedule visible
- ✅ Any scheduled leaves shown

---

### Test 4.2: (For Admin) Set Availability
**Steps:**
1. Go to Django Admin
2. Navigate to Doctor Availability section
3. Create entry for doctor

**Expected Results:**
- ✅ Can create availability per day
- ✅ Unique constraint prevents duplicate days per doctor
- ✅ Saves successfully

---

## 🎯 Test Suite 5: Medical Records

### Test 5.1: Medical Record Flow
**Steps:**
1. Doctor approves appointment
2. Doctor adds diagnosis
3. Go back to appointments

**Expected Results:**
- ✅ Diagnosis saved successfully
- ✅ Appointment status changes to "Selesai"
- ✅ Diagnosis not editable after completing

---

## 🎯 Quick Wins Verification

### Test 6.1: Profile Link in Navbar
**Steps:**
1. Login as any user
2. Look at navbar

**Expected Results:**
- ✅ "Profil" link visible in navbar
- ✅ Clicking goes to `/accounts/profile/`

---

### Test 6.2: Status Badges
**Steps:**
1. View appointments on any dashboard

**Expected Results:**
- ✅ Green badges for confirmed
- ✅ Yellow badges for pending
- ✅ Red badges for rejected

---

### Test 6.3: Empty States
**Steps:**
1. Clear all pending appointments
2. Go back to doctor appointments

**Expected Results:**
- ✅ Shows helpful message (not blank page)
- ✅ "Tidak ada appointment..." message

---

## 🔒 Security Tests

### Test S.1: Access Control - Doctor Only
**Steps:**
1. Login as patient
2. Try to access `/accounts/appointment/confirm/`

**Expected Results:**
- ✅ Error message shows
- ✅ Redirects to appropriate page
- ✅ Cannot access restricted views

---

### Test S.2: Access Control - Profile
**Steps:**
1. Login as patient
2. Update profile
3. Logout
4. Try to access `/accounts/profile/`

**Expected Results:**
- ✅ Redirected to login page
- ✅ Cannot access without authentication

---

### Test S.3: CSRF Protection
**Steps:**
1. Try to submit form without CSRF token
2. (Use browser dev tools to remove token)

**Expected Results:**
- ✅ Form submission fails
- ✅ CSRF error message shows

---

## 📊 Test Results Template

Use this to document your test results:

```
=== TESTING SESSION ===
Date: _______________
Tester: ______________
Browser: _____________

Test Suite 1: Appointment Confirmation
  Test 1.1 View Pending:        [ ] PASS [ ] FAIL
  Test 1.2 Search:              [ ] PASS [ ] FAIL
  Test 1.3 Pagination:          [ ] PASS [ ] FAIL
  Test 1.4 Approve:             [ ] PASS [ ] FAIL
  Test 1.5 Reject:              [ ] PASS [ ] FAIL
  Test 1.6 Add Diagnosis:       [ ] PASS [ ] FAIL

Test Suite 2: Email Notifications
  Test 2.1 Appointment Email:   [ ] PASS [ ] FAIL
  Test 2.2 Payment Email:       [ ] PASS [ ] FAIL

Test Suite 3: Profile Updates
  Test 3.1 Patient Profile:     [ ] PASS [ ] FAIL
  Test 3.2 Doctor Profile:      [ ] PASS [ ] FAIL
  Test 3.3 Change Password:     [ ] PASS [ ] FAIL

Test Suite 4: Doctor Availability
  Test 4.1 View Availability:   [ ] PASS [ ] FAIL
  Test 4.2 Set Availability:    [ ] PASS [ ] FAIL

Test Suite 5: Medical Records
  Test 5.1 Diagnosis Entry:     [ ] PASS [ ] FAIL

Test Suite 6: Quick Wins
  Test 6.1 Profile Link:        [ ] PASS [ ] FAIL
  Test 6.2 Status Badges:       [ ] PASS [ ] FAIL
  Test 6.3 Empty States:        [ ] PASS [ ] FAIL

Security Tests
  Test S.1 Doctor Access:       [ ] PASS [ ] FAIL
  Test S.2 Auth Required:       [ ] PASS [ ] FAIL
  Test S.3 CSRF Protection:     [ ] PASS [ ] FAIL

OVERALL RESULT: [ ] ALL PASS [ ] SOME FAILURES

Issues Found:
1. ________________________
2. ________________________
3. ________________________
```

---

## 🐛 Debugging Tips

### If Email Not Showing
```bash
# Check console output in server terminal
# Look for "Content-Type: text/plain"
# Should show full email content

# For development, emails print directly to console
# No external configuration needed
```

### If Form Validation Fails
```python
# Check form errors in template
# Look for error messages under each field
# Form includes non-field errors at top with {{ form.non_field_errors }}
```

### If Redirect Issues
```bash
# Check if @login_required is blocking access
# Ensure logged in as correct role
# Check URL patterns in accounts/urls.py
```

---

## ✅ Final Validation

When all tests pass:

- [ ] All 5 features working
- [ ] All quick wins verified
- [ ] Security tests pass
- [ ] No console errors
- [ ] No database errors
- [ ] Emails working (console output)
- [ ] Forms validating
- [ ] Redirects working

**Status:** ✅ **READY FOR PRODUCTION**

---

## 📞 Common Issues & Solutions

### Issue: "Profil" link not in navbar
**Solution:** Clear browser cache, restart server

### Issue: Email not appearing in console
**Solution:** 
1. Check EMAIL_BACKEND = 'console.EmailBackend' in settings.py
2. Look in server terminal, not browser console
3. Scroll up - may be above other output

### Issue: Form says "Old password incorrect"
**Solution:** Enter correct current password, not the one you want to change to

### Issue: "Doctor" view shows patient appointments
**Solution:** Ensure logged in as doctor account, not patient

---

## 🎯 Performance Notes

- Pagination limits database queries to 10 items
- Search filters before pagination
- Email sending is non-blocking (fail_silently)
- Templates use select_related() for efficiency

---

**Happy Testing! 🧪**

*If you find any issues, the code comments and error messages should help identify the problem.*
