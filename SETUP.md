# Setup django-companyatlas

Ce document récapitule la structure et la configuration du projet django-companyatlas.

## 📁 Structure du projet

```
django-companyatlas/
├── .cursor/
│   └── rules/
│       └── assistant-guidelines.md   # Règles pour l'assistant AI
├── companyatlas/                     # App Django principale
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                     # Modèle Company
│   ├── admin.py                      # Interface admin
│   ├── views.py                      # Vues
│   └── urls.py                       # URLs
├── tests/
│   ├── __init__.py
│   ├── settings.py                   # Configuration Django pour les tests
│   ├── urls.py                       # URLs de test
│   └── test_models.py                # Tests unitaires
├── dev.py                            # Script de développement
├── manage.py                         # Django management
├── pyproject.toml                    # Configuration du projet
├── requirements.txt                  # Dépendances production
├── requirements-dev.txt              # Dépendances développement
├── README.md                         # Documentation principale
├── LICENSE                           # Licence MIT
├── .gitignore                        # Fichiers à ignorer
└── env.example                       # Exemple de variables d'environnement
```

## 🚀 Quick Start

```bash
# Installation
cd /home/charl/Projects/django-companyatlas
python dev.py venv                  # Créer l'environnement virtuel
python dev.py install-dev           # Installer les dépendances
python dev.py update-companyatlas   # Installer python-companyatlas

# Optionnel : Installer flagpy pour les images de drapeaux dans l'admin
# Sur Fedora : sudo dnf install gcc-c++ python3-devel
# Puis : pip install flagpy>=1.0.0
# Note : flagpy est optionnel - l'admin utilisera des emojis drapeaux en fallback

# Database
python dev.py migrate               # Créer la base de données
python dev.py createsuperuser       # Créer un super utilisateur

# Run server
python dev.py runserver             # Démarrer le serveur (port 8000)

# Tests
python dev.py test                  # Exécuter les tests
python dev.py coverage              # Tests avec couverture

# Code quality
python dev.py lint                  # Vérifier le code
python dev.py format                # Formater le code
```

## ✅ Fonctionnalités actuelles

### **Modèle Company**

- ✅ **Identifiants multiples**: domain, SIREN, VAT, stock_symbol
- ✅ **Informations de base**: name, legal_name, description
- ✅ **Détails**: founded_year, employee_count, industry, website
- ✅ **Localisation**: country, city, address
- ✅ **Enrichissement**: is_enriched, enriched_at, enrichment_data (JSON)
- ✅ **Méthode `enrich()`**: Enrichit les données via python-companyatlas
- ✅ **Auto-enrichissement**: Optionnel à la création

### **Interface Admin**

- ✅ Liste des entreprises avec filtres
- ✅ Recherche par nom, domaine, identifiants
- ✅ Action d'enrichissement en masse
- ✅ Affichage du statut d'enrichissement

### **Views & URLs**

- ✅ Liste des entreprises
- ✅ Détail d'une entreprise
- ✅ Trigger d'enrichissement

## 📋 Commandes dev.py disponibles

### Environnement
- `venv` - Créer l'environnement virtuel
- `install` - Installer les dépendances de production
- `install-dev` - Installer les dépendances de développement
- `venv-clean` - Recréer l'environnement virtuel
- `update-companyatlas` - Installer/mettre à jour python-companyatlas localement

### Database
- `migrate` - Appliquer les migrations
- `makemigrations` - Créer de nouvelles migrations
- `resetdb` - Réinitialiser la base de données

### Server
- `runserver` - Démarrer le serveur de développement
- `shell` - Ouvrir le shell Django
- `createsuperuser` - Créer un super utilisateur

### Tests & Qualité
- `test` - Exécuter pytest
- `test-verbose` - Tests avec sortie détaillée
- `coverage` - Tests avec rapport de couverture
- `lint` - Vérifier le code (ruff + mypy)
- `format` - Formater le code avec ruff
- `check` - Vérifications complètes

### Nettoyage
- `clean` - Nettoyer tous les artefacts
- `clean-build` - Nettoyer les artefacts de build
- `clean-pyc` - Nettoyer les fichiers bytecode
- `clean-test` - Nettoyer les artefacts de tests

### Packaging
- `build` - Construire le package
- `show-version` - Afficher la version

## 🔧 Configuration

### Variables d'environnement (`.env`)

Copier `env.example` vers `.env` et configurer :

```bash
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CompanyAtlas API
COMPANYATLAS_API_KEY=your-api-key-here
```

### Settings Django

Dans `settings.py` :

```python
INSTALLED_APPS = [
    ...
    'companyatlas',
]

COMPANYATLAS = {
    'API_KEY': os.environ.get('COMPANYATLAS_API_KEY'),
    'AUTO_ENRICH': True,  # Auto-enrich on creation
    'CACHE_TIMEOUT': 3600,  # Cache for 1 hour
}
```

### Règles Cursor AI

Les règles dans `.cursor/rules/assistant-guidelines.md` :
- ✅ Utiliser `python dev.py <command>`
- ✅ Code en anglais
- ✅ Déléguer la logique métier à python-companyatlas
- ✅ Utiliser les signaux Django pour les opérations async
- ✅ Support de multiples identifiants d'entreprise
- ✅ Gestion des rate limits et erreurs API

## 📊 Statut actuel

- **Version**: 0.1.0
- **Tests**: 5/5 passent ✅
- **Migrations**: Créées et appliquées ✅
- **Admin**: Interface fonctionnelle ✅
- **python-companyatlas**: Intégré ✅
- **Documentation**: README, SETUP ✅
- **Licence**: MIT ✅

## 🎯 Utilisation du modèle Company

```python
from companyatlas.models import Company

# Créer une entreprise
company = Company.objects.create(
    name="Example Corp",
    domain="example.com"
)

# Enrichir manuellement
company.enrich()

# Ou enrichir en force (ignore le cache)
company.enrich(force=True)

# Vérifier l'enrichissement
if company.is_enriched:
    print(f"Fondée en: {company.founded_year}")
    print(f"Employés: {company.employee_count}")
    print(f"Secteur: {company.industry}")
```

## 🔗 Relations avec les autres projets

| Projet | Rôle |
|--------|------|
| **python-companyatlas** | Bibliothèque core pour lookup et enrichissement |
| **django-companyatlas** | Intégration Django + modèles + admin |
| **python-missive** | Projet similaire pour l'envoi de messages |
| **django-missive** | Projet similaire pour l'envoi de messages avec Django |

## 📚 Resources

- [python-companyatlas](../python-companyatlas) - Bibliothèque core
- [Django documentation](https://docs.djangoproject.com/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)

