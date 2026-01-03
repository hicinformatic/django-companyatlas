"""Django admin configuration."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Company, CompanyData, CompanyDocument, CompanyEvent

# BackendInfoAdmin is registered in apps.py ready() method to avoid AppRegistryNotReady


class CompanyDataInline(admin.TabularInline):
    """Inline admin for CompanyData."""

    model = CompanyData
    extra = 1
    fields = ["source", "country_code", "data_type", "value_type", "value"]


class CompanyDocumentInline(admin.TabularInline):
    """Inline admin for CompanyDocument."""

    model = CompanyDocument
    extra = 1
    fields = ["source", "country_code", "document_type", "title", "date", "url"]


class CompanyEventInline(admin.TabularInline):
    """Inline admin for CompanyEvent."""

    model = CompanyEvent
    extra = 1
    fields = ["source", "country_code", "event_type", "title", "date"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""

    list_display = [
        "name",
        "description_preview",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]

    inlines = [CompanyDataInline, CompanyDocumentInline, CompanyEventInline]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("name", "description"),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def description_preview(self, obj):
        """Display truncated description."""
        if obj.description and len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description or "-"

    description_preview.short_description = _("Description")


@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    """Admin interface for CompanyData model."""

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
        (
            _("Data"),
            {
                "fields": ("company", "source", "country_code", "data_type", "value_type", "value"),
            },
        ),
        (
            _("Value Preview"),
            {
                "fields": ("value_display",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def value_preview(self, obj):
        """Display truncated value."""
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value

    value_preview.short_description = _("Value")

    def value_display(self, obj):
        """Display the value converted to its proper type."""
        if obj:
            converted = obj.get_value()
            return f"Type: {obj.value_type}, Value: {converted} (type: {type(converted).__name__})"
        return "-"

    value_display.short_description = _("Converted Value")


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    """Admin interface for CompanyDocument model."""

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
                "fields": ("company", "source", "country_code", "document_type", "title", "date", "url"),
            },
        ),
        (
            _("Content"),
            {
                "fields": ("content",),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("metadata", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(CompanyEvent)
class CompanyEventAdmin(admin.ModelAdmin):
    """Admin interface for CompanyEvent model."""

    list_display = [
        "company",
        "source",
        "country_code",
        "event_type",
        "title",
        "date",
        "created_at",
    ]
    list_filter = ["source", "country_code", "event_type", "date", "created_at"]
    search_fields = ["company__name", "title", "event_type", "source"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Event"),
            {
                "fields": ("company", "source", "country_code", "event_type", "title", "date"),
            },
        ),
        (
            _("Description"),
            {
                "fields": ("description",),
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ("metadata", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
