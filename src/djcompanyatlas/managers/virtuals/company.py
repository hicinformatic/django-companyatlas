from typing import Any

from companyatlas.helpers import search_company, search_company_by_code
from virtualqueryset.managers import VirtualManager


class CompanyAtlasVirtualCompanyManager(VirtualManager):
    backend: str | None = None
    first: bool = False

    def __init__(self, query: str | None = None, code: str | None = None, **kwargs: Any):
        super().__init__()
        self.query = query
        self.code = code
        self.search_kwargs = kwargs
        self.first = kwargs.get("first", False)
        self.backend = kwargs.get("backend", None)
        self.attribute_search = kwargs.get("attribute_search", None)
        self._cached_data = None

    def get_data(self) -> list[Any]:
        if self._cached_data is not None:
            return self._cached_data

        if (not self.query and not self.code) or not self.model:
            self._cached_data = []
            return self._cached_data

        try:
            if self.backend:
                self.attribute_search = {"name": self.backend}
            if self.code:
                result = search_company_by_code(
                    self.code, first=self.first, attribute_search=self.attribute_search
                )
            else:
                result = search_company(
                    self.query, first=self.first, attribute_search=self.attribute_search
                )

            if isinstance(result, dict):
                results_list = []
                for provider_result in result.values():
                    if "result" in provider_result:
                        if isinstance(provider_result["result"], list):
                            results_list.extend(provider_result["result"])
                        else:
                            results_list.append(provider_result["result"])
                result = results_list

            if not isinstance(result, list):
                self._cached_data = []
                return self._cached_data

            objects = []
            for item in result:
                if isinstance(item, dict):
                    obj = self.model(**item)
                    objects.append(obj)
                elif isinstance(item, self.model):
                    objects.append(item)
            self._cached_data = objects
            return self._cached_data
        except Exception:
            self._cached_data = []
            return self._cached_data

    def search(self, query: str, first: bool = False, **kwargs: Any) -> Any:
        manager = CompanyAtlasVirtualCompanyManager(query=query, first=first, **kwargs)
        manager.model = self.model
        return manager.get_queryset()
