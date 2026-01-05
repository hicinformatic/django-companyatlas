from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ...models.virtuals.provider import ProviderModel


@admin.register(ProviderModel)
class ProviderModelAdmin(admin.ModelAdmin):
    list_display = [
        "display_name",
        "are_packages_installed",
        "are_services_implemented",
        "is_config_ready",
        "has_search_company",
        "cost_search_company",
        "has_search_company_by_code",
        "cost_search_company_by_code",
        "has_get_company_documents",
        "cost_get_company_documents",
        "has_get_company_events",
        "cost_get_company_events",
    ]
    list_filter = [
        "are_packages_installed",
        "are_services_implemented",
        "is_config_ready",
    ]
    search_fields = ["name", "display_name", "description"]
    readonly_fields = [
        "name",
        "display_name",
        "description",
        "required_packages",
        "status_url",
        "documentation_url",
        "site_url",
        "config_keys",
        "config_required",
        "config_prefix",
        "services",
        "are_packages_installed",
        "are_services_implemented",
        "is_config_ready",
        "missing_packages",
        "missing_config_keys",
        "missing_services",
    ]

    fieldsets = (
        (_("Basic Information"), {"fields": ("name", "display_name", "description")}),
        (_("URLs"), {"fields": ("status_url", "documentation_url", "site_url")}),
        (_("Configuration"), {"fields": ("config_keys", "config_required", "config_prefix")}),
        (_("Services"), {"fields": ("services",)}),
        (_("Status"), {"fields": ("are_packages_installed", "are_services_implemented", "is_config_ready")}),
        (_("Missing"), {"fields": ("missing_packages", "missing_config_keys", "missing_services")}),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_search_company(self, obj):
        if not obj or not obj.services:
            return False
        if "search_company" not in obj.services:
            return False
        missing = obj.missing_services or []
        return "search_company" not in missing

    has_search_company.short_description = _("Search company")
    has_search_company.boolean = True

    def has_search_company_by_code(self, obj):
        if not obj or not obj.services:
            return False
        if "search_company_by_code" not in obj.services:
            return False
        missing = obj.missing_services or []
        return "search_company_by_code" not in missing

    has_search_company_by_code.short_description = _("Search by code")
    has_search_company_by_code.boolean = True

    def has_get_company_documents(self, obj):
        if not obj or not obj.services:
            return False
        if "get_company_documents" not in obj.services:
            return False
        missing = obj.missing_services or []
        return "get_company_documents" not in missing

    has_get_company_documents.short_description = _("Get documents")
    has_get_company_documents.boolean = True

    def has_get_company_events(self, obj):
        if not obj or not obj.services:
            return False
        if "get_company_events" not in obj.services:
            return False
        missing = obj.missing_services or []
        return "get_company_events" not in missing

    has_get_company_events.short_description = _("Get events")
    has_get_company_events.boolean = True

    def cost_search_company(self, obj: ProviderModel | None) -> str:
        if not obj:
            return "-"
        cost = getattr(obj, "cost_search_company", None)
        if cost is None or cost == 0 or cost == "free":
            return "-"
        return f"${cost:.5f}"

    cost_search_company.short_description = _("Cost (search)")

    def cost_search_company_by_code(self, obj: ProviderModel | None) -> str:
        if not obj:
            return "-"
        cost = getattr(obj, "cost_search_company_by_code", None)
        if cost is None or cost == 0 or cost == "free":
            return "-"
        return f"${cost:.5f}"

    cost_search_company_by_code.short_description = _("Cost (code)")

    def cost_get_company_documents(self, obj: ProviderModel | None) -> str:
        if not obj:
            return "-"
        cost = getattr(obj, "cost_get_company_documents", None)
        if cost is None or cost == 0 or cost == "free":
            return "-"
        return f"${cost:.5f}"

    cost_get_company_documents.short_description = _("Cost (documents)")

    def cost_get_company_events(self, obj: ProviderModel | None) -> str:
        if not obj:
            return "-"
        cost = getattr(obj, "cost_get_company_events", None)
        if cost is None or cost == 0 or cost == "free":
            return "-"
        return f"${cost:.5f}"

    cost_get_company_events.short_description = _("Cost (events)")

