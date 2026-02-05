from django.db import models
from django.db.models import Count


class CompanyAtlasReferentielManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs.annotate(
            sql_used_count=Count('to_companyatlasdata'),
        )
        return qs