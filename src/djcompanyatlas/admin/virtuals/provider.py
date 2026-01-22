"""Admin for provider model."""

from django.contrib import admin
from djproviderkit.admin.provider import BaseProviderAdmin

from ...models.virtuals.provider import CompanyAtlasProviderModel


@admin.register(CompanyAtlasProviderModel)
class CompanyAtlasProviderModelAdmin(BaseProviderAdmin):
    """Admin for companyatlas providers."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display.insert(1, 'geo_data')
        return list_display

    def change_fieldsets(self):
        super().change_fieldsets()
        self.add_to_fieldset(None, ['geo_data'])

__all__ = ["CompanyAtlasProviderModelAdmin"]