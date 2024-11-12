# main_app/services/langchain_integration.py

from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langsmith import Client as LangsmithClient

class LangChainIntegration:
    def __init__(self):
        # Inicializamos el modelo de lenguaje
        self.llm = OpenAI(api_key=LANGCHAIN_API_KEY)
        self.client = LangsmithClient(api_key=LANGSMITH_API_KEY)

        # Definimos el prompt para generar la descripción
        self.description_prompt = PromptTemplate(
            input_variables=["name", "services", "location"],
            template="Write a professional and appealing description for an escort named {name}, offering {services} in {location}.",
        )

        # Definimos el prompt para categorizar el perfil
        self.categorization_prompt = PromptTemplate(
            input_variables=["services"],
            template="Categorize the following services into a list of standardized categories: {services}.",
        )

        # Creamos cadenas de procesamiento
        self.description_chain = LLMChain(llm=self.llm, prompt=self.description_prompt)
        self.categorization_chain = LLMChain(llm=self.llm, prompt=self.categorization_prompt)

    def process_profile(self, profile):
        # Generamos la descripción
        description_input = {
            "name": profile['name'],
            "services": profile.get('services', ''),
            "location": profile.get('location', ''),
        }
        description = self.description_chain.run(description_input)

        # Categorizamos los servicios
        categorization_input = {"services": profile.get('services', '')}
        categories_text = self.categorization_chain.run(categorization_input)
        categories = [cat.strip() for cat in categories_text.split(',')]

        # Opcional: Registrar en Langsmith para análisis y seguimiento
        self.client.log_data(
            model='OpenAI',
            input_data=description_input,
            output_data={'description': description, 'categories': categories},
            metadata={'provider': profile['provider_name'], 'external_id': profile['external_id']}
        )

        return description, categories
