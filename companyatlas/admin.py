"""Django admin configuration."""

from django.contrib import admin
from django.utils.html import format_html
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin interface for Company model."""

    list_display = [
        "name",
        "domain",
        "industry",
        "employee_count",
        "enrichment_status",
        "created_at",
    ]
    list_filter = ["is_enriched", "industry", "country", "created_at"]
    search_fields = ["name", "domain", "siren", "vat_number", "legal_name"]
    readonly_fields = ["is_enriched", "enriched_at", "created_at", "updated_at"]
    
    fieldsets = (
        ("Identifiers", {
            "fields": ("domain", "siren", "vat_number", "stock_symbol"),
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

