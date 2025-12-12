"""Virtual backend model for admin display (not persisted)."""

from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from virtualqueryset.queryset.base import InMemoryQuerySet  # type: ignore[import-not-found]
except ImportError:
    try:
        from virtualqueryset import InMemoryQuerySet  # type: ignore[import-not-found]
    except ImportError:
        # Fallback if virtualqueryset is not installed
        InMemoryQuerySet = None


class SimpleInMemoryQuerySet:
    """Simple in-memory QuerySet implementation when virtualqueryset is not available."""

    def __init__(self, model, data=None):
        self.model = model
        self._data = list(data) if data is not None else []
        self._result_cache = None
        self._ordering = []

    def __iter__(self):
        if self._result_cache is None:
            self._result_cache = list(self._data)
            if self._ordering:
                self._apply_ordering()
        return iter(self._result_cache)

    def __getitem__(self, k):
        if self._result_cache is None:
            self._result_cache = list(self._data)
            if self._ordering:
                self._apply_ordering()
        return self._result_cache[k]

    def __len__(self):
        if self._result_cache is None:
            self._result_cache = list(self._data)
            if self._ordering:
                self._apply_ordering()
        return len(self._result_cache)

    def _apply_ordering(self):
        """Apply ordering to result cache."""
        if not self._ordering:
            return
        
        def get_sort_key(obj):
            keys = []
            for field in self._ordering:
                reverse = field.startswith('-')
                field_name = field.lstrip('-')
                value = getattr(obj, field_name, None)
                if value is None:
                    value = ""
                if isinstance(value, str):
                    value = value.lower()
                keys.append(value)
            return tuple(keys)
        
        # Sort with multiple passes for each field
        for field in reversed(self._ordering):
            reverse = field.startswith('-')
            field_name = field.lstrip('-')
            
            def get_field_value(obj):
                value = getattr(obj, field_name, None)
                if value is None:
                    value = ""
                if isinstance(value, str):
                    value = value.lower()
                return value
            
            self._result_cache.sort(key=get_field_value, reverse=reverse)

    def count(self):
        return len(self._data)

    def all(self):
        return self

    def none(self):
        qs = SimpleInMemoryQuerySet(self.model, [])
        qs._ordering = self._ordering
        return qs

    def order_by(self, *field_names):
        """Order the queryset by the given fields."""
        qs = SimpleInMemoryQuerySet(self.model, self._data)
        qs._ordering = list(field_names)
        return qs

    def filter(self, **kwargs):
        filtered = []
        for obj in self._data:
            match = True
            for key, value in kwargs.items():
                if not hasattr(obj, key) or getattr(obj, key) != value:
                    match = False
                    break
            if match:
                filtered.append(obj)
        qs = SimpleInMemoryQuerySet(self.model, filtered)
        qs._ordering = self._ordering
        return qs

    def exclude(self, **kwargs):
        filtered = []
        for obj in self._data:
            match = False
            for key, value in kwargs.items():
                if hasattr(obj, key) and getattr(obj, key) == value:
                    match = True
                    break
            if not match:
                filtered.append(obj)
        qs = SimpleInMemoryQuerySet(self.model, filtered)
        qs._ordering = self._ordering
        return qs

    def exists(self):
        """Check if queryset has any results."""
        return len(self._data) > 0

    def first(self):
        """Return the first object or None."""
        if self._data:
            if self._result_cache is None:
                self._result_cache = list(self._data)
                if self._ordering:
                    self._apply_ordering()
            return self._result_cache[0] if self._result_cache else None
        return None

    def get(self, **kwargs):
        """Get a single object matching the given criteria."""
        filtered = self.filter(**kwargs)
        if len(filtered) == 0:
            raise self.model.DoesNotExist(f"{self.model.__name__} matching query does not exist.")
        if len(filtered) > 1:
            raise self.model.MultipleObjectsReturned(
                f"get() returned more than one {self.model.__name__} -- it returned {len(filtered)}!"
            )
        return filtered.first()


class BackendInfoQuerySet(  # type: ignore[misc]
    InMemoryQuerySet if InMemoryQuerySet else SimpleInMemoryQuerySet
):
    """In-memory QuerySet for backend info."""

    pass


