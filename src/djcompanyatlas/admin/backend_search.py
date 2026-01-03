"""Admin for backend search results."""

import json

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..models.backend import BackendInfo
from ..models.backend_search import BackendSearchResult, BackendSearchResultQuerySet


def get_backend_instance(backend_name: str):
    """Get backend instance from python-companyatlas."""
    try:
        from django.conf import settings
        from python_companyatlas.backends import get_all_backend_classes

        config = getattr(settings, "COMPANYATLAS", {})
        backend_classes = get_all_backend_classes()

        for backend_class in backend_classes:
            if backend_class.name == backend_name:
                return backend_class(config=config)

        return None
    except Exception:
        return None


@admin.register(BackendSearchResult)
class BackendSearchResultAdmin(admin.ModelAdmin):
    """Admin for displaying backend search results using change_list template."""

    list_display = [
        "denomination",
        "siren",
        "siret",
        "rna",
        "legalform",
        "ape",
        "since",
        "category",
        "slice_effective",
        "siege",
    ]
    list_per_page = 20
    search_fields = ["denomination", "siren", "siret", "rna"]
    readonly_fields = ["result_data_display", "backend_name", "service"]
    list_filter = []
    change_list_template = "admin/djcompanyatlas/backendsearchresult/change_list.html"
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist to add backend context."""
        extra_context = extra_context or {}
        backend_name = request.GET.get("backend", "").strip()
        service = request.GET.get("service", "data").strip()
        
        if backend_name:
            try:
                backend_obj = BackendInfo.objects.get(pk=backend_name)
                extra_context["backend"] = backend_obj
                extra_context["current_service"] = service
            except BackendInfo.DoesNotExist:
                pass
        
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        """Build VirtualQuerySet from search parameters."""
        import logging
        
        logger = logging.getLogger(__name__)
        query = (request.GET.get("q") or "").strip()
        backend_name = (request.GET.get("backend") or "").strip()
        service = (request.GET.get("service") or "data").strip()

        logger.debug(f"get_queryset called with query='{query}', backend='{backend_name}', service='{service}'")

        if not query or not backend_name:
            logger.debug("Missing query or backend_name, returning empty queryset")
            return BackendSearchResultQuerySet(model=BackendSearchResult, data=[])

        try:
            backend_obj = BackendInfo.objects.get(pk=backend_name)
        except BackendInfo.DoesNotExist:
            logger.warning(f"BackendInfo not found: {backend_name}")
            return BackendSearchResultQuerySet(model=BackendSearchResult, data=[])

        backend_instance = get_backend_instance(backend_name)
        if not backend_instance:
            logger.warning(f"Backend instance not found: {backend_name}")
            return BackendSearchResultQuerySet(model=BackendSearchResult, data=[])

        raw_results = []
        try:
            if service == "data":
                if backend_obj.can_fetch_company_data:
                    logger.debug(f"Calling search_by_name with query='{query}'")
                    raw_results = backend_instance.search_by_name(query, limit=20, raw=False)
                    logger.debug(f"search_by_name returned {len(raw_results)} results")

            elif service == "documents":
                if backend_obj.can_fetch_documents:
                    raw_results = backend_instance.get_documents(query, limit=20)

            elif service == "events":
                if backend_obj.can_fetch_events:
                    raw_results = backend_instance.get_events(query, limit=20)

        except Exception as e:
            logger.exception(f"Error in BackendSearchResultAdmin.get_queryset: {e}")

        data = []
        logger.debug(f"Processing {len(raw_results)} raw results")
        for idx, result in enumerate(raw_results):
            if not isinstance(result, dict):
                result = {"data": result}
            
            normalized = result
            from python_companyatlas.backends.europe.france.base import FrenchBaseBackend
            if isinstance(backend_instance, FrenchBaseBackend) and service == "data":
                standard_fields = ["siren", "rna", "siret", "denomination", "since", "legalform", "ape", "category", "slice_effective", "siege"]
                is_already_normalized = all(field in result for field in standard_fields)
                if not is_already_normalized:
                    normalized_list = backend_instance.normalize_results([result])
                    if normalized_list:
                        normalized = normalized_list[0]
            
            def safe_str(value):
                if value is None:
                    return ""
                return str(value)
            
            obj = BackendSearchResult(
                pk=f"{backend_name}-{service}-{idx}",
                result_data=result,
                backend_name=backend_name,
                service=service,
                siren=safe_str(normalized.get("siren")),
                rna=safe_str(normalized.get("rna")),
                siret=safe_str(normalized.get("siret")),
                denomination=safe_str(normalized.get("denomination")),
                since=safe_str(normalized.get("since")),
                legalform=safe_str(normalized.get("legalform")),
                ape=safe_str(normalized.get("ape")),
                category=safe_str(normalized.get("category")),
                slice_effective=safe_str(normalized.get("slice_effective")),
                siege=safe_str(normalized.get("siege")),
            )
            data.append(obj)

        logger.debug(f"Created {len(data)} BackendSearchResult objects")
        return BackendSearchResultQuerySet(model=BackendSearchResult, data=data)

    @admin.display(description=_("Result Data"))
    def result_data_display(self, obj):
        """Display result data in detail view."""
        if not obj:
            return "-"
        try:
            formatted = json.dumps(obj.result_data, indent=2, ensure_ascii=False)
            return format_html(
                '<pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; '
                'overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; '
                'max-width: 100%;">{}</pre>',
                mark_safe(formatted),
            )
        except (TypeError, ValueError):
            return format_html(
                '<pre style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; '
                'overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; '
                'max-width: 100%;">{}</pre>',
                str(obj.result_data),
            )

