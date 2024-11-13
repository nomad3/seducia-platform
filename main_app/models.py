# main_app/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from .utils.base_model import TimestampedModel
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Enumeraciones y opciones
class SessionType(models.TextChoices):
    VOICE = 'voice', 'Voice'
    VIDEO = 'video', 'Video'

class LevelChoices(models.TextChoices):
    BRONZE = 'bronze', 'Bronze'
    SILVER = 'silver', 'Silver'
    GOLD = 'gold', 'Gold'
    PLATINUM = 'platinum', 'Platinum'

class UserRole(models.TextChoices):
    CUSTOMER = 'customer', 'Customer'
    COACH = 'coach', 'Coach'
    ESCORT = 'escort', 'Escort'

# Modelo de perfil de usuario
class UserProfile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.CUSTOMER)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=10, choices=LevelChoices.choices, default=LevelChoices.BRONZE)
    achievements = models.JSONField(default=list)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.10)  # Comisión inicial del 10%
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    benefits = models.JSONField(default=list)  # Lista de beneficios adquiridos

    def __str__(self):
        return f"{self.user.username} Profile"

    def add_points(self, points):
        self.points += points
        self.check_level_up()
        self.save()

    def check_level_up(self):
        previous_level = self.level
        # Lógica de niveles basada en puntos
        if self.points >= 1000:
            self.level = LevelChoices.PLATINUM
        elif self.points >= 500:
            self.level = LevelChoices.GOLD
        elif self.points >= 250:
            self.level = LevelChoices.SILVER
        else:
            self.level = LevelChoices.BRONZE
        if self.level != previous_level:
            self.add_achievement(f"Reached {self.level} Level")
            # Otorgar beneficios adicionales al subir de nivel
            self.apply_level_benefits()

    def apply_level_benefits(self):
        # Definir beneficios por nivel
        level_benefits = {
            LevelChoices.SILVER: {'commission_rate': 0.12, 'gift': 'Exclusive Badge'},
            LevelChoices.GOLD: {'commission_rate': 0.15, 'gift': 'Premium Support'},
            LevelChoices.PLATINUM: {'commission_rate': 0.20, 'gift': 'Featured Profile'},
        }
        benefits = level_benefits.get(self.level, None)
        if benefits:
            self.commission_rate = benefits['commission_rate']
            self.benefits.append(benefits['gift'])
            self.save()

    def add_achievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            self.save()

# Modelo base con timestamps y estado activo
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

# Modelo de fantasía
class Fantasy(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fantasies')
    scenario = models.TextField()
    response = models.TextField(blank=True, null=True)  # Respuesta del chatbot

    def __str__(self):
        return f"Fantasy by {self.user.username}"

# Modelo de prueba de compatibilidad
class CompatibilityTest(TimestampedModel):
    user_1 = models.ForeignKey(User, related_name='compat_tests_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name='compat_tests_2', on_delete=models.CASCADE)
    result = models.JSONField()  # Resultados del test en formato JSON

    def __str__(self):
        return f"Compatibility Test between {self.user_1.username} and {self.user_2.username}"

# Modelo de sesión de coaching
class CoachingSession(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coaching_sessions')
    coach = models.ForeignKey(
        UserProfile,
        limit_choices_to={'role': UserRole.COACH},
        on_delete=models.SET_NULL,
        null=True
    )
    scheduled_time = models.DateTimeField()
    session_type = models.CharField(max_length=5, choices=SessionType.choices)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session with {self.coach.user.username} on {self.scheduled_time}"

    def clean(self):
        if self.scheduled_time < timezone.now():
            raise ValidationError('Scheduled time must be in the future.')

    def complete_session(self):
        if not self.is_completed:
            self.is_completed = True
            self.user.userprofile.add_points(50)
            self.user.userprofile.add_achievement("Session Completed")
            self.save()

# Modelo de producto
class Product(TimestampedModel):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.name

# Modelo de pedido
class Order(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        # Calcular comisión para el proveedor si aplica
        if self.product.provider:
            commission_rate = self.product.provider.userprofile.commission_rate
            self.commission_amount = self.total_price * commission_rate
            self.product.provider.userprofile.total_earnings += self.commission_amount
            self.product.provider.userprofile.save()
        super().save(*args, **kwargs)
        # Otorgar puntos al cliente
        self.user.userprofile.add_points(int(self.total_price))  # 1 punto por cada unidad de moneda gastada

# Modelo de logro
class Achievement(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Modelo de desafío
class Challenge(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.PositiveIntegerField()
    is_daily = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Modelo de recompensa
class Reward(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost_in_points = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Modelo de redención de recompensas
class Redemption(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name}"

class Benefit(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    required_level = models.CharField(max_length=10, choices=LevelChoices.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class EscortProfile(TimestampedModel):
    external_id = models.CharField(max_length=255, unique=True)
    provider_name = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    services = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Descripción enriquecida con LangChain
    categories = models.JSONField(default=list)  # Categorías analizadas con LangChain

    def __str__(self):
        return f"{self.name} from {self.provider_name}"

class Mission(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_reward = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Friendship(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"