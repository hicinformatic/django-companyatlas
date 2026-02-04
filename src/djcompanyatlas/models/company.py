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
        return f"{self.company.denomination} - {self.source} - {self.country_code} - {self.data_type}"

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
