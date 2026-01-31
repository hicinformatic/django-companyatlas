from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.event import CompanyAtlasEvent


class CompanyEventInline(admin.TabularInline):
    model = CompanyAtlasEvent
    extra = 1
    fields = ["source", "country_code", "event_type", "title", "date"]


@admin.register(CompanyAtlasEvent)
class CompanyEventAdmin(admin.ModelAdmin):
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
            {"fields": ("company", "source", "country_code", "event_type", "title", "date")},
        ),
        (_("Description"), {"fields": ("description",)}),
        (
            _("Metadata"),
            {"fields": ("metadata", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

