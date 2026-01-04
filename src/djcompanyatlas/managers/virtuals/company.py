from django.db import models
from django.utils.translation import gettext_lazy as _
from ..managers.virtuals.company import CompanyAt

class CompanyAtlasVirtualCompany(models.Model):
    """Virtual company model for companyatlas."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = 

    class Meta:
        managed = False
        verbose_name = _("Company Atlas Virtual Company")
        verbose_name_plural = _("Company Atlas Virtual Companies")

    