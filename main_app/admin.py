# main_app/admin.py

from django.contrib import admin
from .models import (
    UserProfile, Fantasy, CompatibilityTest, CoachingSession,
    Product, Order, Achievement, Challenge, Reward, Redemption,
    Benefit, EscortProfile, Mission, Friendship, EscortProfile
)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Registro del modelo UserProfile con opciones personalizadas
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role', 'get_level', 'get_points')
    list_select_related = ('userprofile',)

    def get_role(self, instance):
        return instance.userprofile.role
    get_role.short_description = 'Role'

    def get_level(self, instance):
        return instance.userprofile.level
    get_level.short_description = 'Level'

    def get_points(self, instance):
        return instance.userprofile.points
    get_points.short_description = 'Points'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registro del modelo Fantasy
@admin.register(Fantasy)
class FantasyAdmin(admin.ModelAdmin):
    list_display = ('user', 'scenario', 'created_at')
    search_fields = ('user__username', 'scenario')
    list_filter = ('created_at',)

# Registro del modelo CompatibilityTest
@admin.register(CompatibilityTest)
class CompatibilityTestAdmin(admin.ModelAdmin):
    list_display = ('user_1', 'user_2', 'created_at')
    search_fields = ('user_1__username', 'user_2__username')
    list_filter = ('created_at',)

# Registro del modelo CoachingSession
@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'coach', 'scheduled_time', 'session_type', 'is_completed')
    search_fields = ('user__username', 'coach__user__username')
    list_filter = ('session_type', 'is_completed', 'scheduled_time')
    date_hierarchy = 'scheduled_time'

# Registro del modelo Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'provider')
    search_fields = ('name', 'provider__username')
    list_filter = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'is_paid', 'commission_amount')
    search_fields = ('user__username', 'product__name')
    list_filter = ('is_paid', 'created_at')
    readonly_fields = ('total_price', 'commission_amount', 'created_at', 'updated_at')

# Registro del modelo Achievement
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_reward')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Challenge
@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_reward', 'is_daily')
    search_fields = ('name',)
    list_filter = ('is_daily',)
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Reward
@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_in_points')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Redemption
@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'redeemed_at')
    search_fields = ('user__username', 'reward__name')
    readonly_fields = ('redeemed_at',)

# Registro del modelo Benefit
@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_level', 'is_active')
    search_fields = ('name',)
    list_filter = ('required_level', 'is_active')
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo EscortProfile
class EscortProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'location', 'provider_name')
    search_fields = ('name', 'location', 'provider_name')
    list_filter = ('location',)
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Mission
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'start_date', 'end_date')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')

# Registro del modelo Friendship
@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'created_at')
    search_fields = ('user__username', 'friend__username')
    readonly_fields = ('created_at',)

# Configuración adicional para el modelo UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'level', 'points', 'total_earnings')
    search_fields = ('user__username', 'user__email')
    list_filter = ('role', 'level')
    readonly_fields = ('points', 'level', 'total_earnings', 'achievements', 'benefits', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'role', 'bio', 'profile_picture')
        }),
        ('Status', {
            'fields': ('points', 'level', 'achievements', 'benefits')
        }),
        ('Earnings', {
            'fields': ('commission_rate', 'total_earnings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(EscortProfile)
class EscortProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_name', 'age', 'location')
    search_fields = ('name', 'provider_name', 'location')
    list_filter = ('provider_name', 'location')
    readonly_fields = ('created_at', 'updated_at')