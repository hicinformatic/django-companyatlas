from django.db import models
from django.db.models import F, Subquery

from ..models.referentiel import CompanyAtlasReferentiel


class CompanyAtlasDataManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs.annotate(
            sql_referentiel_description=Subquery(
                CompanyAtlasReferentiel.objects.filter(
                    code=F("referentiel"),
                ).values("description"),
            ),
        )
        return qs
