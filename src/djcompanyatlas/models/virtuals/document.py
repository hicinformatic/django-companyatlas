from django.db import models
from django.utils.translation import gettext_lazy as _

from ...managers.virtuals.document import CompanyAtlasVirtualDocumentManager


class CompanyAtlasVirtualDocument(models.Model):
    """Virtual document model for companyatlas."""

    objects = CompanyAtlasVirtualDocumentManager()

    class Meta:
        managed = False
        verbose_name = _("Virtual Document")
        verbose_name_plural = _("Virtual Documents")

