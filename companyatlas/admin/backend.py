"""Administration du modèle virtuel BackendInfo."""

import importlib

from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..models.backend import BackendInfoQuerySet


class ContinentFilter(admin.SimpleListFilter):
    """Filter backends by continent."""

    title = _("Continent")
    parameter_name = "continent"

    def lookups(self, request, model_admin):
        """Return list of continent choices."""
        try:
            from django.apps import apps

            apps.check_apps_ready()

            from django.conf import settings
            from python_companyatlas.backends import get_backends

            config = getattr(settings, "COMPANYATLAS", {})
            statuses = get_backends(config=config)
            continents = sorted(set(s.get("continent") for s in statuses if s.get("continent")))
            return [(c, c.title()) for c in continents]
        except Exception:
            return []

    def queryset(self, request, queryset):
        """Filter queryset by continent."""
        if not self.value():
            return queryset

        continent = self.value()
        # Convert queryset to list for filtering
        filtered = [b for b in list(queryset) if b.continent == continent]

        return BackendInfoQuerySet(
            model=queryset.model,
            data=filtered,
        )


class CountryFilter(admin.SimpleListFilter):
    """Filter backends by country."""

    title = _("Country")
    parameter_name = "country_code"

    def lookups(self, request, model_admin):
        """Return list of country code choices."""
        try:
            from django.apps import apps

            apps.check_apps_ready()

            from django.conf import settings
            from python_companyatlas.backends import get_backends

            config = getattr(settings, "COMPANYATLAS", {})
            statuses = get_backends(config=config)
            countries = sorted(
                set(s.get("country_code") for s in statuses if s.get("country_code"))
            )
            return [(c, c) for c in countries]
        except Exception:
            return []

    def queryset(self, request, queryset):
        """Filter queryset by country."""
        if not self.value():
            return queryset

        country_code = self.value()
        # Convert queryset to list for filtering
        filtered = [b for b in list(queryset) if b.country_code == country_code]

        return BackendInfoQuerySet(
            model=queryset.model,
            data=filtered,
        )


class StatusFilter(admin.SimpleListFilter):
    """Filter backends by status."""

    title = _("Status")
    parameter_name = "status"

    def lookups(self, request, model_admin):
        """Return list of status choices."""
        return [
            ("available", _("✅ Available")),
            ("missing_packages", _("❌ Missing Packages")),
            ("missing_config", _("⚠️ Missing Config")),
            ("unavailable", _("❌ Unavailable")),
        ]

    def queryset(self, request, queryset):
        """Filter queryset by status."""
        if not self.value():
            return queryset

        status = self.value()
        # Convert queryset to list for filtering
        filtered = [b for b in list(queryset) if b.status == status]

        return BackendInfoQuerySet(
            model=queryset.model,
            data=filtered,
        )


