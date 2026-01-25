from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.company import Company, CompanyData
from ..models.document import CompanyDocument
from ..models.event import CompanyEvent


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["denomination", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["denomination", ]
    readonly_fields = ["created_at", "updated_at"]

