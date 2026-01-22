from django.contrib import admin

from ...models.virtuals.company import CompanyAtlasVirtualCompany


@admin.register(CompanyAtlasVirtualCompany)
class CompanyAtlasVirtualCompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    readonly_fields = ["name", "description"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

