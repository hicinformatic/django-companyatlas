"""Helper functions for company data management."""

from django.db import transaction

from .models import Company, CompanyData


def create_or_update_company_data(
    country: str,
    data_type: str,
    value,
    source: str,
    company: Company | None = None,
    company_name: str | None = None,
    value_type: str | None = None,
    **company_kwargs,
) -> tuple[Company, CompanyData]:
    """Create or update company data.

    Args:
        country: ISO country code (e.g., "FR", "france")
        data_type: Type of data (e.g., "denomination", "siren", "rna", "capital")
        value: Data value (can be str, int, float, dict, list)
        source: Backend source (e.g., "insee", "pappers", "infogreffe")
        company: Existing Company instance (optional)
        company_name: Company name to use if creating new company
        value_type: Optional value type override (auto-detected if not provided)
        **company_kwargs: Additional fields for Company model

    Returns:
        Tuple of (Company, CompanyData) instances
    """
    country = country.upper()
    if country == "FRANCE":
        country = "FR"

    if company is None:
        if not company_name:
            company_name = value if data_type == "denomination" else "Unknown Company"

        company, _ = Company.objects.get_or_create(
            name=company_name, defaults=company_kwargs
        )

    data, created = CompanyData.objects.get_or_create(
        company=company,
        source=source,
        country_code=country,
        data_type=data_type,
        defaults={},
    )

    if value_type:
        data.value_type = value_type
        data.value = str(value)
    else:
        data.set_value(value)
    data.save()

    return company, data


def bulk_create_company_data(
    data_list: list[tuple[str, str, str, str]], company_name: str | None = None
) -> Company | None:
    """Bulk create company data from a list of tuples.

    Args:
        data_list: List of tuples (country, data_type, value, source)
        company_name: Company name (optional, will use first denomination if not provided)

    Returns:
        Company instance or None if data_list is empty
    """
    company = None

    with transaction.atomic():
        for country, data_type, value, source in data_list:
            if company is None and data_type == "denomination" and not company_name:
                company_name = value

            company, _ = create_or_update_company_data(
                country=country,
                data_type=data_type,
                value=value,
                source=source,
                company=company,
                company_name=company_name,
            )

    return company


def get_company_by_country_data(
    country: str, data_type: str, value: str, source: str | None = None
) -> Company | None:
    """Find a company by country-specific data.

    Args:
        country: ISO country code
        data_type: Type of data (e.g., "siren", "rna")
        value: Data value
        source: Optional backend source filter

    Returns:
        Company instance or None
    """
    country = country.upper()
    if country == "FRANCE":
        country = "FR"

    try:
        query = CompanyData.objects.filter(
            country_code=country, data_type=data_type, value=value
        )
        if source:
            query = query.filter(source=source)
        data = query.first()
        if data:
            return data.company
    except CompanyData.DoesNotExist:
        pass

    return None
