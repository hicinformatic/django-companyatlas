from django.db import models
from django.utils.translation import gettext_lazy as _
from .company import Company
from .source import CompanyAtlasSourceBase

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
