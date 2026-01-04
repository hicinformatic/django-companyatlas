"""Manager for companyatlas providers."""

from typing import Any

from companyatlas.helpers import get_company_events
from virtualqueryset.managers import VirtualManager

class CompanyAtlasVirtualEventManager(VirtualManager):
    
