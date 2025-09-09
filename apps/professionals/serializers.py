# apps/professionals/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProfessionalProfile, Specialization, WorkingHours

User = get_user_model()

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'description']

class WorkingHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = WorkingHours
        fields = ['id', 'day_of_week', 'day_name', 'start_time', 'end_time', 'is_active']

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    specializations = SpecializationSerializer(many=True, read_only=True)
    working_hours = WorkingHoursSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = ProfessionalProfile
        fields = [
            'id', 'full_name', 'email', 'license_number', 'bio', 
            'education', 'experience_years', 'consultation_fee',
            'session_duration', 'accepts_online_sessions', 
            'accepts_in_person_sessions', 'office_address', 'city', 
            'state', 'average_rating', 'total_reviews', 'is_verified',
            'profile_completed', 'specializations', 'working_hours'
        ]
        read_only_fields = ['average_rating', 'total_reviews', 'is_verified', 'profile_completed']

class ProfessionalProfileUpdateSerializer(serializers.ModelSerializer):
    specialization_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
    )
    
    class Meta:
        model = ProfessionalProfile
        fields = [
            'license_number', 'bio', 'education', 'experience_years',
            'consultation_fee', 'session_duration', 'accepts_online_sessions',
            'accepts_in_person_sessions', 'office_address', 'city', 'state',
            'specialization_ids'
        ]
    
    def create(self, validated_data):
        specialization_ids = validated_data.pop('specialization_ids', [])
        
        # Crear el perfil sin las especialidades
        profile = ProfessionalProfile.objects.create(**validated_data)
        
        # Agregar especialidades si se proporcionaron
        if specialization_ids:
            specializations = Specialization.objects.filter(id__in=specialization_ids)
            profile.specializations.set(specializations)
        
        # Marcar perfil como completo si tiene datos básicos
        if profile.license_number and profile.bio and profile.specializations.exists():
            profile.profile_completed = True
            profile.save()
        
        return profile
    
    def update(self, instance, validated_data):
        specialization_ids = validated_data.pop('specialization_ids', None)
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Actualizar especialidades si se proporcionaron
        if specialization_ids is not None:
            specializations = Specialization.objects.filter(id__in=specialization_ids)
            instance.specializations.set(specializations)
        
        # Marcar perfil como completo si tiene datos básicos
        if instance.license_number and instance.bio and instance.specializations.exists():
            instance.profile_completed = True
        
        instance.save()
        return instance

class ProfessionalPublicSerializer(serializers.ModelSerializer):
    """Serializer para vista pública (sin datos sensibles)"""
    specializations = SpecializationSerializer(many=True, read_only=True)
    working_hours = WorkingHoursSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ProfessionalProfile
        fields = [
            'id', 'full_name', 'bio', 'education', 'experience_years',
            'consultation_fee', 'session_duration', 'accepts_online_sessions',
            'accepts_in_person_sessions', 'city', 'state', 'average_rating',
            'total_reviews', 'specializations', 'working_hours'
        ]