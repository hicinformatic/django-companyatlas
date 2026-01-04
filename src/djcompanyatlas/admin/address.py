from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.address import CompanyAtlasAddress


class CompanyAtlasAddressInline(admin.TabularInline):
    model = CompanyAtlasAddress
    extra = 1
    fields = ["source", "country_code", "address", "is_headquarters"]


@admin.register(CompanyAtlasAddress)
class CompanyAtlasAddressAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "source",
        "country_code",
        "address",
        "is_headquarters",
        "created_at",
    ]
    list_filter = ["source", "country_code", "is_headquarters", "created_at"]
    search_fields = ["company__name", "address"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (_("Address"), {"fields": ("company", "source", "country_code", "address", "is_headquarters")}),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

