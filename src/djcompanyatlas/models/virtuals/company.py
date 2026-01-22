from django.db import models
from django.utils.translation import gettext_lazy as _

from ...managers.virtuals.company import CompanyAtlasVirtualCompanyManager


class CompanyAtlasVirtualCompany(models.Model):
    """Virtual company model for companyatlas."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    objects = CompanyAtlasVirtualCompanyManager()

    class Meta:
        managed = False
        verbose_name = _("Virtual Company")
        verbose_name_plural = _("Virtual Companies")

