# en apps/users/management/commands/populate_db.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from apps.professionals.models import ProfessionalProfile, Specialization
from apps.appointments.models import Appointment
from datetime import date, timedelta, time

User = get_user_model()

class Command(BaseCommand):
    help = 'Popula la base de datos con datos de prueba (seeders)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando el proceso de populación...'))
        fake = Faker('es_ES')  # Usar datos en español

        # --- 1. Crear Pacientes ---
        patients = []
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}_{random.randint(1, 1000)}@fakemail.com"

            patient, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'patient',
                    'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=70),
                    'phone': fake.phone_number()[:8],
                }
            )
            if created:
                patient.set_password('password123')
                patient.save()
                patients.append(patient)

        self.stdout.write(self.style.SUCCESS(f'✅ Creados {len(patients)} pacientes.'))

        # --- 2. Crear Psicólogos y sus Perfiles ---
        specializations = list(Specialization.objects.all())
        if not specializations:
            self.stdout.write(self.style.ERROR('Error: No hay especializaciones. Ejecuta "python manage.py create_specializations" primero.'))
            return

        psychologists = []
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@psico.com"

            psy_user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name,
                    'user_type': 'professional',
                }
            )
            if created:
                psy_user.set_password('password123')
                psy_user.save()
                psychologists.append(psy_user)

                # Crear su perfil profesional
                profile = ProfessionalProfile.objects.create(
                    user=psy_user,
                    license_number=fake.unique.numerify(text='LIC-#####'),
                    bio=fake.paragraph(nb_sentences=3),
                    education=fake.sentence(nb_words=6),
                    experience_years=random.randint(2, 20),
                    consultation_fee=random.choice([150.00, 200.00, 250.00, 300.00]),
                    session_duration=60,
                    city=fake.city(),
                    profile_completed=True
                )
                # Asignar especializaciones aleatorias
                profile.specializations.set(random.sample(specializations, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS(f'✅ Creados {len(psychologists)} psicólogos con sus perfiles.'))

        # --- 3. Crear Citas Falsas ---
        if not psychologists or not patients:
            self.stdout.write(self.style.WARNING('No hay suficientes usuarios para crear citas.'))
            return

        appointment_count = 0
        possible_times = [time(h, m) for h in range(9, 17) for m in [0, 30]] # Horarios de 9 a 5

        for _ in range(100): # Crear 100 citas
            try:
                Appointment.objects.create(
                    patient=random.choice(patients),
                    psychologist=random.choice(psychologists),
                    appointment_date=fake.date_between(start_date='-30d', end_date='+30d'),
                    start_time=random.choice(possible_times),
                    status=random.choice(['pending', 'confirmed', 'completed']),
                    reason_for_visit=fake.sentence()
                )
                appointment_count += 1
            except Exception:
                # Falla silenciosamente si hay un conflicto (ej. cita duplicada para ese psico/hora)
                pass

        self.stdout.write(self.style.SUCCESS(f'✅ Creadas {appointment_count} citas falsas.'))
        self.stdout.write(self.style.WARNING('Recuerda también ejecutar "python manage.py create_availability" para los nuevos psicólogos.'))