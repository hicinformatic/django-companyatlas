"""Admin modules for companyatlas."""

from django.contrib import admin
from django.urls import path

from .backend import BackendInfoAdmin
from .views import backend_search_view

__all__ = ["BackendInfoAdmin"]


def get_admin_urls():
    """Get custom admin URLs for backend testing."""
    from .views import backend_search_view
    
    return [
        path(
            "djcompanyatlas/backendinfo/<str:name>/search/<str:service>/",
            admin.site.admin_view(backend_search_view),
            name="djcompanyatlas_backendinfo_search",
        ),
    ]

