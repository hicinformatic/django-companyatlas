from django.db import models
from django.utils.translation import gettext_lazy as _

from .company import CompanyAtlasCompany
from .source import CompanyAtlasSourceBase


class CompanyAtlasDocument(CompanyAtlasSourceBase):
    """Company documents from various backends."""

    company = models.ForeignKey(
        CompanyAtlasCompany,
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
