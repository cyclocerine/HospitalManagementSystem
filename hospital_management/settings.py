# settings.py
# for postgresql code
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hospital_db',
#         'USER': 'your_user',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# untuk mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# === JAZZMIN UI CONFIGURATION ===
# settings.py
INSTALLED_APPS = [
    'jazzmin',  # <-- HARUS DI ATAS django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # app Anda
]

JAZZMIN_SETTINGS = {
    # Judul & logo
    "site_title": "Rumah Sakit Admin",
    "site_header": "HMS",
    "site_brand": "Hospital Management",
    "welcome_sign": "Selamat datang di Admin Rumah Sakit",
    "copyright": "Rumah Sakit © 2025",

    # Logo (opsional)
    "site_logo": "images/hospital-logo.png",  # simpan di static/images/
    "login_logo": None,

    # Warna & tema
    "site_icon": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],

    # Sidebar
    "usermenu_links": [{"name": "Profile", "url": "admin:auth_user_change", "icon": "fas fa-user"}],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    # Ikon untuk setiap model 
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Patient": "fas fa-bed",
        "core.Doctor": "fas fa-user-md",
        "core.Room": "fas fa-hospital",
        "core.Supplier": "fas fa-truck",
        "core.Medicine": "fas fa-pills",
        "core.MedicalRecord": "fas fa-file-medical",
        "core.Inpatient": "fas fa-procedures",
        "core.Prescription": "fas fa-prescription",
        "core.Schedule": "fas fa-calendar-check",
        "core.Payment": "fas fa-credit-card",
        "core.MedicalTransaction": "fas fa-receipt",
    },

    # Tema warna
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # UI customization
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,  # set True untuk izinkan admin ganti tema langsung

    # Pilihan tema
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "core.patient": "collapsible",
        "core.doctor": "collapsible",
    },
}

# ini buat tema jazzmin
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "cyborg",  # pilihan: darkly, flatly, slate, cyborg, superhero, dll.
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}