# Don't use @admin.register decorator here to avoid AppRegistryNotReady
# Registration is done in apps.py ready() method
class BackendInfoAdmin(admin.ModelAdmin):
    """Administration en lecture seule pour consulter le statut des backends."""

    ordering = ["continent", "country_code", "name"]

    list_display = [
        "name_display",
        "continent_display",
        "country_display",
        "can_fetch_company_data",
        "can_fetch_documents",
        "can_fetch_events",
        "status_display",
    ]

    list_filter = [ContinentFilter, CountryFilter]

    search_fields = ["name", "display_name", "country_code", "continent"]

    change_form_template = "admin/companyatlas/backendinfo/change_form.html"


    readonly_fields = [
        "name",
        "display_name",
        "continent",
        "country_code_display",
        "company_data_capability",
        "documents_capability",
        "events_capability",
        "status_display_detail",
        "packages_display_detail",
        "config_display_detail",
        "documentation_url_display",
        "site_url_display",
        "status_url_display",
        "description_display",
    ]

    fieldsets = (
        (
            _("General Information"),
            {
                "fields": (
                    "name",
                    "display_name",
                    "description_display",
                    "continent",
                    "country_code_display",
                    "status_display_detail",
                )
            },
        ),
        (
            _("Capabilities"),
            {
                "fields": (
                    "company_data_capability",
                    "documents_capability",
                    "events_capability",
                )
            },
        ),
        (
            _("Requirements"),
            {
                "fields": (
                    "packages_display_detail",
                    "config_display_detail",
                )
            },
        ),
        (
            _("Links"),
            {
                "fields": (
                    "documentation_url_display",
                    "site_url_display",
                    "status_url_display",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        """Override to use our custom manager that doesn't access database."""
        return self.model.objects.get_queryset()

    def save_model(self, request, obj, form, change):
        """Prevent saving - this is a virtual model."""
        pass

    def delete_model(self, request, obj):
        """Prevent deletion - this is a virtual model."""
        pass

    def get_object(self, request, object_id, from_field=None):
        """Get backend object by its name (which is the pk)."""
        if object_id is None:
            return None
        try:
            queryset = self.get_queryset(request)
            # For virtual models, iterate through queryset to find matching pk
            object_id_str = str(object_id)
            for backend in queryset:
                # Match by pk (which is the backend name)
                if str(backend.pk) == object_id_str or backend.name == object_id_str:
                    return backend
                # Also try matching by display_name
                if backend.display_name and backend.display_name.lower() == object_id_str.lower():
                    return backend
            return None
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error getting backend object {object_id}: {e}", exc_info=True)
            return None

    def get_search_results(self, request, queryset, search_term):
        """Implement manual search for custom QuerySet."""
        if not search_term:
            return queryset, False

        search_term_lower = search_term.lower()
        filtered = []

        for backend in queryset:
            if search_term_lower in backend.name.lower():
                filtered.append(backend)
                continue

            if backend.display_name and search_term_lower in backend.display_name.lower():
                filtered.append(backend)
                continue

            if search_term_lower in backend.country_code.lower():
                filtered.append(backend)
                continue

            if search_term_lower in backend.continent.lower():
                filtered.append(backend)
                continue

        filtered_qs = BackendInfoQuerySet(
            model=queryset.model,
            data=filtered,
        )

        return filtered_qs, False

    @admin.display(description=_("Backend"))
    def name_display(self, obj):
        """Display backend name with description."""
        if not obj:
            return "-"
        description = obj.description_text
        name = obj.display_name or obj.name or "Unknown"
        if description:
            return format_html(
                '<strong>{}</strong><br><span style="color: #6c757d; font-size: 11px; '
                'font-style: italic;">{}</span>',
                name,
                description,
            )
        else:
            return format_html("<strong>{}</strong>", name)

    @admin.display(description=_("Continent"))
    def continent_display(self, obj):
        """Display continent with badge."""
        if not obj:
            return "-"
        if obj.continent:
            return format_html(
                '<span style="background-color: #e7f3ff; color: #0c5b9d; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
                obj.continent.title(),
            )
        return mark_safe('<span style="color: #ccc;">—</span>')

    @admin.display(description=_("Country"))
    def country_display(self, obj):
        """Display country code with flag badge."""
        if not obj:
            return "-"
        if obj.country_code:
            # Try to use flag image (base64) first, fallback to emoji
            flag_image = obj.country_flag_image or ""
            flag_emoji = obj.country_flag or ""

            if flag_image:
                # Use flag image from flagpy
                return format_html(
                    '<span style="background-color: #d1e7dd; color: #0f5132; padding: 3px 8px; '
                    'border-radius: 3px; font-size: 11px; font-weight: bold; '
                    'display: inline-flex; align-items: center; gap: 6px;">'
                    '<img src="{}" alt="{}" style="width: 20px; height: 12px; '
                    'vertical-align: middle;"> {}</span>',
                    mark_safe(flag_image),  # Mark image URL as safe
                    obj.country_code,  # Alt text
                    obj.country_code,  # Country code will be escaped by format_html
                )
            elif flag_emoji:
                # Fallback to emoji
                return format_html(
                    '<span style="background-color: #d1e7dd; color: #0f5132; padding: 3px 8px; '
                    'border-radius: 3px; font-size: 11px; font-weight: bold;">{} {}</span>',
                    mark_safe(flag_emoji),  # Mark flag as safe
                    obj.country_code,  # Country code will be escaped by format_html
                )
            else:
                # No flag available, just show country code
                return format_html(
                    '<span style="background-color: #d1e7dd; color: #0f5132; padding: 3px 8px; '
                    'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
                    obj.country_code,
                )
        return mark_safe('<span style="color: #ccc;">—</span>')

    @admin.display(description=_("Country"))
    def country_code_display(self, obj):
        """Display country code with flag in detail view."""
        if not obj:
            return "-"
        if obj.country_code:
            # Try to use flag image (base64) first, fallback to emoji
            flag_image = obj.country_flag_image or ""
            flag_emoji = obj.country_flag or ""

            if flag_image:
                # Use flag image from flagpy
                return format_html(
                    '<div style="display: flex; align-items: center; gap: 8px;">'
                    '<img src="{}" alt="{}" style="width: 48px; height: 24px; '
                    'vertical-align: middle;">'
                    '<span style="font-weight: bold; font-size: 14px;">{}</span>'
                    "</div>",
                    mark_safe(flag_image),  # Mark image URL as safe
                    obj.country_code,  # Alt text
                    obj.country_code,  # Country code will be escaped by format_html
                )
            elif flag_emoji:
                # Fallback to emoji
                return format_html(
                    '<div style="display: flex; align-items: center; gap: 8px;">'
                    '<span style="font-size: 24px;">{}</span>'
                    '<span style="font-weight: bold; font-size: 14px;">{}</span>'
                    "</div>",
                    mark_safe(flag_emoji),  # Mark flag as safe
                    obj.country_code,  # Country code will be escaped by format_html
                )
            else:
                # No flag available, just show country code
                return format_html(
                    '<div style="display: flex; align-items: center; gap: 8px;">'
                    '<span style="font-weight: bold; font-size: 14px;">{}</span>'
                    "</div>",
                    obj.country_code,
                )
        return mark_safe('<span style="color: #ccc;">—</span>')

    @admin.display(description=_("Status"))
    def status_display(self, obj):
        """Display status badge."""
        if not obj:
            return "-"
        if obj.status == "available":
            return mark_safe(
                '<span style="background-color: #d1e7dd; color: #0f5132; padding: 5px 12px; '
                "border-radius: 4px; font-size: 12px; font-weight: bold; "
                'white-space: nowrap;">✅ Available</span>'
            )
        elif obj.status == "missing_packages":
            return mark_safe(
                '<span style="background-color: #f8d7da; color: #842029; padding: 5px 12px; '
                "border-radius: 4px; font-size: 12px; font-weight: bold; "
                'white-space: nowrap;">❌ Missing Packages</span>'
            )
        elif obj.status == "missing_config":
            return mark_safe(
                '<span style="background-color: #fff3cd; color: #664d03; padding: 5px 12px; '
                "border-radius: 4px; font-size: 12px; font-weight: bold; "
                'white-space: nowrap;">⚠️ Missing Config</span>'
            )
        else:
            return mark_safe(
                '<span style="background-color: #f8d7da; color: #842029; padding: 5px 12px; '
                "border-radius: 4px; font-size: 12px; font-weight: bold; "
                'white-space: nowrap;">❌ Unavailable</span>'
            )

    @admin.display(description=_("Status"))
    def status_display_detail(self, obj):
        """Display status in detail view."""
        return self.status_display(obj)

    @admin.display(description=_("Packages"))
    def packages_display(self, obj):
        """Display package status summary."""
        if not obj:
            return "-"
        packages = obj.packages
        if not packages:
            return mark_safe('<span style="color: #6c757d; font-style: italic;">None</span>')

        missing = [pkg for pkg, installed in packages.items() if not installed]
        if missing:
            return format_html(
                '<span style="color: #dc3545;">❌ {} missing</span>',
                len(missing),
            )
        return mark_safe('<span style="color: #198754;">✅ All installed</span>')

    @admin.display(description=_("Packages"))
    def packages_display_detail(self, obj):
        """Display detailed package information with installation status.

        Uses the same format as django-missive: list of packages with status icons.
        """
        if not obj:
            return mark_safe('<p style="color: #666;">No backend selected.</p>')

        packages = obj.packages
        if not packages:
            return mark_safe(
                '<span style="color: #6c757d; white-space: nowrap; font-style: italic;">No specific packages required for this backend.</span>'
            )

        package_statuses = []
        missing_packages = []

        for package, installed in packages.items():
            # Double-check installation status
            is_installed = installed
            if not is_installed:
                # Try to import to verify
                try:
                    importlib.import_module(package)
                    is_installed = True
                except ImportError:
                    try:
                        # Try with hyphens replaced by underscores
                        importlib.import_module(package.replace("-", "_"))
                        is_installed = True
                    except ImportError:
                        is_installed = False

            if is_installed:
                package_statuses.append(
                    format_html(
                        '<span style="color: #198754;">✓</span> <code>{}</code>',
                        package,
                    )
                )
            else:
                package_statuses.append(
                    format_html(
                        '<span style="color: #dc3545;">✗ <code style="color: #dc3545;">{}</code></span>',
                        package,
                    )
                )
                missing_packages.append(package)

        # Also check obj.missing_packages if available (from diagnostic)
        if hasattr(obj, "missing_packages") and obj.missing_packages:
            for pkg in obj.missing_packages:
                if pkg not in missing_packages and pkg not in packages:
                    missing_packages.append(pkg)
                    package_statuses.append(
                        format_html(
                            '<span style="color: #dc3545;">✗ <code style="color: #dc3545;">{}</code></span>',
                            pkg,
                        )
                    )

        # Use format_html_join like django-missive
        packages_html = format_html_join(", ", "{}", ((status,) for status in package_statuses))

        result = format_html(
            '<span style="white-space: nowrap;">{}</span>',
            packages_html,
        )

        # Add installation instructions if packages are missing
        if missing_packages:
            packages_list = ", ".join(
                f"<code>{pkg}</code>" for pkg in missing_packages
            )
            instructions_html = format_html(
                '<p style="margin-top: 15px; padding: 10px; background-color: #fff3cd; border-left: 4px solid #ffc107; color: #856404;">'
                "<strong>💡 To install missing packages:</strong><br>"
                '<code style="background-color: #f8f9fa; padding: 4px 8px; border-radius: 3px; display: inline-block; margin-top: 8px;">'
                "pip install {}</code>"
                "</p>",
                mark_safe(packages_list),
            )
            return format_html("{}<br>{}", result, instructions_html)

        return result

    @admin.display(description=_("Config"))
    def config_display(self, obj):
        """Display config status summary."""
        if not obj:
            return "-"
        missing = obj.missing_config
        if not missing:
            return mark_safe('<span style="color: #198754;">✅ Configured</span>')
        return format_html(
            '<span style="color: #ffc107;">⚠️ {} missing</span>',
            len(missing),
        )

    @admin.display(description=_("Configuration"))
    def config_display_detail(self, obj):
        """Display detailed configuration information."""
        if not obj:
            return mark_safe('<p style="color: #666;">No backend selected.</p>')
        config_status = obj.diagnostic.get("config", {})

        if not config_status:
            return mark_safe(
                '<p style="color: #666;">No specific configuration required for this backend.</p>'
            )

        rows = []
        for key, configured in config_status.items():
            if configured:
                icon = mark_safe('<span style="color: #198754; font-weight: bold;">✓</span>')
                status_text = mark_safe('<span style="color: #198754;">Configured</span>')
            else:
                icon = mark_safe('<span style="color: #dc3545; font-weight: bold;">✗</span>')
                status_text = mark_safe('<span style="color: #dc3545;">Missing</span>')

            rows.append(
                format_html(
                    "<tr>"
                    '<td style="padding: 8px; width: 30px;">{}</td>'
                    '<td style="padding: 8px;"><code>{}</code></td>'
                    '<td style="padding: 8px;">{}</td>'
                    "</tr>",
                    icon,
                    key,
                    status_text,
                )
            )

        # Use mark_safe to preserve HTML in rows
        rows_html = mark_safe("".join(str(row) for row in rows))
        table_html = format_html(
            """
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
                <tr style="background-color: #f8f9fa;">
                    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6; width: 30px;"></th>
                    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Variable</th>
                    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Status</th>
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
        <p style="margin-top: 15px; padding: 10px; background-color: #cfe2ff; "
           "border-left: 4px solid #0d6efd; color: #084298;">
            <strong>💡 To configure:</strong> Edit the <code>COMPANYATLAS</code> setting
            in your Django settings.
        </p>
        """,
            rows_html,
        )

        return table_html

    @admin.display(description=_("Documentation"))
    def documentation_url_display(self, obj):
        """Display documentation URL."""
        if not obj:
            return "-"
        url = obj.documentation_url
        if url:
            return format_html(
                '<a href="{}" target="_blank" style="white-space: nowrap;">'
                '<span style="color: #0d6efd;">📖 Documentation</span>'
                "</a>",
                url,
            )
        return mark_safe(
            '<span style="color: #6c757d; font-style: italic; white-space: nowrap;">'
            "Not available</span>"
        )

    @admin.display(description=_("Official Site"))
    def site_url_display(self, obj):
        """Display official site URL."""
        if not obj:
            return "-"
        url = obj.site_url
        if url:
            return format_html(
                '<a href="{}" target="_blank" style="white-space: nowrap;">'
                '<span style="color: #0d6efd;">🌐 Official Site</span>'
                "</a>",
                url,
            )
        return mark_safe(
            '<span style="color: #6c757d; font-style: italic; white-space: nowrap;">'
            "Not available</span>"
        )

    @admin.display(description=_("Status Page"))
    def status_url_display(self, obj):
        """Display status page URL."""
        if not obj:
            return "-"
        url = obj.status_url
        if url:
            return format_html(
                '<a href="{}" target="_blank" style="white-space: nowrap;">'
                '<span style="color: #0d6efd;">🔗 Status Page</span>'
                "</a>",
                url,
            )
        return mark_safe(
            '<span style="color: #6c757d; font-style: italic; white-space: nowrap;">'
            "Not available</span>"
        )

    @admin.display(description=_("Description"))
    def description_display(self, obj):
        """Display backend description."""
        if not obj:
            return mark_safe('<p style="color: #ccc; font-style: italic;">No backend selected</p>')
        description = obj.description_text
        if description:
            return format_html('<p style="color: #666;">{}</p>', description)
        return mark_safe('<p style="color: #ccc; font-style: italic;">No description available</p>')

    @admin.display(description=_("Company Data"))
    def can_fetch_company_data(self, obj):
        """Display if backend can fetch company data with cost."""
        if not obj:
            return "-"
        if not obj.can_fetch_company_data:
            return "-"
        cost = getattr(obj, "_request_cost", {}).get("data", "free")
        if cost == "free":
            return mark_safe('<span style="color: #198754;">✓</span> (free)')
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
        return format_html('<span style="color: #198754;">✓</span> ({})', cost_str)

    @admin.display(description=_("Documents"))
    def can_fetch_documents(self, obj):
        """Display if backend can fetch documents with cost."""
        if not obj:
            return "-"
        if not obj.can_fetch_documents:
            return "-"
        cost = getattr(obj, "_request_cost", {}).get("documents", "free")
        if cost == "free":
            return mark_safe('<span style="color: #198754;">✓</span> (free)')
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
        return format_html('<span style="color: #198754;">✓</span> ({})', cost_str)

    @admin.display(description=_("Events"))
    def can_fetch_events(self, obj):
        """Display if backend can fetch events with cost."""
        if not obj:
            return "-"
        if not obj.can_fetch_events:
            return "-"
        cost = getattr(obj, "_request_cost", {}).get("events", "free")
        if cost == "free":
            return mark_safe('<span style="color: #198754;">✓</span> (free)')
        cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
        return format_html('<span style="color: #198754;">✓</span> ({})', cost_str)

    @admin.display(description=_("Company Data"))
    def company_data_capability(self, obj):
        """Display company data capability."""
        if not obj:
            return "-"
        request_cost = getattr(obj, "_request_cost", {})
        cost = request_cost.get("data", "free")
        if obj.can_fetch_company_data:
            if cost == "free":
                return mark_safe('<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled (free)</span>')
            else:
                cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
                return mark_safe(f'<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled ({cost_str})</span>')
        else:
            return mark_safe('<span style="color: #6c757d; font-weight: bold;">○</span> <span style="color: #6c757d;">Not available</span>')

    @admin.display(description=_("Documents"))
    def documents_capability(self, obj):
        """Display documents capability."""
        if not obj:
            return "-"
        request_cost = getattr(obj, "_request_cost", {})
        cost = request_cost.get("documents", "free")
        if obj.can_fetch_documents:
            if cost == "free":
                return mark_safe('<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled (free)</span>')
            else:
                cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
                return mark_safe(f'<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled ({cost_str})</span>')
        else:
            return mark_safe('<span style="color: #6c757d; font-weight: bold;">○</span> <span style="color: #6c757d;">Not available</span>')

    @admin.display(description=_("Events"))
    def events_capability(self, obj):
        """Display events capability."""
        if not obj:
            return "-"
        request_cost = getattr(obj, "_request_cost", {})
        cost = request_cost.get("events", "free")
        if obj.can_fetch_events:
            if cost == "free":
                return mark_safe('<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled (free)</span>')
            else:
                cost_str = f"{cost:.2f}" if isinstance(cost, (int, float)) else str(cost)
                return mark_safe(f'<span style="color: #198754; font-weight: bold;">✓</span> <span style="color: #198754;">Enabled ({cost_str})</span>')
        else:
            return mark_safe('<span style="color: #6c757d; font-weight: bold;">○</span> <span style="color: #6c757d;">Not available</span>')
