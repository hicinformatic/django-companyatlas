"""Company data models."""


from django.db import models
from django.utils.translation import gettext_lazy as _

from .company import CompanyAtlasCompany
from .referentiel import CompanyAtlasReferentiel
from .source import CompanyAtlasSourceBase


class CompanyAtlasData(CompanyAtlasSourceBase):
    """Company data from various backends."""

    company = models.ForeignKey(
        CompanyAtlasCompany,
        on_delete=models.CASCADE,
        related_name="to_companyatlasdata",
        verbose_name=_("Company"),
        help_text=_("Company this data belongs to"),
    )
    data_type = models.CharField(
        max_length=100,
        verbose_name=_("Data Type"),
        help_text=_("Type of data (e.g., denomination, siren, capital, employees)"),
    )
    value_type = models.CharField(
        max_length=10,
        verbose_name=_("Value Type"),
        choices=[
            ("str", _("String")),
            ("int", _("Integer")),
            ("float", _("Float")),
            ("json", _("JSON")),
        ],
        default="str",
        help_text=_("Type of the value (str, int, float, json)"),
    )
    value = models.TextField(
        verbose_name=_("Value"),
        help_text=_("Data value"),
    )
    referentiel = models.ManyToManyField(
        CompanyAtlasReferentiel,
        verbose_name=_("Referentiel"),
        help_text=_("Referentiel this data belongs to"),
        related_name="to_companyatlasdata",
        blank=True,
    )

    class Meta:
        verbose_name = _("Company Data")
        verbose_name_plural = _("Company Data")
        unique_together = [["company", "source", "country_code", "data_type"]]
        indexes = [
            models.Index(fields=["company", "country_code"]),
            models.Index(fields=["data_type"]),
        ]
        ordering = ["data_type", "-created_at"]

    def __str__(self):
        return (
            f"{self.company.denomination} - {self.source} - "
            f"{self.country_code} - {self.data_type}"
        )

    @property
    def referentiel_description(self):
        return self.sql_referentiel_description
