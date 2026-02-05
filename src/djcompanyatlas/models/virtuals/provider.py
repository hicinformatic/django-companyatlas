"""Provider model for companyatlas providers."""

from companyatlas.helpers import ADD_FIELDS
from companyatlas.providers import CompanyAtlasProvider
from django.db import models
from django.utils.translation import gettext_lazy as _
from djproviderkit.models.service import define_provider_fields, define_service_fields
from virtualqueryset.models import VirtualModel

from ...managers.virtuals.provider import CompanyAtlasProviderManager

_default_cfg = getattr(CompanyAtlasProvider, '_default_services_cfg', {})
services_cfg = getattr(CompanyAtlasProvider, 'services_cfg', _default_cfg)
services = list(services_cfg.keys())

@define_provider_fields(primary_key='name', add_fields=ADD_FIELDS)
@define_service_fields(services)
class CompanyAtlasProviderModel(VirtualModel):
    """Virtual model for companyatlas providers."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Provider name (e.g., insee)"),
        primary_key=True,
    )

    objects = CompanyAtlasProviderManager()

    class Meta:
        managed = False
        app_label = 'djcompanyatlas'
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")
        ordering = ['-priority', 'name']

    def __str__(self) -> str:
        return self.display_name or self.name
