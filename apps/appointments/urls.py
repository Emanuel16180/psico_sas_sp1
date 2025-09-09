# apps/appointments/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'availability', views.PsychologistAvailabilityViewSet, basename='availability')

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
    
    # Custom endpoints
    path('search-psychologists/', views.search_available_psychologists, name='search-psychologists'),
    path('psychologist/<int:psychologist_id>/schedule/', views.get_psychologist_schedule, name='psychologist-schedule'),
]