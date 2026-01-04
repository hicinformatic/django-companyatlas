from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.company import Company, CompanyData
from ..models.document import CompanyDocument
from ..models.event import CompanyEvent


class CompanyDataInline(admin.TabularInline):
    model = CompanyData
    extra = 1
    fields = ["source", "country_code", "data_type", "value_type", "value"]


class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    extra = 1
    fields = ["source", "country_code", "document_type", "title", "date", "url"]


class CompanyEventInline(admin.TabularInline):
    model = CompanyEvent
    extra = 1
    fields = ["source", "country_code", "event_type", "title", "date"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "description_preview", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [CompanyDataInline, CompanyDocumentInline, CompanyEventInline]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "description")}),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def description_preview(self, obj):
        if obj.description and len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description or "-"

    description_preview.short_description = _("Description")


@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "source",
        "country_code",
        "data_type",
        "value_type",
        "value_preview",
        "created_at",
    ]
    list_filter = ["source", "country_code", "data_type", "value_type", "created_at"]
    search_fields = ["company__name", "value", "data_type", "source"]
    readonly_fields = ["created_at", "updated_at", "value_display"]

    fieldsets = (
        (_("Data"), {"fields": ("company", "source", "country_code", "data_type", "value_type", "value")}),
        (_("Value Preview"), {"fields": ("value_display",), "classes": ("collapse",)}),
        (_("Metadata"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def value_preview(self, obj):
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value

    value_preview.short_description = _("Value")

    def value_display(self, obj):
        if obj:
            converted = obj.get_value()
            return f"Type: {obj.value_type}, Value: {converted} (type: {type(converted).__name__})"
        return "-"

    value_display.short_description = _("Converted Value")

