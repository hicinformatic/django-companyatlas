from typing import Any

from companyatlas.helpers import search_company, search_company_by_reference
from djproviderkit.managers import BaseServiceProviderManager


class CompanyAtlasVirtualCompanyManager(BaseServiceProviderManager):
    """Manager for company search from companyatlas."""

    _commands = {
        'search_company': search_company,
        'search_company_by_reference': search_company_by_reference,
    }

    _args_available = ['query', 'code', 'first', 'backend']

    def search_company(self, query: str, first: bool = False, **kwargs: Any) -> Any:
        return self.get_queryset_command('search_company', query=query, first=first, **kwargs)

    def search_company_by_reference(self, code: str, **kwargs: Any) -> Any:
        code = code.split("_")
        print(code)
        reference = code[-1]
        backend = "_".join(code[:-1])
        return self.get_queryset_command(
            'search_company_by_reference',
            code=reference,
            attribute_search={"name": backend}, 
            **kwargs)

    def get_data(self) -> Any:
        if not self.query and not self.code:
            return []
        command = self._command
        kwargs = {
            "first": self.first,
            "attribute_search": self.attribute_search,
        }
        if self.backend:
            kwargs["attribute_search"] = {"name": self.backend}
        if command == "search_company_by_reference":
            if not self.code:
                return self.queryset_class(model=self.model, data=[])
            kwargs["code"] = self.code
        else:
            if not self.query:
                return self.queryset_class(model=self.model, data=[])
            kwargs["query"] = self.query
        return self.get_queryset_command(command, **kwargs)
