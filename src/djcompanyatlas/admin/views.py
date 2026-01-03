"""Admin views for testing backends."""

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models.backend import BackendInfo


def backend_search_view(request, name: str, service: str):
    """Display search results using native change_list template.

    Args:
        request: Django request object
        name: Backend name
        service: Service type (data, documents, events)
    """
    if not request.user.is_staff:
        raise Http404

    if service not in ["data", "documents", "events"]:
        raise Http404

    try:
        backend_obj = BackendInfo.objects.get(pk=name)
    except BackendInfo.DoesNotExist:
        raise Http404

    if service == "data" and not backend_obj.can_fetch_company_data:
        raise Http404
    elif service == "documents" and not backend_obj.can_fetch_documents:
        raise Http404
    elif service == "events" and not backend_obj.can_fetch_events:
        raise Http404

    from django.contrib import admin
    from ..admin.backend_search import BackendSearchResultAdmin
    from ..models.backend_search import BackendSearchResult

    admin_instance = BackendSearchResultAdmin(BackendSearchResult, admin.site)
    
    request.GET = request.GET.copy()
    request.GET["backend"] = name
    request.GET["service"] = service

    return admin_instance.changelist_view(request)

