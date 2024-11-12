# Seducia

**Seducia** es una plataforma avanzada de exploración y coaching de intimidad que utiliza IA y gamificación para ofrecer experiencias únicas de fantasías, pruebas de compatibilidad, coaching en vivo, servicios para adultos y una tienda de productos de última generación. Esta plataforma está diseñada para ser segura, privada, y altamente personalizada.

## Características

- **Chatbot de Fantasías**: Chatbot impulsado por IA para escenarios personalizados.
- **Prueba de Compatibilidad para Parejas**: Prueba mejorada por IA que ayuda a explorar y mejorar la compatibilidad.
- **Coaching en Tiempo Real**: Sesiones en vivo con coaches de intimidad, facilitadores de fantasías y más.
- **Integración de Productos**: Venta de productos y juguetes sexuales con entrega discreta.
- **Gamificación**: Sistema de puntos, logros, niveles y desafíos para hacer la plataforma más entretenida.
- **Marketing Automatizado**: Integración con redes sociales como Facebook, Instagram, Tinder, Threads, y Grinder.

## Requisitos

- Python 3.10+
- PostgreSQL
- Redis (para manejar tareas asíncronas con Celery)
- Django-environ para gestionar variables de entorno
- Docker y Docker Compose (opcional para desarrollo local)

## Configuración del Proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/seducia.git
cd seducia
```

### 2. Crea un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

Asegúrate de tener `django-environ` y otras dependencias instaladas.

```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno

Para cargar las variables de entorno, utiliza el archivo `.env`. Crea un archivo `.env` en el directorio raíz del proyecto y define las siguientes variables (asegúrate de reemplazar con tus valores):

```plaintext
SECRET_KEY=tu-secreto
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
POSTGRES_DB=seducia_db
POSTGRES_USER=seducia_user
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys
LANGCHAIN_API_KEY=tu_langchain_api_key
LANGSMITH_API_KEY=tu_langsmith_api_key
FACEBOOK_API_KEY=tu_facebook_api_key
INSTAGRAM_API_KEY=tu_instagram_api_key
TINDER_API_KEY=tu_tinder_api_key
THREADS_API_KEY=tu_threads_api_key
GRINDER_API_KEY=tu_grinder_api_key
```

### 5. Configuración de la base de datos

Asegúrate de tener PostgreSQL configurado y luego aplica las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear un superusuario

Para acceder al panel de administración de Django, crea un superusuario:

```bash
python manage.py createsuperuser
```

### 7. Cargar datos iniciales

Si deseas cargar datos iniciales para probar la plataforma, puedes usar fixtures o un script de prueba (opcional).

### 8. Iniciar el servidor de desarrollo

Ejecuta el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

Accede a la plataforma en `http://127.0.0.1:8000`.

## Uso de Docker

Para ejecutar la aplicación en Docker, usa `docker-compose`:

1. Asegúrate de tener Docker y Docker Compose instalados.
2. Ejecuta el siguiente comando:

```bash
docker-compose up --build
```

Esto iniciará los contenedores para la aplicación Django, Redis y PostgreSQL.

## Tareas Periódicas con Celery y Redis

Seducia utiliza Celery para manejar tareas asíncronas, como la asignación de desafíos y notificaciones. Las tareas programadas están configuradas con `django-celery-beat` y pueden gestionarse desde el panel de administración.

Para iniciar los trabajadores de Celery, utiliza:

```bash
# Trabajador de Celery
celery -A seducia worker -l info

# Tareas periódicas de Celery
celery -A seducia beat -l info
```

Si estás usando Docker Compose, estos servicios se levantarán automáticamente.

## Despliegue en Render

1. **Configura las variables de entorno** en la sección "Environment" del panel de Render. Agrega todas las variables que están en el archivo `.env`.

2. **Despliegue de la aplicación**: Render detectará automáticamente el repositorio y aplicará las configuraciones al iniciar la aplicación.

## Tecnologías Utilizadas

- **Django**: Framework web backend.
- **Django Rest Framework**: Para crear la API de la plataforma.
- **Celery**: Tareas asíncronas para desafíos diarios y manejo de eventos.
- **Redis**: Broker para tareas de Celery.
- **PostgreSQL**: Base de datos relacional.
- **LangChain y LangSmith**: Herramientas de IA para crear experiencias personalizadas y marketing automatizado.
- **Docker**: Para contenedores y despliegue.
- **Render**: Servicio de despliegue en la nube.

## Gamificación

La plataforma incorpora un sistema de gamificación para motivar la interacción del usuario, incluyendo:

- **Sistema de puntos**: Los usuarios ganan puntos por completar acciones y pueden usarlos para canjear recompensas.
- **Logros y distintivos**: Los usuarios desbloquean logros por completar actividades específicas.
- **Niveles**: Los niveles de usuario (Bronce, Plata, Oro, Platino) desbloquean beneficios exclusivos.
- **Desafíos diarios y semanales**: Actividades para fomentar la participación constante.
- **Tablas de clasificación**: Clasificaciones de los usuarios y proveedores más activos.

## Contribuciones

Si deseas contribuir a **Seducia**, por favor, crea un fork del repositorio y realiza una pull request. Nos encantaría recibir tus contribuciones.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

---

Con esta guía, podrás desplegar y operar **Seducia** en tu entorno local o en Render, y disfrutar de todas sus funcionalidades avanzadas.
```

Este archivo `README.md` cubre todos los aspectos importantes del proyecto, desde las instrucciones de configuración y despliegue hasta una descripción completa de las características y tecnologías utilizadas. También proporciona una guía para contribuir y una sección de contacto para soporte.