class BackendInfoManager(models.Manager):
    """Custom manager that returns our in-memory QuerySet"""

    def get_queryset(self):
        # Load backends from python-companyatlas helpers
        # Use lazy loading to avoid AppRegistryNotReady errors
        try:
            from django.apps import apps

            # Ensure Django apps are ready
            apps.check_apps_ready()
        except Exception:
            # If apps aren't ready, return empty queryset
            return BackendInfoQuerySet(model=self.model, data=[])

        try:
            # Get configuration from Django settings (only after apps are ready)
            from django.conf import settings
            from python_companyatlas.backends import get_backends

            config = getattr(settings, "COMPANYATLAS", {})
            statuses = get_backends(config=config)

            # Build backend list
            backends_list = []
            for status in statuses:
                try:
                    backend = BackendInfo(
                        pk=status.get("name", "unknown"),  # Use name as pk
                        name=status.get("name", "unknown"),
                        display_name=status.get("display_name", ""),
                        continent=status.get("continent", ""),
                        country_code=status.get("country_code", ""),
                        status=status.get("status", "unknown"),
                        is_available=status.get("is_available", False),
                        documentation_url=status.get("documentation_url") or None,
                        site_url=status.get("site_url") or None,
                        status_url=status.get("status_url") or None,
                    )
                    # Store diagnostic data and lists as attributes (not model fields)
                    backend._diagnostic = status
                    backend._missing_packages = status.get("missing_packages", [])
                    backend._missing_config = status.get("missing_config", [])
                    backend._country_flag = status.get("country_flag", "")
                    backend._country_flag_image = status.get("country_flag_image", "")
                    backend._can_fetch_documents = status.get("can_fetch_documents", False)
                    backend._can_fetch_events = status.get("can_fetch_events", False)
                    backend._can_fetch_company_data = status.get("can_fetch_company_data", True)
                    backend._request_cost = status.get("request_cost", {"data": "free", "documents": "free", "events": "free"})
                    backends_list.append(backend)
                except Exception as e:
                    # Log error for individual backend but continue
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(
                        f"Error creating BackendInfo for {status.get('name')}: {e}"
                    )

            # Return an in-memory QuerySet
            return BackendInfoQuerySet(model=self.model, data=backends_list)

        except Exception as e:
            # Log error for debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error loading backends: {e}", exc_info=True)
            # Return empty queryset on error
            return BackendInfoQuerySet(model=self.model, data=[])


class BackendInfo(models.Model):
    """
    Virtual model (not persisted) representing a configured backend.
    Data comes from python-companyatlas, not from the database.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("Backend Name"),
    )
    display_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Display Name"),
    )
    continent = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Continent"),
    )
    country_code = models.CharField(
        max_length=2,
        blank=True,
        verbose_name=_("Country Code"),
    )
    status = models.CharField(
        max_length=50,
        verbose_name=_("Status"),
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name=_("Is Available"),
    )
    documentation_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Documentation URL"),
    )
    site_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Site URL"),
    )
    status_url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("Status URL"),
    )

    class Meta:
        managed = False  # No database table
        verbose_name = _("Backend")
        verbose_name_plural = _("Backends")
        default_permissions = ()  # No add/change/delete permissions
        ordering = ["continent", "country_code", "name"]

    # Assign manager after class definition to avoid AppRegistryNotReady
    objects = BackendInfoManager()

    def __str__(self):
        return self.display_name or self.name

    # Internal helpers -------------------------------------------------
    @property
    def diagnostic(self) -> dict:
        """Get full diagnostic information."""
        diag = getattr(self, "_diagnostic", None)
        if isinstance(diag, dict):
            return diag
        return {}

    @property
    def packages(self) -> dict:
        """Get package installation status."""
        value = self.diagnostic.get("packages", {}) or {}
        return value if isinstance(value, dict) else {}

    @property
    def required_packages(self):
        """Get list of required packages."""
        return list(self.packages.keys())

    @property
    def missing_packages(self):
        """Get list of missing packages."""
        return getattr(self, "_missing_packages", [])

    @property
    def missing_config(self):
        """Get list of missing config keys."""
        return getattr(self, "_missing_config", [])

    @property
    def country_flag(self):
        """Get country flag emoji."""
        return getattr(self, "_country_flag", "")

    @property
    def country_flag_image(self):
        """Get country flag as base64-encoded image."""
        return getattr(self, "_country_flag_image", "")

    @property
    def config_entries(self) -> list:
        """Get configuration entries."""
        config = self.diagnostic.get("config", {}) or {}
        if not isinstance(config, dict):
            return []
        return [(key, details) for key, details in config.items()]

    @property
    def description_text(self):
        """Get backend description."""
        return self.diagnostic.get("description_text")

    @property
    def error(self):
        """Get error message if any."""
        return self.diagnostic.get("error")

    @property
    def status_display(self):
        """Get human-readable status."""
        labels = {
            "available": _("✅ Available"),
            "missing_packages": _("❌ Missing Packages"),
            "missing_config": _("⚠️ Missing Config"),
            "unavailable": _("❌ Unavailable"),
        }
        return labels.get(self.status, _("❓ Unknown"))

    @property
    def can_fetch_documents(self):
        """Get can_fetch_documents capability."""
        return getattr(self, "_can_fetch_documents", False)

    @property
    def can_fetch_events(self):
        """Get can_fetch_events capability."""
        return getattr(self, "_can_fetch_events", False)

    @property
    def can_fetch_company_data(self):
        """Get can_fetch_company_data capability."""
        return getattr(self, "_can_fetch_company_data", True)
