from django.contrib import admin

# Register your models here.
# en apps/professionals/admin.py

from django.contrib import admin
from .models import ProfessionalProfile, Specialization, WorkingHours

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'experience_years', 'is_active', 'profile_completed')
    list_filter = ('is_active', 'profile_completed', 'specializations')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')

admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(WorkingHours)