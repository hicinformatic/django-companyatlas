from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel, admin_boost_view
from ...models.virtuals.company import CompanyAtlasVirtualCompany
from ...models.virtuals.provider import CompanyAtlasProviderModel
from ...forms.virtuals.company import CompanyAtlasVirtualCompanyCreateForm
from djproviderkit.admin.service import FirstServiceAdminFilter, BackendServiceAdminFilter
BackendServiceAdminFilter.provider_model = CompanyAtlasProviderModel

@admin.register(CompanyAtlasVirtualCompany)
class CompanyAtlasVirtualCompanyAdmin(AdminBoostModel):
    list_display = ["denomination", "reference", "address", "backend_name_display"]
    search_fields = ["denomination",]
    list_filter = [FirstServiceAdminFilter, BackendServiceAdminFilter]
    fieldsets = [
        (None, {'fields': ("denomination", "reference", "source_field", "address")}),
    ]
    changeform_actions = {
        "create_company": _("Create Company"),
    }

    def change_fieldsets(self):
        self.add_to_fieldset(_('Backend'), ('backend',  'backend_name_display', 'companyatlas_id'))
        self.add_to_fieldset('data', ('country', 'data_source',))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        query = request.GET.get("q")
        if query:
            kwargs = {"first": bool(request.GET.get("first"))}
            if request.GET.get("bck"):
                kwargs["attribute_search"] = {"name": request.GET.get("bck")}
            return self.model.objects.search_company(query=query, **kwargs)
        return self.model.objects.none()

    def get_object(self, request, object_id, from_field=None):
        object_id = unquote(object_id)
        return self.model.objects.search_company_by_reference(code=object_id).first()

    def backend_name_display(self, obj: CompanyAtlasVirtualCompany | None) -> str:
        if not obj or not obj.backend or not obj.backend_name:
            return "-"
        url = reverse("admin:djcompanyatlas_companyatlasprovidermodel_change", args=[obj.backend])
        return format_html('<a href="{}">{}</a>', url, obj.backend_name)
    backend_name_display.short_description = _("Backend name")

    def company_model_exist(self, obj: CompanyAtlasVirtualCompany | None) -> bool:
        from djcompanyatlas.models.company import CompanyAtlasCompany
        return CompanyAtlasCompany.objects.filter(denomination=obj.denomination).exists()

    def handle_create_company(self, request, object_id):
        object_id = unquote(object_id)
        obj = self.get_object(request, object_id)

    @admin_boost_view("adminform", "Create Company")
    def create_company_view(self, request, obj):
        if request.method == "POST":
            form = CompanyAtlasVirtualCompanyCreateForm(request.POST, instance=obj)
            if form.is_valid():
                company = form.save()
        else:
            form = CompanyAtlasVirtualCompanyCreateForm(instance=obj)
        return { "form": form, "has_change_permission": True }
