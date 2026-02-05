"""Company models with international and country-specific data."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from namedid.fields import NamedIDField
from .source import CompanyAtlasSourceBase
from ..managers.company import CompanyAtlasCompanyManager

COMPANYATLAS_FIELDS_COMPANY = [
    "denomination",
    "code",
    "named_id",
]

class CompanyAtlasCompany(CompanyAtlasSourceBase):
    """Company model - parent model for company data, documents, and events."""
    denomination = models.CharField(
        max_length=255,
        verbose_name=_("Denomination"),
        help_text=_("Company denomination"),
    )
    code = models.CharField(
        max_length=255,
        verbose_name=_("Code"),
        help_text=_("Company code"),
    )
    named_id = NamedIDField(
        source_fields=["denomination", "code"],
        verbose_name=_("Named ID"),
        help_text=_("Named ID"),
    )

    objects = CompanyAtlasCompanyManager()

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.denomination} - {self.code}"

    @property
    def headquarters_address(self):
        return self.to_companyatlasaddress.filter(is_headquarters=True).first()
