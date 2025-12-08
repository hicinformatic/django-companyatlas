# Exemples d'utilisation

## Insertion de données par pays

### Exemple 1 : Insertion simple

```python
from companyatlas.helpers import create_or_update_company_data

# Créer une entreprise avec une dénomination
company, data = create_or_update_company_data(
    country="FR",
    data_type="denomination",
    value="Tour Eiffel",
    company_name="Tour Eiffel"
)

# Ajouter un SIREN
company, data = create_or_update_company_data(
    country="FR",
    data_type="siren",
    value="123456789",
    company=company
)

# Ajouter un RNA
company, data = create_or_update_company_data(
    country="FR",
    data_type="rna",
    value="W12345678",
    company=company
)
```

### Exemple 2 : Insertion en masse

```python
from companyatlas.helpers import bulk_create_company_data

# Créer une entreprise avec plusieurs données
company = bulk_create_company_data([
    ("FR", "denomination", "Tour Eiffel"),
    ("FR", "siren", "123456789"),
    ("FR", "siret", "12345678901234"),
    ("FR", "rna", "W12345678"),
    ("FR", "ape", "6201Z"),
    ("FR", "legal_form", "SARL"),
])
```

### Exemple 3 : Recherche par données

```python
from companyatlas.helpers import get_company_by_country_data

# Trouver une entreprise par SIREN
company = get_company_by_country_data("FR", "siren", "123456789")

# Trouver une entreprise par RNA
company = get_company_by_country_data("FR", "rna", "W12345678")
```

## Utilisation des modèles directement

### Accès aux données

```python
from companyatlas.models import Company, CompanyData, CompanyCountryData

# Créer une entreprise
company = Company.objects.create(
    name="Tour Eiffel",
    country="FR"
)

# Ajouter des données flexibles
data1 = CompanyData.objects.create(
    company=company,
    country="FR",
    data_type="denomination",
    value_type="str",
    value="Tour Eiffel"
)

data2 = CompanyData.objects.create(
    company=company,
    country="FR",
    data_type="capital",
    value_type="float",
    value="100000.50"
)

# Ou utiliser set_value() pour détection automatique
data3 = CompanyData.objects.create(
    company=company,
    country="FR",
    data_type="employees"
)
data3.set_value(150)  # Détecte automatiquement le type "int"
data3.save()

# Ajouter des données structurées
country_data, created = CompanyCountryData.objects.get_or_create(
    company=company,
    country="FR",
    defaults={
        "siren": "123456789",
        "siret": "12345678901234",
        "rna": "W12345678",
        "ape": "6201Z",
        "legal_form": "SARL",
    }
)

# Accéder aux données (retourne la valeur convertie au bon type)
print(company.get_data_value("FR", "denomination"))  # "Tour Eiffel" (str)
print(company.get_data_value("FR", "capital"))      # 100000.50 (float)
print(company.get_data_value("FR", "employees"))    # 150 (int)
print(company.get_data_value("FR", "metadata"))      # {"key": "value"} (dict)

# Accéder aux données structurées
print(company.get_country_data("FR").siren)   # "123456789"

# Définir une valeur (détection automatique du type)
company.set_data_value("FR", "denomination", "Nouvelle dénomination")  # str
company.set_data_value("FR", "capital", 200000.75)  # float
company.set_data_value("FR", "employees", 200)  # int
company.set_data_value("FR", "tags", ["tech", "startup"])  # json
```

## Structure des données

### Modèle Company (données internationales)
- `name` : Nom de l'entreprise
- `domain` : Domaine (optionnel)
- `vat_number` : Numéro de TVA international
- `country` : Code pays ISO
- `founded_year`, `employee_count`, `industry`, etc.

### Modèle CompanyData (données flexibles)
- `company` : Référence à Company
- `country` : Code pays (FR, US, GB, etc.)
- `data_type` : Type de donnée (denomination, siren, rna, etc.)
- `value` : Valeur de la donnée

### Modèle CompanyCountryData (données structurées)
- `company` : Référence à Company
- `country` : Code pays
- `siren`, `siret`, `rna`, `ape`, `legal_form`, `rcs` : Champs français
- `extra_data` : JSON pour données supplémentaires

## Types de valeurs supportés

Le champ `value_type` peut être :
- `str` : Chaîne de caractères (par défaut)
- `int` : Nombre entier
- `float` : Nombre décimal
- `json` : Objet JSON (dict ou list)

Le champ `data_type` est libre (CharField) - vous pouvez utiliser n'importe quel nom :
- `denomination`, `siren`, `siret`, `rna`, `ape`, `legal_form`, `rcs`
- `capital`, `employees`, `revenue`, `profit`
- `metadata`, `tags`, `categories`
- etc.

### Exemples avec différents types

```python
# String
create_or_update_company_data("FR", "denomination", "Tour Eiffel")

# Integer
create_or_update_company_data("FR", "employees", 150)

# Float
create_or_update_company_data("FR", "capital", 100000.50)

# JSON
create_or_update_company_data("FR", "metadata", {"key": "value", "tags": ["tech", "startup"]})
```

