"""Company models with international and country-specific data."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from .source import CompanyAtlasSourceBase


class Company(CompanyAtlasSourceBase):
    """Company model - parent model for company data, documents, and events."""

    denomination = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Company name"),
    )


    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

class CompanyData(CompanyAtlasSourceBase):
    """Company data from various backends."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="data",
        verbose_name=_("Company"),
        help_text=_("Company this data belongs to"),
    )
    data_type = models.CharField(
        max_length=100,
        verbose_name=_("Data Type"),
        help_text=_("Type of data (e.g., denomination, siren, capital, employees)"),
    )
    value = models.TextField(
        verbose_name=_("Value"),
        help_text=_("Data value"),
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

    class Meta:
        verbose_name = _("Company Data")
        verbose_name_plural = _("Company Data")
        unique_together = [["company", "source", "country_code", "data_type"]]
        indexes = [
            models.Index(fields=["company", "country_code"]),
            models.Index(fields=["data_type"]),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.source} - {self.country_code} - {self.data_type}"

    def get_value(self):
        """Get the value converted to its proper type."""
        if self.value_type == "int":
            try:
                return int(self.value)
            except (ValueError, TypeError):
                return None
        elif self.value_type == "float":
            try:
                return float(self.value)
            except (ValueError, TypeError):
                return None
        elif self.value_type == "json":
            import json

            try:
                return json.loads(self.value)
            except (json.JSONDecodeError, TypeError):
                return None
        else:
            return self.value

    def set_value(self, value):
        """Set the value, automatically detecting the type."""
        if isinstance(value, (dict, list)):
            import json

            self.value = json.dumps(value)
            self.value_type = "json"
        elif isinstance(value, int):
            self.value = str(value)
            self.value_type = "int"
        elif isinstance(value, float):
            self.value = str(value)
            self.value_type = "float"
        else:
            self.value = str(value)
            self.value_type = "str"

