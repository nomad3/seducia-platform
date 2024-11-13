FROM python:3.10-slim

# Crear un usuario no root
RUN useradd -ms /bin/bash appuser

WORKDIR /app

# Copiar el archivo de requerimientos y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear el directorio 'static' si no existe
RUN mkdir -p /app/static

# Limpiar archivos de caché (opcional)
RUN find . -name "*.pyc" -delete && find . -name "__pycache__" -delete

# Ejecutar collectstatic
RUN python manage.py collectstatic --noinput

# Cambiar la propiedad de los archivos al usuario no root
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

EXPOSE 8000

# Comando para iniciar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "seducia.wsgi:application"]
