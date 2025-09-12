# en apps/appointments/admin.py

from django.contrib import admin
from .models import Appointment, PsychologistAvailability

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'psychologist', 'appointment_date', 'start_time', 'status', 'is_paid')
    list_filter = ('status', 'appointment_date', 'psychologist')
    search_fields = ('patient__first_name', 'patient__last_name', 'psychologist__first_name')

class PsychologistAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('psychologist', 'get_weekday_display', 'start_time', 'end_time', 'is_active')
    list_filter = ('psychologist', 'weekday', 'is_active')

    # Pequeña función para mostrar el nombre del día en lugar del número
    def get_weekday_display(self, obj):
        return obj.get_weekday_display()
    get_weekday_display.short_description = 'Día de la Semana'

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(PsychologistAvailability, PsychologistAvailabilityAdmin)