from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.data import CompanyAtlasData
from ..models.source import COMPANYATLAS_FIELDS_SOURCE


@admin.register(CompanyAtlasData)
class CompanyAtlasDataAdmin(AdminBoostModel):
    list_display = ["company", "data_type", "value", "created_at"]
    list_filter = ["data_type", "created_at"]
    search_fields = ["company__denomination", "data_type", "value"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["company"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, ('company', 'data_type', 'value_type', 'value', ))
        self.add_to_fieldset(_("Source"), COMPANYATLAS_FIELDS_SOURCE)


class CompanyAtlasDataInline(admin.TabularInline):
    model = CompanyAtlasData
    extra = 1
    fields = ["data_type", "value_type", "value", "source", "country_code"]
