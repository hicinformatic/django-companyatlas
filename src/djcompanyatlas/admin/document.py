from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.document import CompanyAtlasDocument


class CompanyDocumentInline(admin.TabularInline):
    model = CompanyAtlasDocument
    extra = 1
    fields = ["source", "country_code", "document_type", "title", "date", "url"]


@admin.register(CompanyAtlasDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "source",
        "country_code",
        "document_type",
        "title",
        "date",
        "created_at",
    ]
    list_filter = ["source", "country_code", "document_type", "date", "created_at"]
    search_fields = ["company__name", "title", "document_type", "source"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Document"),
            {
                "fields": (
                    "company",
                    "source",
                    "country_code",
                    "document_type",
                    "title",
                    "date",
                    "url",
                )
            },
        ),
        (_("Content"), {"fields": ("content",)}),
        (
            _("Metadata"),
            {"fields": ("metadata", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

