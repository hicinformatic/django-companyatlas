"""Django CompanyAtlas - Company information management."""

from django.db import models

__all__ = []

# Version
__version__ = "0.1.0"

fields_associations = {
    'int': models.IntegerField,
    'float': models.FloatField,
    'bool': models.BooleanField,
    'list': models.JSONField,
    'str': models.CharField,
    'text': models.TextField,
    'date': models.DateField,
    'time': models.TimeField,
    'datetime': models.DateTimeField,
    'email': models.EmailField,
    'url': models.URLField,
}
