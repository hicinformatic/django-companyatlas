from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel, admin_boost_view

from ..models.company import COMPANYATLAS_FIELDS_COMPANY, CompanyAtlasCompany
from ..models.source import COMPANYATLAS_FIELDS_SOURCE
from .address import CompanyAtlasAddressInline
from .data import CompanyAtlasDataInline


@admin.register(CompanyAtlasCompany)
class CompanyAtlasCompanyAdmin(AdminBoostModel):
    list_display = ["denomination", "code", "headquarters_address_display", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["denomination", "code", "to_companyatlasdata__value"]
    readonly_fields = ["named_id", "created_at", "updated_at"]
    inlines = [CompanyAtlasDataInline, CompanyAtlasAddressInline]
    changeform_actions = {
        "refresh_person": _("Refresh Persons"),
        "refresh_address": _("Refresh Addresses"),
        "refresh_data": _("Refresh Data"),
        "refresh_event": _("Refresh Events"),
        "refresh_document": _("Refresh Documents"),
        "full_refresh": _("Full Refresh"),
    }

    def change_fieldsets(self):
        self.add_to_fieldset(None, COMPANYATLAS_FIELDS_COMPANY)
        self.add_to_fieldset(_("Source"), COMPANYATLAS_FIELDS_SOURCE)

    def headquarters_address_display(self, obj: CompanyAtlasCompany) -> str:
        return str(obj.headquarters_address.address) if obj.headquarters_address else "-"
    headquarters_address_display.short_description = _("Headquarters Address")

    def handle_refresh_person(self, request, object_id):
        print("ok")

    @admin_boost_view("message", _("Search Company"))
    def search_company(self, request):
        return redirect("admin:djcompanyatlas_companyatlasvirtualcompany_changelist")
