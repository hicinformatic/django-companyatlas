from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.referentiel import CompanyAtlasReferentiel
from ..models.source import COMPANYATLAS_FIELDS_SOURCE

base_fields = [
    "category",
    "usage_type",
    "code",
    "description",
    "characteristics",
    "priority",
    "used_count",
]

@admin.register(CompanyAtlasReferentiel)
class CompanyAtlasReferentielAdmin(AdminBoostModel):
    list_display = base_fields
    list_filter = ["category", "usage_type"]
    search_fields = ["category", "code", "description", "characteristics"]
    readonly_fields = ["created_at", "updated_at", "used_count"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, base_fields)
        self.add_to_fieldset(_("Source"), COMPANYATLAS_FIELDS_SOURCE)
