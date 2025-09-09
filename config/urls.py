# psico_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),      # CU-01, CU-02, CU-03, CU-04
    path('api/users/', include('apps.users.urls')),              # CU-05
    path('api/professionals/', include('apps.professionals.urls')), # CU-06, CU-08, CU-09, CU-12
    path('api/appointments/', include('apps.appointments.urls')), # CU-10
    
    # API browsable (para desarrollo)
    path('api-auth/', include('rest_framework.urls')),
]

# Servir archivos media y static en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)