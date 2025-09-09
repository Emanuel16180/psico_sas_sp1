# apps/professionals/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Specialization(models.Model):
    """
    Especialidades de los profesionales
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'specializations'
        verbose_name = 'Especialización'
        verbose_name_plural = 'Especializaciones'
    
    def __str__(self):
        return self.name


class ProfessionalProfile(models.Model):
    """
    Perfil profesional para psicólogos
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='professional_profile'
    )
    license_number = models.CharField(max_length=50, unique=True)
    specializations = models.ManyToManyField(Specialization, blank=True)
    bio = models.TextField(help_text="Descripción profesional")
    education = models.TextField(help_text="Formación académica")
    experience_years = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text="Años de experiencia"
    )
    consultation_fee = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        help_text="Tarifa por consulta en Bs."
    )
    
    # Configuración de consultas
    session_duration = models.PositiveIntegerField(
        default=60, 
        help_text="Duración de sesión en minutos"
    )
    accepts_online_sessions = models.BooleanField(default=True)
    accepts_in_person_sessions = models.BooleanField(default=True)
    
    # Información de ubicación
    office_address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True, default="La Paz")
    
    # Calificaciones y reseñas
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Estado del perfil
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'professional_profiles'
        verbose_name = 'Perfil Profesional'
        verbose_name_plural = 'Perfiles Profesionales'
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class WorkingHours(models.Model):
    """
    Horarios de trabajo de los profesionales
    """
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    professional = models.ForeignKey(
        ProfessionalProfile, 
        on_delete=models.CASCADE,
        related_name='working_hours'
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'working_hours'
        verbose_name = 'Horario de Trabajo'
        verbose_name_plural = 'Horarios de Trabajo'
        unique_together = ['professional', 'day_of_week']
    
    def __str__(self):
        return f"{self.professional} - {self.get_day_of_week_display()}: {self.start_time} - {self.end_time}"