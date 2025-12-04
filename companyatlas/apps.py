"""Django app configuration."""

from django.apps import AppConfig


class CompanyAtlasConfig(AppConfig):
    """Configuration for the companyatlas app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "companyatlas"
    verbose_name = "Company Atlas"

