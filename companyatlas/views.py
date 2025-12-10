"""Views for companyatlas app."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Company


def company_list(request):
    """List all companies."""
    companies = Company.objects.all()
    context = {
        "companies": companies,
    }
    return render(request, "companyatlas/company_list.html", context)


def company_detail(request, pk):
    """Show company details."""
    company = get_object_or_404(Company, pk=pk)
    context = {
        "company": company,
    }
    return render(request, "companyatlas/company_detail.html", context)


def company_enrich(request, pk):
    """Trigger company enrichment."""
    company = get_object_or_404(Company, pk=pk)

    if request.method == "POST":
        if company.enrich(force=True):
            messages.success(request, f"Successfully enriched {company.name}")
        else:
            messages.error(request, f"Failed to enrich {company.name}")
        return redirect("companyatlas:company-detail", pk=pk)

    return render(request, "companyatlas/company_enrich.html", {"company": company})
