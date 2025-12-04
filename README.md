# django-companyatlas

Django integration for company information lookup and enrichment using python-companyatlas.

## Features

- 🏢 Company model with multiple identifier types (domain, SIREN, VAT, etc.)
- 🔍 Automatic company data enrichment
- 🎨 Admin interface for company management
- 📊 RESTful API endpoints
- ⚡ Background enrichment with Celery support
- 🔄 Sync with python-companyatlas library

## Installation

```bash
pip install django-companyatlas
```

## Quick Start

1. **Add to INSTALLED_APPS**:

```python
INSTALLED_APPS = [
    ...
    'companyatlas',
]
```

2. **Configure settings** (optional):

```python
COMPANYATLAS = {
    'API_KEY': 'your-api-key',  # If needed
    'AUTO_ENRICH': True,  # Auto-enrich on company creation
    'CACHE_TIMEOUT': 3600,  # Cache enrichment for 1 hour
}
```

3. **Run migrations**:

```bash
python manage.py migrate
```

4. **Start using**:

```python
from companyatlas.models import Company

# Create a company
company = Company.objects.create(
    name="Example Corp",
    domain="example.com"
)

# Enrich company data
company.enrich()

# Check enrichment status
if company.is_enriched:
    print(f"Founded: {company.founded_year}")
    print(f"Employees: {company.employee_count}")
```

## Development

```bash
# Setup
python dev.py venv
python dev.py install-dev
python dev.py update-companyatlas  # Install local python-companyatlas

# Database
python dev.py migrate
python dev.py createsuperuser

# Run server
python dev.py runserver

# Tests
python dev.py test
python dev.py coverage

# Code quality
python dev.py lint
python dev.py format
```

## Models

### Company

Main model for storing company information:

- **Identifiers**: domain, siren, vat_number, stock_symbol
- **Basic info**: name, legal_name, description
- **Details**: founded_year, employee_count, industry, location
- **Enrichment**: enriched_at, enrichment_data (JSON)
- **Timestamps**: created_at, updated_at

## API Endpoints

```
GET    /api/companies/              List companies
POST   /api/companies/              Create company
GET    /api/companies/{id}/         Retrieve company
PATCH  /api/companies/{id}/         Update company
DELETE /api/companies/{id}/         Delete company
POST   /api/companies/{id}/enrich/  Trigger enrichment
```

## Configuration

Available settings in `settings.COMPANYATLAS`:

```python
COMPANYATLAS = {
    # API configuration (passed to python-companyatlas)
    'API_KEY': None,
    'BASE_URL': 'https://api.example.com',
    'TIMEOUT': 30,
    
    # Django-specific settings
    'AUTO_ENRICH': True,  # Auto-enrich on creation
    'CACHE_TIMEOUT': 3600,  # Cache duration in seconds
    'ENRICH_ON_SAVE': False,  # Enrich on every save
    'USE_CELERY': False,  # Use Celery for async enrichment
}
```

## License

MIT

