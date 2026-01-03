"""Tests for Company model."""

import pytest
from django.utils import timezone

from djcompanyatlas.models import Company


@pytest.mark.django_db
class TestCompanyModel:
    """Tests for Company model."""

    def test_company_creation(self):
        """Test basic company creation."""
        company = Company.objects.create(name="Test Company", domain="test.com")

        assert company.name == "Test Company"
        assert company.domain == "test.com"
        assert company.is_enriched is False
        assert company.enriched_at is None

    def test_company_str(self):
        """Test company string representation."""
        company = Company.objects.create(name="Example Corp", domain="example.com")

        assert str(company) == "Example Corp"

    def test_company_with_identifiers(self):
        """Test company with multiple identifiers."""
        from djcompanyatlas.models import CompanyCountryData

        company = Company.objects.create(
            name="French Company", domain="french.fr", vat_number="FR12345678901", country="FR"
        )

        # Create country-specific data with SIREN
        CompanyCountryData.objects.create(
            company=company, country="FR", siren="123456789"
        )

        assert company.vat_number == "FR12345678901"
        assert company.get_country_data("FR").siren == "123456789"

    def test_company_enrichment_fields(self):
        """Test enrichment-related fields."""
        company = Company.objects.create(
            name="Tech Startup",
            domain="techstartup.com",
            is_enriched=True,
            enriched_at=timezone.now(),
            enrichment_data={"source": "test"},
        )

        assert company.is_enriched is True
        assert company.enriched_at is not None
        assert company.enrichment_data == {"source": "test"}

    def test_company_location_fields(self):
        """Test location fields."""
        company = Company.objects.create(
            name="US Company",
            domain="uscompany.com",
            country="US",
            city="San Francisco",
            address="123 Main St",
        )

        assert company.country == "US"
        assert company.city == "San Francisco"
        assert company.address == "123 Main St"
