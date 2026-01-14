## Project Structure

django-companyatlas follows a standard Python package structure with Django integration for CompanyAtlas.

### General Structure

```
django-companyatlas/
├── src/
│   └── djcompanyatlas/        # Main package directory
│       ├── __init__.py        # Package exports
│       ├── models/            # Django model definitions
│       ├── models.py          # Model definitions
│       ├── managers/          # Custom managers
│       ├── admin/             # Django admin configuration
│       ├── views.py           # Django views
│       ├── urls.py             # URL configuration
│       ├── helpers.py          # Helper functions
│       ├── apps.py             # Django app configuration
│       └── templates/          # Django templates
├── tests/                     # Test suite
│   └── ...
├── docs/                      # Documentation
│   └── ...
├── service.py                 # Main service entry point script
├── pyproject.toml             # Project configuration
└── ...
```

### Module Organization Principles

- **Single Responsibility**: Each module should have a clear, single purpose
- **Separation of Concerns**: Keep different concerns in separate modules
- **Django Integration**: Integrates CompanyAtlas with Django's ORM and admin
- **Clear Exports**: Use `__init__.py` to define public API

### Model Organization

The `models/` directory and `models.py` contain Django model definitions for company data.

### Manager Organization

The `managers/` directory contains custom managers for company models.

### Admin Organization

The `admin/` directory contains Django admin configurations for company models.

### Package Exports

The public API is defined in `src/djcompanyatlas/__init__.py`:
- Models, managers, and admin configurations

### CompanyAtlas Integration

django-companyatlas integrates CompanyAtlas with Django:
- Uses CompanyAtlas providers for company data lookup
- Provides Django models and admin interface for company data
- Integrates company lookup and enrichment in Django applications
