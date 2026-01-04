"""Manager for companyatlas providers."""

from typing import Any

from companyatlas.helpers import get_company_documents
from virtualqueryset.managers import VirtualManager

class CompanyAtlasVirtualDocumentManager(VirtualManager):
    
