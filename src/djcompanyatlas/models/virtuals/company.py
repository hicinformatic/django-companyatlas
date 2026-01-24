"""Company suggestion model for companyatlas."""

from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _
from companyatlas import COMPANYATLAS_SEARCH_COMPANY_FIELDS
from djproviderkit.models.service import define_fields_from_config
from virtualqueryset.models import VirtualModel

from djcompanyatlas.managers.virtuals.company import CompanyAtlasVirtualCompanyManager

FIELDS_COMPANYATLAS = COMPANYATLAS_SEARCH_COMPANY_FIELDS

companyatlas_id_config: dict[str, Any] = FIELDS_COMPANYATLAS['companyatlas_id']


@define_fields_from_config(FIELDS_COMPANYATLAS, primary_key='companyatlas_id')
class BaseCompanyAtlasVirtualCompany(VirtualModel):
    """Virtual model for company suggestions from companyatlas."""

    companyatlas_id: models.CharField = models.CharField(
        max_length=500,
        verbose_name=companyatlas_id_config['label'],
        help_text=companyatlas_id_config['description'],
        primary_key=True,
    )

    objects = CompanyAtlasVirtualCompanyManager()

    class Meta:
        managed = False
        abstract = True
        verbose_name = _('Company Suggestion')
        verbose_name_plural = _('Company Suggestions')

    def __str__(self) -> str:
        denomination = getattr(self, 'denomination', None)
        companyatlas_id = getattr(self, 'companyatlas_id', None)
        if denomination:
            return str(denomination)
        return f"Company {companyatlas_id or 'unknown'}"


class CompanyAtlasVirtualCompany(BaseCompanyAtlasVirtualCompany):
    """Model for companyatlas companies."""

    class Meta:
        managed = False
        verbose_name = _('CompanyAtlas Company')
        verbose_name_plural = _('CompanyAtlas Companies')

