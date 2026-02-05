from django.db import models


class CompanyAtlasCompanyManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs.prefetch_related("to_companyatlasdata", "to_companyatlasaddress")
        return qs
