"""Company models with international and country-specific data."""

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


class Company(models.Model):
    """International company information model.

    Contains data that is universal across all countries.
    """

    # Universal identifiers
    domain = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Company domain (e.g., example.com)",
    )
    vat_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="VAT/Tax identification number (international)",
    )
    stock_symbol = models.CharField(
        max_length=10, blank=True, null=True, help_text="Stock ticker symbol"
    )

    # Basic information (universal)
    name = models.CharField(max_length=255, help_text="Company name")
    legal_name = models.CharField(max_length=255, blank=True, help_text="Legal/registered name")
    description = models.TextField(blank=True, help_text="Company description")

    # Universal details
    founded_year = models.IntegerField(null=True, blank=True, help_text="Year founded")
    employee_count = models.IntegerField(null=True, blank=True, help_text="Number of employees")
    industry = models.CharField(max_length=100, blank=True, help_text="Industry/sector")
    website = models.URLField(blank=True, help_text="Company website")

    # Location (universal)
    country = models.CharField(
        max_length=2, blank=True, help_text="ISO country code (e.g., FR, US, GB)"
    )
    city = models.CharField(max_length=100, blank=True, help_text="City")
    address = models.TextField(blank=True, help_text="Full address")

    # Enrichment metadata
    is_enriched = models.BooleanField(
        default=False, help_text="Whether company data has been enriched"
    )
    enriched_at = models.DateTimeField(null=True, blank=True, help_text="Last enrichment timestamp")
    enrichment_data = models.JSONField(default=dict, blank=True, help_text="Raw enrichment data")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["domain"]),
            models.Index(fields=["vat_number"]),
            models.Index(fields=["country"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

    def get_country_data(self, country_code: str = None):
        """Get country-specific data for this company.

        Args:
            country_code: ISO country code (defaults to self.country)

        Returns:
            CompanyCountryData instance or None
        """
        country_code = country_code or self.country
        if not country_code:
            return None

        try:
            return self.country_data.get(country=country_code.upper())
        except CompanyCountryData.DoesNotExist:
            return None

    def get_data_value(self, country_code: str, data_type: str):
        """Get a specific data value for a country.

        Args:
            country_code: ISO country code (e.g., "FR")
            data_type: Type of data (e.g., "denomination", "siren", "rna")

        Returns:
            Data value converted to its proper type, or None
        """
        try:
            data = self.data.get(country=country_code.upper(), data_type=data_type)
            return data.get_value()
        except CompanyData.DoesNotExist:
            return None

    def set_data_value(self, country_code: str, data_type: str, value, value_type: str = None):
        """Set a specific data value for a country.

        Args:
            country_code: ISO country code (e.g., "FR")
            data_type: Type of data (e.g., "denomination", "siren", "rna")
            value: Value to set (can be str, int, float, dict, list)
            value_type: Optional value type override (auto-detected if not provided)
        """
        data, created = CompanyData.objects.get_or_create(
            company=self, country=country_code.upper(), data_type=data_type, defaults={}
        )
        if value_type:
            data.value_type = value_type
            data.value = str(value)
        else:
            data.set_value(value)
        data.save()

    def enrich(self, force=False):
        """Enrich company data using python-companyatlas.

        Args:
            force: Force enrichment even if recently enriched

        Returns:
            bool: True if enrichment was successful
        """
        try:
            from python_companyatlas import CompanyAtlas
        except ImportError:
            return False

        # Check if we should enrich
        if not force and self.is_enriched and self.enriched_at:
            cache_timeout = getattr(settings, "COMPANYATLAS", {}).get("CACHE_TIMEOUT", 3600)
            if (timezone.now() - self.enriched_at).total_seconds() < cache_timeout:
                return True

        # Get API configuration
        config = getattr(settings, "COMPANYATLAS", {})
        api_key = config.get("API_KEY")

        # Create client and lookup
        atlas = CompanyAtlas(api_key=api_key, config=config)

        try:
            # Lookup company by domain
            result = atlas.lookup(self.domain)

            # Update fields from result
            if result.get("name"):
                self.name = result["name"]
            if result.get("founded_year"):
                self.founded_year = result["founded_year"]
            if result.get("employee_count"):
                self.employee_count = result["employee_count"]
            if result.get("industry"):
                self.industry = result["industry"]

            # Store raw data
            self.enrichment_data = result
            self.is_enriched = True
            self.enriched_at = timezone.now()
            self.save()

            return True
        except Exception:
            return False

    def save(self, *args, **kwargs):
        """Override save to handle auto-enrichment."""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Auto-enrich on creation if enabled
        if is_new:
            config = getattr(settings, "COMPANYATLAS", {})
            if config.get("AUTO_ENRICH", False):
                self.enrich()


class CompanyData(models.Model):
    """Flexible key-value data storage for country-specific company information.

    Allows storing arbitrary data like:
    - france, denomination, "Tour Eiffel" (str)
    - france, siren, "123456789" (str)
    - france, capital, 100000.50 (float)
    - france, employees, 150 (int)
    - france, metadata, {"key": "value"} (json)
    """

    VALUE_TYPE_CHOICES = [
        ("str", "String"),
        ("int", "Integer"),
        ("float", "Float"),
        ("json", "JSON"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="data",
        help_text="Company this data belongs to",
    )
    country = models.CharField(max_length=2, help_text="ISO country code (e.g., FR, US, GB)")
    data_type = models.CharField(
        max_length=100, help_text="Type of data (e.g., denomination, siren, capital, employees)"
    )
    value_type = models.CharField(
        max_length=10,
        choices=VALUE_TYPE_CHOICES,
        default="str",
        help_text="Type of the value (str, int, float, json)",
    )
    value = models.TextField(
        help_text="Data value (stored as string, converted based on value_type)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Data"
        verbose_name_plural = "Company Data"
        unique_together = [["company", "country", "data_type"]]
        indexes = [
            models.Index(fields=["company", "country"]),
            models.Index(fields=["country", "data_type"]),
            models.Index(fields=["data_type"]),
            models.Index(fields=["value_type"]),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.country} - {self.data_type}: {self.value}"

    def get_value(self):
        """Get the value converted to its proper type.

        Returns:
            Value converted to the appropriate type (str, int, float, or dict/list)
        """
        if self.value_type == "int":
            try:
                return int(self.value)
            except (ValueError, TypeError):
                return None
        elif self.value_type == "float":
            try:
                return float(self.value)
            except (ValueError, TypeError):
                return None
        elif self.value_type == "json":
            import json

            try:
                return json.loads(self.value)
            except (json.JSONDecodeError, TypeError):
                return None
        else:  # str
            return self.value

    def set_value(self, value):
        """Set the value, automatically detecting the type.

        Args:
            value: Value to set (will be converted to string and type detected)
        """
        if isinstance(value, (dict, list)):
            import json

            self.value = json.dumps(value)
            self.value_type = "json"
        elif isinstance(value, int):
            self.value = str(value)
            self.value_type = "int"
        elif isinstance(value, float):
            self.value = str(value)
            self.value_type = "float"
        else:
            self.value = str(value)
            self.value_type = "str"


class CompanyCountryData(models.Model):
    """Structured country-specific company data.

    Contains normalized fields for specific countries.
    For France, this would include SIREN, SIRET, RNA, etc.
    """

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="country_data",
        help_text="Company this data belongs to",
    )
    country = models.CharField(max_length=2, help_text="ISO country code (e.g., FR, US, GB)")

    # French-specific fields
    siren = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[MinLengthValidator(9)],
        help_text="French SIREN number (9 digits)",
    )
    siret = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        validators=[MinLengthValidator(14)],
        help_text="French SIRET number (14 digits)",
    )
    rna = models.CharField(
        max_length=10, blank=True, null=True, help_text="French RNA number (W + 8 digits)"
    )
    ape = models.CharField(max_length=5, blank=True, null=True, help_text="French APE/NAF code")
    legal_form = models.CharField(
        max_length=50, blank=True, null=True, help_text="Legal form (SARL, SA, etc.)"
    )
    rcs = models.CharField(
        max_length=50, blank=True, null=True, help_text="RCS registration number"
    )

    # Additional country-specific data stored as JSON
    extra_data = models.JSONField(
        default=dict, blank=True, help_text="Additional country-specific data"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Country Data"
        verbose_name_plural = "Company Country Data"
        unique_together = [["company", "country"]]
        indexes = [
            models.Index(fields=["company", "country"]),
            models.Index(fields=["country", "siren"]),
            models.Index(fields=["siren"]),
            models.Index(fields=["siret"]),
            models.Index(fields=["rna"]),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.country}"

    def get_data_dict(self) -> dict:
        """Get all data as a dictionary.

        Returns:
            Dictionary with all country-specific data
        """
        data = {
            "country": self.country,
            "siren": self.siren,
            "siret": self.siret,
            "rna": self.rna,
            "ape": self.ape,
            "legal_form": self.legal_form,
            "rcs": self.rcs,
        }
        data.update(self.extra_data)
        return {k: v for k, v in data.items() if v is not None and v != ""}
