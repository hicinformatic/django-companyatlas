"""Helper functions for company data management."""

from typing import Optional, Dict, Any
from django.db import transaction

from .models import Company, CompanyData, CompanyCountryData


def create_or_update_company_data(
    country: str,
    data_type: str,
    value,
    company: Optional[Company] = None,
    company_name: Optional[str] = None,
    value_type: Optional[str] = None,
    **company_kwargs
) -> tuple[Company, CompanyData]:
    """Create or update company data.
    
    This function allows inserting data like:
    - france, denomination, "Tour Eiffel" (str)
    - france, siren, "123456789" (str)
    - france, capital, 100000.50 (float)
    - france, employees, 150 (int)
    - france, metadata, {"key": "value"} (json)
    
    Args:
        country: ISO country code (e.g., "FR", "france")
        data_type: Type of data (e.g., "denomination", "siren", "rna", "capital")
        value: Data value (can be str, int, float, dict, list)
        company: Existing Company instance (optional)
        company_name: Company name to use if creating new company
        value_type: Optional value type override (auto-detected if not provided)
        **company_kwargs: Additional fields for Company model
    
    Returns:
        Tuple of (Company, CompanyData) instances
    
    Example:
        >>> company, data = create_or_update_company_data(
        ...     country="FR",
        ...     data_type="denomination",
        ...     value="Tour Eiffel",
        ...     company_name="Tour Eiffel"
        ... )
        >>> company, data = create_or_update_company_data(
        ...     country="FR",
        ...     data_type="capital",
        ...     value=100000.50
        ... )
        >>> company, data = create_or_update_company_data(
        ...     country="FR",
        ...     data_type="employees",
        ...     value=150
        ... )
    """
    # Normalize country code
    country = country.upper()
    if country == "FRANCE":
        country = "FR"
    
    # Get or create company
    if company is None:
        if not company_name:
            company_name = value if data_type == "denomination" else "Unknown Company"
        
        # Try to find existing company by name
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={
                "country": country,
                **company_kwargs
            }
        )
        if not created:
            # Update country if not set
            if not company.country:
                company.country = country
                company.save(update_fields=["country"])
    else:
        # Update company country if not set
        if not company.country:
            company.country = country
            company.save(update_fields=["country"])
    
    # Create or update data
    data, created = CompanyData.objects.get_or_create(
        company=company,
        country=country,
        data_type=data_type,
        defaults={}
    )
    
    # Set value with automatic type detection or explicit type
    if value_type:
        data.value_type = value_type
        data.value = str(value)
    else:
        data.set_value(value)
    data.save()
    
    # If this is a structured field, also update CompanyCountryData
    if data_type in ["siren", "siret", "rna", "ape", "legal_form", "rcs"]:
        country_data, _ = CompanyCountryData.objects.get_or_create(
            company=company,
            country=country,
            defaults={}
        )
        # Convert value to string for structured fields
        str_value = str(data.get_value()) if data.get_value() is not None else ""
        setattr(country_data, data_type, str_value)
        country_data.save(update_fields=[data_type])
    
    return company, data


def bulk_create_company_data(
    data_list: list[tuple[str, str, str]],
    company_name: Optional[str] = None
) -> Company:
    """Bulk create company data from a list of tuples.
    
    Args:
        data_list: List of tuples (country, data_type, value)
        company_name: Company name (optional, will use first denomination if not provided)
    
    Returns:
        Company instance
    
    Example:
        >>> company = bulk_create_company_data([
        ...     ("FR", "denomination", "Tour Eiffel"),
        ...     ("FR", "siren", "123456789"),
        ...     ("FR", "rna", "W12345678"),
        ... ])
    """
    company = None
    
    with transaction.atomic():
        for country, data_type, value in data_list:
            # Use first denomination as company name if not provided
            if company is None and data_type == "denomination" and not company_name:
                company_name = value
            
            company, _ = create_or_update_company_data(
                country=country,
                data_type=data_type,
                value=value,
                company=company,
                company_name=company_name
            )
    
    return company


def get_company_by_country_data(
    country: str,
    data_type: str,
    value: str
) -> Optional[Company]:
    """Find a company by country-specific data.
    
    Args:
        country: ISO country code
        data_type: Type of data (e.g., "siren", "rna")
        value: Data value
    
    Returns:
        Company instance or None
    
    Example:
        >>> company = get_company_by_country_data("FR", "siren", "123456789")
    """
    country = country.upper()
    if country == "FRANCE":
        country = "FR"
    
    try:
        # Try CompanyData first
        data = CompanyData.objects.get(
            country=country,
            data_type=data_type,
            value=value
        )
        return data.company
    except CompanyData.DoesNotExist:
        pass
    
    # Try CompanyCountryData for structured fields
    if data_type in ["siren", "siret", "rna"]:
        try:
            country_data = CompanyCountryData.objects.get(
                country=country,
                **{data_type: value}
            )
            return country_data.company
        except CompanyCountryData.DoesNotExist:
            pass
    
    return None

