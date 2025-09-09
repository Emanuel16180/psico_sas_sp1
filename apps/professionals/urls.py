# apps/professionals/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # CU-06: Completar Perfil Profesional
    path('profile/', views.professional_profile_detail, name='professional_profile'),
    
    # CU-08: Buscar y Filtrar Profesionales
    path('', views.list_professionals, name='list_professionals'),
    
    # CU-09: Ver Perfil Público Profesional
    path('<int:professional_id>/', views.professional_public_detail, name='professional_detail'),
    
    # Especialidades
    path('specializations/', views.list_specializations, name='list_specializations'),
]