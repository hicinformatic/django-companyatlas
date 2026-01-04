from django.db import models
from django.utils.translation import gettext_lazy as _
from ..managers.virtuals.event import CompanyAtlasVirtualEventManager

class CompanyAtlasVirtualEvent(models.Model):
    """Virtual event model for companyatlas."""

    objects = CompanyAtlasVirtualEventManager

    class Meta:
        managed = False
        verbose_name = _("Company Atlas Virtual Event")
        verbose_name_plural = _("Company Atlas Virtual Events")

    