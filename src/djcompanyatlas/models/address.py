"""Company address models."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from djgeoaddress.fields import GeoaddressField

from .company import CompanyAtlasCompany
from .source import CompanyAtlasSourceBase


class CompanyAtlasAddress(CompanyAtlasSourceBase):
    """Company addresses from various backends."""

    company = models.ForeignKey(
        CompanyAtlasCompany,
        on_delete=models.CASCADE,
        related_name="to_companyatlasaddress",
        verbose_name=_("Company"),
        help_text=_("Company this address belongs to"),
    )
    address = GeoaddressField(
        verbose_name=_("Address"),
        help_text=_("Company address"),
    )
    is_headquarters = models.BooleanField(
        default=False,
        verbose_name=_("Is headquarters"),
        help_text=_("Whether this address is the company's headquarters"),
    )

    class Meta:
        verbose_name = _("Company Address")
        verbose_name_plural = _("Company Addresses")
        indexes = [
            models.Index(fields=["company", "address"]),
            models.Index(fields=["company", "is_headquarters"]),
        ]
        ordering = ["-is_headquarters", "-created_at"]

    def __str__(self):
        return f"{self.company.denomination} - {self.address}"
