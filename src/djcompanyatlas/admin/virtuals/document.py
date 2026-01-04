from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ...models.virtuals.document import CompanyAtlasVirtualCompany


@admin.register(CompanyAtlasVirtualCompany)
class CompanyAtlasVirtualDocumentAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    readonly_fields = []

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

