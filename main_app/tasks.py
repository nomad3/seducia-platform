# main_app/tasks.py

from celery import shared_task
from .services.scraper import EscortScraperManager
from .models import UserProfile
import logging


@shared_task
def adjust_commission_rates():
    providers = UserProfile.objects.filter(role__in=[UserRole.COACH, UserRole.ESCORT])
    for provider in providers:
        # Ajustar la tasa de comisión según el total de ganancias o desempeño
        if provider.total_earnings >= 10000:
            provider.commission_rate = 0.25  # Aumentar la comisión al 25%
        elif provider.total_earnings >= 5000:
            provider.commission_rate = 0.20  # Comisión del 20%
        elif provider.total_earnings >= 1000:
            provider.commission_rate = 0.15  # Comisión del 15%
        else:
            provider.commission_rate = 0.10  # Comisión base del 10%
        provider.save()

@shared_task
def send_special_offers():
    from django.core.mail import send_mail
    customers = UserProfile.objects.filter(role=UserRole.CUSTOMER)
    for customer in customers:
        # Lógica para determinar si el cliente es elegible para una oferta
        if customer.points >= 500:
            # Enviar correo electrónico con una oferta especial
            send_mail(
                'Special Offer from Seducia',
                'Dear {},\n\nYou have earned a special offer! Use code SPECIAL500 for a discount.'.format(customer.user.username),
                'noreply@seducia.com',
                [customer.user.email],
                fail_silently=True,
            )

logger = logging.getLogger(__name__)

@shared_task
def run_escort_scraper():
    try:
        scraper = EscortScraperManager()
        scraper.scrape_all()
        logger.info("Escort scraper completed successfully.")
    except Exception as e:
        logger.error(f"Error running escort scraper: {e}")

@shared_task
def run_marketing_campaign():
    from .models import EscortProfile
    from .services.social_media import SocialMediaManager

    profiles = EscortProfile.objects.filter(is_active=True)
    social_media_manager = SocialMediaManager(api_keys=SOCIAL_MEDIA_API_KEYS)

    for profile in profiles:
        social_media_manager.post_profile(profile)