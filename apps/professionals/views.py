# apps/professionals/views.py

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ProfessionalProfile, Specialization
from .serializers import (
    ProfessionalProfileSerializer,
    ProfessionalProfileUpdateSerializer,
    ProfessionalPublicSerializer,
    SpecializationSerializer
)

User = get_user_model()

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def professional_profile_detail(request):
    """
    CU-06: Completar Perfil Profesional
    Solo psicólogos y admins pueden gestionar perfiles profesionales
    """
    user = request.user
    
    # Verificar permisos
    if user.user_type not in ['professional', 'admin']:
        return Response({
            'error': 'Solo psicólogos y administradores pueden acceder'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        try:
            if user.user_type == 'admin':
                # Admin puede ver cualquier perfil (requiere ID en query params)
                prof_id = request.query_params.get('professional_id')
                if prof_id:
                    professional = get_object_or_404(
                        User.objects.filter(user_type='professional'), 
                        id=prof_id
                    )
                    profile = professional.professional_profile
                else:
                    return Response({
                        'error': 'professional_id requerido para admin'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Psicólogo ve su propio perfil
                profile = user.professional_profile
            
            serializer = ProfessionalProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ProfessionalProfile.DoesNotExist:
            return Response({
                'message': 'Perfil profesional no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        # Crear perfil profesional
        if user.user_type != 'professional':
            return Response({
                'error': 'Solo psicólogos pueden crear perfil profesional'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if hasattr(user, 'professional_profile'):
            return Response({
                'error': 'Ya tienes un perfil profesional'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProfessionalProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=user)
            response_serializer = ProfessionalProfileSerializer(profile)
            return Response({
                'message': 'Perfil profesional creado exitosamente',
                'profile': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method in ['PUT', 'PATCH']:
        # Actualizar perfil profesional
        try:
            if user.user_type == 'admin':
                prof_id = request.data.get('professional_id')
                if prof_id:
                    professional = get_object_or_404(
                        User.objects.filter(user_type='professional'), 
                        id=prof_id
                    )
                    profile = professional.professional_profile
                else:
                    return Response({
                        'error': 'professional_id requerido para admin'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                profile = user.professional_profile
            
            partial = request.method == 'PATCH'
            serializer = ProfessionalProfileUpdateSerializer(
                profile, data=request.data, partial=partial
            )
            
            if serializer.is_valid():
                serializer.save()
                response_serializer = ProfessionalProfileSerializer(profile)
                return Response({
                    'message': 'Perfil actualizado exitosamente',
                    'profile': response_serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except ProfessionalProfile.DoesNotExist:
            return Response({
                'error': 'Perfil profesional no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_professionals(request):
    """
    CU-08: Buscar y Filtrar Profesionales
    """
    # Filtros disponibles
    specialization = request.query_params.get('specialization')
    city = request.query_params.get('city')
    max_fee = request.query_params.get('max_fee')
    min_rating = request.query_params.get('min_rating')
    accepts_online = request.query_params.get('accepts_online')
    search = request.query_params.get('search')
    
    # Query base: solo perfiles activos (quitamos is_verified para testing)
    profiles = ProfessionalProfile.objects.filter(
        is_active=True,
        profile_completed=True
    )
    
    # Aplicar filtros
    if specialization:
        profiles = profiles.filter(specializations__name__icontains=specialization)
    
    if city:
        profiles = profiles.filter(city__icontains=city)
    
    if max_fee:
        try:
            profiles = profiles.filter(consultation_fee__lte=float(max_fee))
        except ValueError:
            pass
    
    if min_rating:
        try:
            profiles = profiles.filter(average_rating__gte=float(min_rating))
        except ValueError:
            pass
    
    if accepts_online:
        profiles = profiles.filter(accepts_online_sessions=True)
    
    if search:
        profiles = profiles.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    serializer = ProfessionalPublicSerializer(profiles, many=True)
    return Response({
        'count': profiles.count(),
        'professionals': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def professional_public_detail(request, professional_id):
    """
    CU-09: Ver Perfil Público Profesional
    Vista pública de un psicólogo específico
    """
    try:
        profile = get_object_or_404(
            ProfessionalProfile.objects.filter(
                is_active=True,
                profile_completed=True
            ),
            id=professional_id
        )
        
        serializer = ProfessionalPublicSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except ProfessionalProfile.DoesNotExist:
        return Response({
            'error': 'Profesional no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_specializations(request):
    """
    Listar todas las especialidades disponibles
    """
    specializations = Specialization.objects.all()
    serializer = SpecializationSerializer(specializations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)