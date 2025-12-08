"""Django admin configuration."""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Company, CompanyData, CompanyCountryData


class CompanyDataInline(admin.TabularInline):
    """Inline admin for CompanyData."""
    
    model = CompanyData
    extra = 1
    fields = ["country", "data_type", "value_type", "value"]
    list_filter = ["country", "data_type", "value_type"]


class CompanyCountryDataInline(admin.StackedInline):
    """Inline admin for CompanyCountryData."""
    
    model = CompanyCountryData
    extra = 0
    fieldsets = (
        ("French Data", {
            "fields": ("siren", "siret", "rna", "ape", "legal_form", "rcs"),
        }),
        ("Extra Data", {
            "fields": ("extra_data",),
            "classes": ("collapse",),
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""

    list_display = [
        "name",
        "country",
        "domain",
        "industry",
        "employee_count",
        "country_data_summary",
        "enrichment_status",
        "created_at",
    ]
    list_filter = ["is_enriched", "industry", "country", "created_at"]
    search_fields = ["name", "domain", "vat_number", "legal_name"]
    readonly_fields = ["is_enriched", "enriched_at", "created_at", "updated_at"]
    
    inlines = [CompanyCountryDataInline, CompanyDataInline]
    
    fieldsets = (
        ("Identifiers", {
            "fields": ("domain", "vat_number", "stock_symbol"),
        }),
        ("Basic Information", {
            "fields": ("name", "legal_name", "description", "website"),
        }),
        ("Details", {
            "fields": ("founded_year", "employee_count", "industry"),
        }),
        ("Location", {
            "fields": ("country", "city", "address"),
        }),
        ("Enrichment", {
            "fields": ("is_enriched", "enriched_at", "enrichment_data"),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    
    actions = ["enrich_selected"]
    
    def country_data_summary(self, obj):
        """Display summary of country-specific data."""
        country_data = obj.country_data.first()
        if country_data:
            parts = []
            if country_data.siren:
                parts.append(f"SIREN: {country_data.siren}")
            if country_data.rna:
                parts.append(f"RNA: {country_data.rna}")
            if parts:
                return format_html("<br>".join(parts))
        return "-"
    country_data_summary.short_description = "Country Data"
    
    def enrichment_status(self, obj):
        """Display enrichment status with icon."""
        if obj.is_enriched:
            return format_html(
                '<span style="color: green;">✓ Enriched</span>'
            )
        return format_html(
            '<span style="color: gray;">○ Not enriched</span>'
        )
    enrichment_status.short_description = "Status"
    
    def enrich_selected(self, request, queryset):
        """Action to enrich selected companies."""
        count = 0
        for company in queryset:
            if company.enrich(force=True):
                count += 1
        
        self.message_user(
            request,
            f"Successfully enriched {count} of {queryset.count()} companies."
        )
    enrich_selected.short_description = "Enrich selected companies"


@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    """Admin interface for CompanyData model."""
    
    list_display = [
        "company",
        "country",
        "data_type",
        "value_type",
        "value_preview",
        "created_at",
    ]
    list_filter = ["country", "data_type", "value_type", "created_at"]
    search_fields = ["company__name", "value", "data_type"]
    readonly_fields = ["created_at", "updated_at", "value_display"]
    
    fieldsets = (
        ("Data", {
            "fields": ("company", "country", "data_type", "value_type", "value"),
        }),
        ("Value Preview", {
            "fields": ("value_display",),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
    
    def value_preview(self, obj):
        """Display truncated value."""
        if len(obj.value) > 50:
            return f"{obj.value[:50]}..."
        return obj.value
    value_preview.short_description = "Value"
    
    def value_display(self, obj):
        """Display the value converted to its proper type."""
        if obj:
            converted = obj.get_value()
            return f"Type: {obj.value_type}, Value: {converted} (type: {type(converted).__name__})"
        return "-"
    value_display.short_description = "Converted Value"


@admin.register(CompanyCountryData)
class CompanyCountryDataAdmin(admin.ModelAdmin):
    """Admin interface for CompanyCountryData model."""
    
    list_display = [
        "company",
        "country",
        "siren",
        "siret",
        "rna",
        "legal_form",
        "created_at",
    ]
    list_filter = ["country", "legal_form", "created_at"]
    search_fields = ["company__name", "siren", "siret", "rna"]
    readonly_fields = ["created_at", "updated_at"]
    
    fieldsets = (
        ("Company", {
            "fields": ("company", "country"),
        }),
        ("French Data", {
            "fields": ("siren", "siret", "rna", "ape", "legal_form", "rcs"),
        }),
        ("Extra Data", {
            "fields": ("extra_data",),
            "classes": ("collapse",),
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
