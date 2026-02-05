from djcompanyatlas.models.virtuals.company import CompanyAtlasVirtualCompany


def create_company(provider: str, reference: str):
    """Create a company from a source."""
    company = CompanyAtlasVirtualCompany.objects.search_company_by_reference(
        reference=reference,
        attribute_search={"name": provider},
    ).first()
    print("provider", provider)
    print("reference", reference)
    print("company", company)
    #company, _ = CompanyAtlasCompany.objects.get_or_create(
    #    denomination=normalized_data["denomination"],
    #    code=normalized_data["code"],
    #    defaults={
    #        "source": provider,
    #        "country_code": normalized_data["country"],
    #        "metadata": normalized_data,
    #    }
    #)
    #return company
