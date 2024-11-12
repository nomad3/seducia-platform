# main_app/utils/base_model.py

from django.db import models

class TimestampedModel(models.Model):
    """
    Modelo base abstracto que proporciona campos de timestamp y estado activo.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
