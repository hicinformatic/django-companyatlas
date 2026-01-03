"""Django app configuration."""

from django.apps import AppConfig


class CompanyAtlasConfig(AppConfig):
    """Configuration for the companyatlas app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "djcompanyatlas"
    verbose_name = "Company Atlas"

    def ready(self):
        """Import and register admin after apps are ready to avoid AppRegistryNotReady."""
        try:
            import os
            import logging
            logger = logging.getLogger(__name__)
            
            companyatlas_vars = {k: v[:20] + "..." if len(v) > 20 else v 
                                for k, v in os.environ.items() 
                                if k.startswith('COMPANYATLAS_')}
            if companyatlas_vars:
                logger.info(f"CompanyAtlas environment variables loaded: {', '.join(companyatlas_vars.keys())}")
                for key, value in sorted(companyatlas_vars.items()):
                    logger.info(f"  {key}: {value}")
            else:
                logger.info("No CompanyAtlas environment variables found")
            
            from django.contrib import admin
            from django.contrib.admin.exceptions import AlreadyRegistered

            from .admin import get_admin_urls
            from .admin.backend import BackendInfoAdmin
            from .admin.backend_search import BackendSearchResultAdmin
            from .models.backend import BackendInfo
            from .models.backend_search import BackendSearchResult

            try:
                admin.site.register(BackendInfo, BackendInfoAdmin)
            except AlreadyRegistered:
                pass

            try:
                admin.site.register(BackendSearchResult, BackendSearchResultAdmin)
            except AlreadyRegistered:
                pass

            original_get_urls = admin.site.get_urls

            def get_urls_with_custom():
                custom_urls = get_admin_urls()
                default_urls = original_get_urls()
                return custom_urls + default_urls

            admin.site.get_urls = get_urls_with_custom
        except (ImportError, Exception) as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Error registering admin URLs: {e}", exc_info=True)
