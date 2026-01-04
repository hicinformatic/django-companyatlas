from django.db import models
from django.utils.translation import gettext_lazy as _
from ..managers.virtuals.CompanyAtlasVirtualDocumentManager import CompanyAtlasVirtualCompanyManager

class CompanyAtlasVirtualCompany(models.Model):
    """Virtual company model for companyatlas."""



    objects = CompanyAtlasVirtualDocumentManager

    class Meta:
        managed = False
        verbose_name = _("Company Atlas Virtual Document")
        verbose_name_plural = _("Company Atlas Virtual Documents")

    