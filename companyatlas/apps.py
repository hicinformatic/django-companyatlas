"""Django app configuration."""

from django.apps import AppConfig


class CompanyAtlasConfig(AppConfig):
    """Configuration for the companyatlas app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "companyatlas"
    verbose_name = "Company Atlas"

    def ready(self):
        """Import and register admin after apps are ready to avoid AppRegistryNotReady."""
        try:
            from django.contrib import admin

            from .admin.backend import BackendInfoAdmin
            from .models.backend import BackendInfo

            admin.site.register(BackendInfo, BackendInfoAdmin)
        except (ImportError, Exception):
            pass
