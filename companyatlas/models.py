"""Company models."""

from django.db import models
from django.utils import timezone
from django.conf import settings


class Company(models.Model):
    """Company information model."""

    # Identifiers
    domain = models.CharField(max_length=255, unique=True, help_text="Company domain (e.g., example.com)")
    siren = models.CharField(max_length=20, blank=True, null=True, help_text="French SIREN number")
    vat_number = models.CharField(max_length=50, blank=True, null=True, help_text="VAT/Tax identification number")
    stock_symbol = models.CharField(max_length=10, blank=True, null=True, help_text="Stock ticker symbol")
    
    # Basic information
    name = models.CharField(max_length=255, help_text="Company name")
    legal_name = models.CharField(max_length=255, blank=True, help_text="Legal/registered name")
    description = models.TextField(blank=True, help_text="Company description")
    
    # Details (can be enriched)
    founded_year = models.IntegerField(null=True, blank=True, help_text="Year founded")
    employee_count = models.IntegerField(null=True, blank=True, help_text="Number of employees")
    industry = models.CharField(max_length=100, blank=True, help_text="Industry/sector")
    website = models.URLField(blank=True, help_text="Company website")
    
    # Location
    country = models.CharField(max_length=2, blank=True, help_text="ISO country code")
    city = models.CharField(max_length=100, blank=True, help_text="City")
    address = models.TextField(blank=True, help_text="Full address")
    
    # Enrichment
    is_enriched = models.BooleanField(default=False, help_text="Whether company data has been enriched")
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
            models.Index(fields=["siren"]),
            models.Index(fields=["vat_number"]),
            models.Index(fields=["-created_at"]),
        ]
    
    def __str__(self):
        return self.name
    
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

