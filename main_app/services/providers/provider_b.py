# main_app/services/providers/provider_b.py

from .base_provider import Provider
import requests
from bs4 import BeautifulSoup

class ProviderB(Provider):
    BASE_URL = "https://anotherexample.com"

    def fetch_profiles(self):
        profiles = []
        response = requests.get(f"{self.BASE_URL}/listings")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lógica de scraping específica para Provider B
        for listing in soup.select('.listing'):
            profile_data = {
                'external_id': listing['data-id'],
                'provider_name': 'Provider B',
                'name': listing.select_one('.title').text.strip(),
                'age': None,  # Datos no disponibles
                'location': listing.select_one('.city').text.strip(),
                'services': listing.select_one('.details').text.strip(),
                'image_url': listing.select_one('.image')['data-src'],
            }
            profiles.append(profile_data)
        return profiles
