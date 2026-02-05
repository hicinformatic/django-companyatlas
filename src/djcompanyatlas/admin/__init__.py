from .company import CompanyAtlasCompanyAdmin
from .data import CompanyAtlasDataAdmin
from .address import CompanyAtlasAddressAdmin
from .document import CompanyDocumentAdmin
from .event import CompanyEventAdmin
from .person import CompanyAtlasPersonAdmin
from .referentiel import CompanyAtlasReferentielAdmin
from .virtuals.provider import CompanyAtlasProviderModel
from .virtuals.company import CompanyAtlasVirtualCompanyAdmin
from .virtuals.document import CompanyAtlasVirtualDocumentAdmin
from .virtuals.event import CompanyAtlasVirtualEventAdmin

__all__ = [
    "CompanyAtlasCompanyAdmin",
    "CompanyAtlasDataAdmin",
    "CompanyAtlasAddressAdmin",
    "CompanyDocumentAdmin",
    "CompanyEventAdmin",
    "CompanyAtlasPersonAdmin",
    "CompanyAtlasReferentielAdmin",
    "CompanyAtlasProviderModel",
    "CompanyAtlasVirtualCompanyAdmin",
    "CompanyAtlasVirtualDocumentAdmin",
    "CompanyAtlasVirtualEventAdmin",
]

