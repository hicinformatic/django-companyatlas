from django.contrib import admin

from ...models.virtuals.document import CompanyAtlasVirtualDocument


@admin.register(CompanyAtlasVirtualDocument)
class CompanyAtlasVirtualDocumentAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    readonly_fields = []

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

