# main_app/views.py

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    UserProfile, Fantasy, CompatibilityTest, CoachingSession,
    Product, Order, Achievement, Challenge, Reward, Redemption, Benefit, EscortProfile
)
from .serializers import (
    UserProfileSerializer, FantasySerializer, CompatibilityTestSerializer, CoachingSessionSerializer,
    ProductSerializer, OrderSerializer, AchievementSerializer, ChallengeSerializer, RewardSerializer, RedemptionSerializer, BenefitSerializer, EscortProfileSerializer
)
from .permissions import IsOwnerOrReadOnly, IsCoach
from django.shortcuts import get_object_or_404

# Vista de perfil de usuario
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_benefits(self, request):
        profile = request.user.userprofile
        benefits = Benefit.objects.filter(required_level__lte=profile.level, is_active=True)
        serializer = BenefitSerializer(benefits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_earnings(self, request):
        profile = request.user.userprofile
        return Response({'total_earnings': profile.total_earnings})

# Vista de fantasías
class FantasyViewSet(viewsets.ModelViewSet):
    queryset = Fantasy.objects.all()
    serializer_class = FantasySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Lógica para generar respuesta del chatbot usando LangChain aquí

# Vista de pruebas de compatibilidad
class CompatibilityTestViewSet(viewsets.ModelViewSet):
    queryset = CompatibilityTest.objects.all()
    serializer_class = CompatibilityTestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_1=self.request.user)
        # Lógica para generar resultado de compatibilidad usando IA

# Vista de sesiones de coaching
class CoachingSessionViewSet(viewsets.ModelViewSet):
    queryset = CoachingSession.objects.all()
    serializer_class = CoachingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete_session(self, request, pk=None):
        session = self.get_object()
        session.complete_session()
        return Response({'status': 'session completed'}, status=status.HTTP_200_OK)

# Vista de productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista de pedidos
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError("Not enough stock available.")
        product.stock -= quantity
        product.save()
        serializer.save(user=self.request.user)
        # La lógica de otorgar puntos y comisiones se maneja en el modelo `Order`

# Vista de logros
class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista de desafíos
class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista de recompensas
class RewardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista de redenciones
class RedemptionViewSet(viewsets.ModelViewSet):
    queryset = Redemption.objects.all()
    serializer_class = RedemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reward = serializer.validated_data['reward']
        user_profile = self.request.user.userprofile
        if user_profile.points >= reward.cost_in_points:
            user_profile.points -= reward.cost_in_points
            user_profile.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("Not enough points to redeem this reward.")

class BenefitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Benefit.objects.filter(is_active=True)
    serializer_class = BenefitSerializer
    permission_classes = [permissions.IsAuthenticated]


class EscortProfileListView(generics.ListAPIView):
    queryset = EscortProfile.objects.all()
    serializer_class = EscortProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class RunScraperView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        run_escort_scraper.delay()
        return Response({'status': 'Scraper started.'})