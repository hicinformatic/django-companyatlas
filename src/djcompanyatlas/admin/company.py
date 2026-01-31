from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel, admin_boost_view
from django.shortcuts import redirect
from ..models.company import (
    CompanyAtlasCompany, CompanyAtlasData, COMPANYATLAS_FIELDS_COMPANY
)
from ..models.source import COMPANYATLAS_FIELDS_SOURCE

@admin.register(CompanyAtlasData)
class CompanyAtlasDataAdmin(AdminBoostModel):
    list_display = ["company", "data_type", "value", "created_at"]
    list_filter = ["data_type", "created_at"]
    search_fields = ["company__name", "data_type", "value"]
    readonly_fields = ["created_at", "updated_at"]

@admin.register(CompanyAtlasCompany)
class CompanyAtlasCompanyAdmin(AdminBoostModel):
    list_display = ["denomination", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["denomination", ]
    readonly_fields = ["named_id", "created_at", "updated_at"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, COMPANYATLAS_FIELDS_COMPANY)
        self.add_to_fieldset(_("Source"), COMPANYATLAS_FIELDS_SOURCE)

    @admin_boost_view("message", _("Search Company"))
    def search_company(self, request):
        return redirect("admin:djcompanyatlas_companyatlasvirtualcompany_changelist")