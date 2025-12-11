"""Company models with international and country-specific data."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """Company model - parent model for company data, documents, and events."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Company name"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Company description"),
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
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name


class CompanySourceBase(models.Model):
    """Abstract base class for company-related models with source and country."""

    source = models.CharField(
        max_length=100,
        verbose_name=_("Source"),
        help_text=_("Backend source (e.g., 'insee', 'pappers', 'infogreffe')"),
    )
    country_code = models.CharField(
        max_length=2,
        verbose_name=_("Country Code"),
        help_text=_("ISO country code (e.g., FR, US, GB)"),
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["source", "country_code"]),
            models.Index(fields=["country_code"]),
        ]


class CompanyData(CompanySourceBase):
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

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
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


class CompanyDocument(CompanySourceBase):
    """Company documents from various backends."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Company"),
        help_text=_("Company this document belongs to"),
    )
    document_type = models.CharField(
        max_length=100,
        verbose_name=_("Document Type"),
        help_text=_("Type of document (e.g., bodacc, kbis, balo)"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Document title"),
    )
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date"),
        help_text=_("Document date"),
    )
    url = models.URLField(
        blank=True,
        verbose_name=_("URL"),
        help_text=_("URL to access the document"),
    )
    content = models.TextField(
        blank=True,
        verbose_name=_("Content"),
        help_text=_("Document content or summary"),
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional document metadata"),
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
        verbose_name = _("Company Document")
        verbose_name_plural = _("Company Documents")
        indexes = [
            models.Index(fields=["company", "country_code"]),
            models.Index(fields=["document_type"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.source} - {self.document_type}"


class CompanyEvent(CompanySourceBase):
    """Company events from various backends."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("Company"),
        help_text=_("Company this event belongs to"),
    )
    event_type = models.CharField(
        max_length=100,
        verbose_name=_("Event Type"),
        help_text=_("Type of event (e.g., status_change, modification, capital_change)"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Event title"),
    )
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date"),
        help_text=_("Event date"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Event description"),
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional event metadata"),
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
        verbose_name = _("Company Event")
        verbose_name_plural = _("Company Events")
        indexes = [
            models.Index(fields=["company", "country_code"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.source} - {self.event_type}"
