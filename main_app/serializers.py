# main_app/serializers.py

from rest_framework import serializers
from .models import (
    UserProfile, Fantasy, CompatibilityTest, CoachingSession,
    Product, Order, Achievement, Challenge, Reward, Redemption, Benefit, EscortProfile
)
from django.contrib.auth.models import User

# Serializador de usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializador de perfil de usuario
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    commission_rate = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    benefits = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['points', 'level', 'achievements', 'total_earnings', 'commission_rate', 'benefits']

# Serializador de fantasía
class FantasySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Fantasy
        fields = '__all__'

# Serializador de prueba de compatibilidad
class CompatibilityTestSerializer(serializers.ModelSerializer):
    user_1 = serializers.StringRelatedField(read_only=True)
    user_2 = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CompatibilityTest
        fields = '__all__'

# Serializador de sesión de coaching
class CoachingSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    coach = UserProfileSerializer(read_only=True)

    class Meta:
        model = CoachingSession
        fields = '__all__'

    def validate_scheduled_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value

# Serializador de producto
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Serializador de pedido
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = ProductSerializer()
    commission_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total_price', 'commission_amount']

# Serializador de logro
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

# Serializador de desafío
class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

# Serializador de recompensa
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

# Serializador de redención
class RedemptionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    reward = RewardSerializer()

    class Meta:
        model = Redemption
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class EscortProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscortProfile
        fields = '__all__'