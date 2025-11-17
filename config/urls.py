# config/urls.py
from django.contrib import admin
from django.urls import path, include
from hospital.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('doctor/', include('hospital.doctor_urls')),
    path('', home, name='home'),
]