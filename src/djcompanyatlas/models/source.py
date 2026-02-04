from django.db import models
from django.utils.translation import gettext_lazy as _


COMPANYATLAS_FIELDS_SOURCE = [
    "source",
    "country_code",
    "metadata",
    "created_at",
    "updated_at",
]

class CompanyAtlasSourceBase(models.Model):
    """Abstract base class for company-related models with source and country."""

    source = models.CharField(
        max_length=100,
        verbose_name=_("Source"),
        help_text=_("Backend source (e.g., 'insee', 'bodacc', 'inpi')"),
        blank=True,
        null=True,
    )
    country_code = models.CharField(
        max_length=2,
        verbose_name=_("Country Code"),
        help_text=_("ISO country code (e.g., FR, US, GB)"),
        blank=True,
        null=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional metadata"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["source", "country_code"]),
            models.Index(fields=["country_code"]),
        ]
