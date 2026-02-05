"""Helper functions for company data management."""

from django.db import transaction

from .models import (
    CompanyAtlasAddress,
    CompanyAtlasCompany,
    CompanyAtlasData,
)


@transaction.atomic
def create_company(obj):
    company = CompanyAtlasCompany.objects.create(
        denomination=obj.denomination,
        code=obj.reference,
        source=obj.backend,
        country_code=obj.country_code,
    )
    CompanyAtlasData.objects.create(
        company=company,
        source=obj.backend,
        country_code=obj.country_code,
        data_type=obj.source_field,
        value=obj.reference,
    )
    if obj.address:
        CompanyAtlasAddress.objects.create(
            company=company,
            source=obj.backend,
            country_code=obj.country_code,
            address=obj.address_json,
            is_headquarters=True,
        )
    return company
