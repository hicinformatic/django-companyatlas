from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.address import CompanyAtlasAddress
from ..models.source import COMPANYATLAS_FIELDS_SOURCE


class CompanyAtlasAddressInline(admin.TabularInline):
    model = CompanyAtlasAddress
    extra = 1
    fields = ["address", "is_headquarters", "source", "country_code", ]


@admin.register(CompanyAtlasAddress)
class CompanyAtlasAddressAdmin(AdminBoostModel):
    list_display = [
        "company",
        "source",
        "country_code",
        "address_display",
        "is_headquarters",
        "created_at",
    ]
    list_filter = ["source", "country_code", "is_headquarters", "created_at"]
    search_fields = ["company__denomination", "company__to_companyatlasdata__value"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["company"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, ("company", "address", "is_headquarters"))
        self.add_to_fieldset(_("source"), COMPANYATLAS_FIELDS_SOURCE)

    def address_display(self, obj: CompanyAtlasAddress) -> str:
        return str(obj.address) if obj.address else "-"
    address_display.short_description = _("Address")
