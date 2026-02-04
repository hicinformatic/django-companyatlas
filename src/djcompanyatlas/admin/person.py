from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel
from ..models.person import CompanyAtlasPerson
from ..models.source import COMPANYATLAS_FIELDS_SOURCE
from ..forms.person import CompanyAtlasPersonForm


class CompanyAtlasPersonInline(admin.TabularInline):
    model = CompanyAtlasPerson
    extra = 1
    fields = ["officer_or_owner", "physical_or_moral", "full_name", "created_at"]


@admin.register(CompanyAtlasPerson)
class CompanyAtlasPersonAdmin(AdminBoostModel):
    form = CompanyAtlasPersonForm
    list_display = ["company", "officer_or_owner", "physical_or_moral", "full_name", "created_at"]
    list_filter = ["officer_or_owner", "physical_or_moral", "created_at"]
    search_fields = ["company__denomination", "full_name"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["company"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, [
            "company", 
            "officer_or_owner",
            "physical_or_moral",
            "is_joint_ownership",
        ])
        self.add_to_fieldset(_("Identity"), [
            "denomination",
            "first_name",
            "last_name",
            "birth_date",
        ])
        self.add_to_fieldset(_("Source"), COMPANYATLAS_FIELDS_SOURCE)