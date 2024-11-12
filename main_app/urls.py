# main_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, FantasyViewSet, CompatibilityTestViewSet, CoachingSessionViewSet,
    ProductViewSet, OrderViewSet, AchievementViewSet, ChallengeViewSet, RewardViewSet, RedemptionViewSet, BenefitViewSet
)

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'fantasies', FantasyViewSet)
router.register(r'compatibility_tests', CompatibilityTestViewSet)
router.register(r'coaching_sessions', CoachingSessionViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'challenges', ChallengeViewSet)
router.register(r'rewards', RewardViewSet)
router.register(r'redemptions', RedemptionViewSet)
router.register(r'benefits', BenefitViewSet)



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/escort_profiles/', views.EscortProfileListView.as_view(), name='escort_profiles'),
    path('api/v1/run_scraper/', views.RunScraperView.as_view(), name='run_scraper'),
]
