from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ...models.virtuals.provider import ProviderModel


@admin.register(ProviderModel)
class ProviderModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_name",
        "are_packages_installed",
        "are_services_implemented",
        "is_config_ready",
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

