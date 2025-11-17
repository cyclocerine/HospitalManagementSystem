# QUICK START GUIDE - Hospital Management System

Setelah perbaikan selesai, ikuti langkah-langkah ini untuk menjalankan aplikasi.

## 1. Setup Environment

```bash
# Navigate ke project directory
cd C:\Users\USER\Documents\GitHub\HospitalManagementSystem

# Create virtual environment (jika belum ada)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Database Setup

### MySQL Configuration

```bash
# Ensure MySQL is running
# Create database
mysql -u root
CREATE DATABASE rumah_sakit CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Run Migrations

```bash
# Apply all migrations
python manage.py migrate
```

## 3. Create Admin User

```bash
# Create superuser
python manage.py createsuperuser
# Masukkan:
# Username: admin (atau username lain)
# Email: admin@example.com
# Password: (pilih password yang kuat)
```

## 4. Run Development Server

```bash
# Start server di http://127.0.0.1:8000/
python manage.py runserver

# Atau untuk akses dari komputer lain:
python manage.py runserver 0.0.0.0:8000
```

## 5. Access Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Dashboards**: 
  - Admin: http://127.0.0.1:8000/accounts/dashboard/admin/
  - Doctor: http://127.0.0.1:8000/accounts/dashboard/doctor/
  - Patient: http://127.0.0.1:8000/accounts/dashboard/patient/

## 6. Troubleshooting

### MySQL Connection Error
```
Error: "Can't connect to MySQL server"
Solution:
  1. Ensure MySQL service is running
  2. Check credentials in config/settings.py
  3. Verify database exists: CREATE DATABASE rumah_sakit;
```

### Migration Error
```
Error: "Column doesn't exist"
Solution:
  python manage.py migrate --fake-initial
  python manage.py migrate
```

### Template Not Found
```
Error: "TemplateDoesNotExist"
Solution:
  Ensure TEMPLATES['DIRS'] is set correctly in settings.py
  Already fixed: DIRS': [BASE_DIR / 'hospital' / 'templates'],
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

## 7. Project Structure Reference

```
HospitalManagementSystem/
├── config/              # Project settings
├── accounts/            # User authentication & roles
├── core/                # Core business models
├── hospital/            # Hospital app (views, templates)
├── db.sqlite3          # Development database
├── manage.py           # Django management
└── requirements.txt    # Python dependencies
```

## 8. Key Files Reference

| File | Purpose | Status |
|------|---------|--------|
| config/settings.py | Project configuration | ✅ Fixed |
| accounts/models.py | User model with roles | ✅ Fixed |
| hospital/models.py | Model re-exports | ✅ Fixed |
| hospital/views.py | View functions | ✅ Fixed |
| hospital/templates/ | HTML templates | ✅ Fixed |
| core/models/ | Business logic models | ✅ OK |

## 9. Common Commands

```bash
# Check for errors
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Drop database and recreate
python manage.py flush
python manage.py migrate
```

## 10. Environment Variables (Optional Setup)

Create `.env` file (gitignore it!):
```
DEBUG=True
DATABASE_NAME=rumah_sakit
DATABASE_USER=root
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=3306
SECRET_KEY=your-secret-key
```

Load in settings.py:
```python
from dotenv import load_dotenv
import os
load_dotenv()
DEBUG = os.getenv('DEBUG', True)
```

## 11. Development Tips

### Enable Debug Toolbar
```bash
pip install django-debug-toolbar
# Add to INSTALLED_APPS: 'debug_toolbar'
# Add to MIDDLEWARE: 'debug_toolbar.middleware.DebugToolbarMiddleware'
```

### Auto-reload on code change
Server otomatis reload saat ada perubahan file (development mode)

### Access database directly
```bash
python manage.py dbshell
```

### Test email locally
```bash
# Terminal 1: Start email console
python -m smtpd -n -c DebuggingServer localhost:1025

# Terminal 2: Update settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 12. Next Development Steps

1. **Implement Login/Logout Pages**
   - Create login template
   - Create logout view
   - Add password reset functionality

2. **Enhance Patient Appointment**
   - Add appointment scheduling
   - Email notifications
   - Calendar view

3. **Add API Endpoints**
   - Install djangorestframework
   - Create API serializers
   - Add API authentication

4. **Improve Admin Panel**
   - Custom admin templates
   - Reports and statistics
   - Dashboard widgets

5. **Frontend Enhancement**
   - Responsive design
   - Dark mode toggle
   - Real-time notifications

## 13. Deployment Checklist

When ready for production:

```bash
# 1. Set DEBUG=False
DEBUG = False

# 2. Set ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 3. Configure static files
python manage.py collectstatic

# 4. Use proper database (PostgreSQL recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rumah_sakit',
        'USER': 'postgres',
        'PASSWORD': 'secure_password',
        'HOST': 'db.example.com',
        'PORT': '5432',
    }
}

# 5. Configure email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# 6. Use environment variables for secrets
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
```

## 14. Support & Documentation

- Django Docs: https://docs.djangoproject.com
- Jazzmin Docs: https://github.com/farridav/django-jazzmin
- MySQL Docs: https://dev.mysql.com/doc/
- Tailwind CSS: https://tailwindcss.com

## 15. Issue Tracking

Jika ada error:
1. Check console output
2. Read error message carefully
3. Check error logs
4. Refer to PERBAIKAN.md untuk detil perbaikan
5. Check Django docs

---

## Quick Reference - URLs Pattern

```
http://localhost:8000/                          # Homepage
http://localhost:8000/admin/                    # Admin panel
http://localhost:8000/accounts/                 # Accounts app
http://localhost:8000/accounts/dashboard/       # Dashboard redirect
http://localhost:8000/accounts/dashboard/admin/ # Admin dashboard
http://localhost:8000/accounts/dashboard/doctor/# Doctor dashboard
http://localhost:8000/accounts/dashboard/patient/# Patient dashboard
http://localhost:8000/accounts/logout/          # Logout
```

---

**Status: ✅ READY TO USE**

Semua error sudah diperbaiki. Aplikasi siap untuk development!

Untuk informasi detail tentang perbaikan, baca file-file:
- `PERBAIKAN.md` - Technical details
- `README_PERBAIKAN.md` - Visual summary
- `CHECKLIST.md` - Complete checklist
- `AUDIT_REPORT.txt` - Detailed audit report
