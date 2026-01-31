from django import forms
from djcompanyatlas.models.virtuals.company import CompanyAtlasVirtualCompany

class CompanyAtlasVirtualCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyAtlasVirtualCompany
        fields = ["denomination", "reference", "backend", "address"]

        def create_company(self, backend: str | None = None, reference: str | None = None):
            company = create_company(
                backend=backend or self.cleaned_data["backend"],
                reference=reference or self.cleaned_data["reference"],
            )
            return company

            