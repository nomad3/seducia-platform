# main_app/services/scraper.py

from .providers.provider_a import ProviderA
from .providers.provider_b import ProviderB
from main_app.models import EscortProfile
from .langchain_integration import LangChainIntegration
import logging

logger = logging.getLogger(__name__)

class EscortScraperManager:
    def __init__(self):
        self.providers = [ProviderA(), ProviderB()]
        self.langchain_integration = LangChainIntegration()

    def scrape_all(self):
        for provider in self.providers:
            try:
                profiles = provider.fetch_profiles()
                enriched_profiles = self.enrich_profiles(profiles)
                self.save_profiles(enriched_profiles)
            except Exception as e:
                logger.error(f"Error scraping {provider.__class__.__name__}: {e}")

    def enrich_profiles(self, profiles):
        enriched_profiles = []
        for profile in profiles:
            # Utilizamos LangChain para enriquecer el perfil
            description, categories = self.langchain_integration.process_profile(profile)
            profile['description'] = description
            profile['categories'] = categories
            enriched_profiles.append(profile)
        return enriched_profiles

    def save_profiles(self, profiles):
        for data in profiles:
            EscortProfile.objects.update_or_create(
                external_id=data['external_id'],
                defaults={
                    'provider_name': data['provider_name'],
                    'name': data['name'],
                    'age': data.get('age'),
                    'location': data.get('location'),
                    'services': data.get('services'),
                    'image_url': data.get('image_url'),
                    'description': data.get('description'),
                    'categories': data.get('categories', []),
                }
            )
