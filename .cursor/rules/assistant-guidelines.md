## Assistant Guidelines

### Project Purpose

**django-companyatlas** provides Django integration for **python-companyatlas**, which collects company information from official sources by country. The library aggregates data about:
- Company addresses (headquarters, branches, registered offices)
- Subsidiaries and corporate structure
- Official documents (registrations, financial reports, certifications)
- Company identifiers (SIREN, VAT, registration numbers by country)

Providers in python-companyatlas are organized by **continent/country** hierarchy (e.g., `providers/europe/france/infogreffe.py`).

### Development Guidelines

- Always execute project tooling through `python dev.py <command>`.
- Default to English for comments, docstrings, and translations.
- Keep comments minimal and only when they clarify non-obvious logic.
- Avoid reiterating what the code already states clearly.
- Add comments only when they resolve likely ambiguity or uncertainty.
- Keep integration with `python-companyatlas` clean: use the library for all company data operations (lookup, enrichment, validation) without reimplementing core logic in Django models or views.
- Django models should store company data but delegate business logic to `python_companyatlas`.
- Use Django signals and tasks (Celery/Django-Q) for async operations like background enrichment.
- Company identifiers must support multiple formats per country (domain, SIREN/France, CRN/UK, VAT, etc.) through a flexible model design.
- Models should store collected data types: addresses (JSONField for multiple locations), subsidiaries (relationships), documents (FileField/URLs), identifiers (country-specific fields).
- API endpoints should follow REST conventions and include proper pagination, filtering, and search capabilities.
- Admin interface should provide company search, enrichment triggers, and data visualization.
- Always handle API rate limits and failures gracefully with proper retry logic.

