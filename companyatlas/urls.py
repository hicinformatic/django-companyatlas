"""URL configuration for companyatlas app."""

from django.urls import path

from . import views

app_name = "companyatlas"

urlpatterns = [
    path("", views.company_list, name="company-list"),
    path("<int:pk>/", views.company_detail, name="company-detail"),
    path("<int:pk>/enrich/", views.company_enrich, name="company-enrich"),
]
