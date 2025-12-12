"""Virtual model for backend search results."""

from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from virtualqueryset.queryset.base import InMemoryQuerySet
except ImportError:
    try:
        from virtualqueryset import InMemoryQuerySet
    except ImportError:
        InMemoryQuerySet = None

if InMemoryQuerySet is None:
    from ..models.backend import SimpleInMemoryQuerySet as InMemoryQuerySet


class BackendSearchResultQuerySet(InMemoryQuerySet):
    """In-memory queryset for backend search results."""

    pass


class BackendSearchResultManager(models.Manager):
    """Manager for BackendSearchResult."""

    def get_queryset(self):
        return BackendSearchResultQuerySet(model=self.model, data=[])


class BackendSearchResult(models.Model):
    """Virtual model for displaying backend search results."""

    result_data = models.JSONField(default=dict, blank=True, verbose_name=_("Result Data"))
    backend_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("Backend Name")
    )
    service = models.CharField(
        max_length=50, blank=True, verbose_name=_("Service")
    )

    siren = models.CharField(max_length=20, blank=True, verbose_name=_("SIREN"))
    rna = models.CharField(max_length=20, blank=True, verbose_name=_("RNA"))
    siret = models.CharField(max_length=20, blank=True, verbose_name=_("SIRET"))
    denomination = models.CharField(max_length=500, blank=True, verbose_name=_("Denomination"))
    since = models.CharField(max_length=50, blank=True, verbose_name=_("Since"))
    legalform = models.CharField(max_length=200, blank=True, verbose_name=_("Legal Form"))
    ape = models.CharField(max_length=20, blank=True, verbose_name=_("APE"))
    category = models.CharField(max_length=100, blank=True, verbose_name=_("Category"))
    slice_effective = models.CharField(max_length=100, blank=True, verbose_name=_("Slice Effective"))
    siege = models.CharField(max_length=100, blank=True, verbose_name=_("Siege"))

    objects = BackendSearchResultManager()

    class Meta:
        managed = False
        verbose_name = _("Search Result")
        verbose_name_plural = _("Search Results")
        ordering = ["denomination", "siren"]
        default_permissions = ()

    def __str__(self):
        return self.denomination or f"{self.backend_name} - {self.service}"

