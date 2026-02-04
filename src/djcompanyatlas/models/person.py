
from django.db import models
from django.utils.translation import gettext_lazy as _

from .company import CompanyAtlasCompany
from .source import CompanyAtlasSourceBase

class CompanyAtlasPerson(CompanyAtlasSourceBase):
    """Company officers and owners from various backends."""
    company = models.ForeignKey(
        CompanyAtlasCompany,
        on_delete=models.CASCADE,
        related_name="to_companyatlasperson",
        verbose_name=_("Company"),
        help_text=_("Company this person belongs to"),
    )

    officer_or_owner = models.CharField(
        max_length=100,
        verbose_name=_("Person Type"),
        help_text=_("Type of person (officer, owner)"),
        choices=[
            ("officer", _("Officer")),
            ("owner", _("Ultimate Beneficial Owner")),
        ],
    )
    physical_or_moral = models.CharField(
        max_length=100,
        verbose_name=_("Physical or Moral"),
        help_text=_("Physical or moral person"),
        choices=[
            ("physical", _("Physical")),
            ("moral", _("Moral")),
        ],
    )
    is_joint_ownership = models.BooleanField(
        default=False,
        verbose_name=_("Is joint ownership"),
        help_text=_("Whether the person is a joint owner (held in indivision)"),
    )

    # Moral person
    denomination = models.CharField(
        max_length=100,
        verbose_name=_("Denomination"),
        help_text=_("Denomination of the person"),
    )
    code = models.CharField(
        max_length=100,
        verbose_name=_("Code"),
        help_text=_("Code of the person"),
    )

    # Physical person
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First Name"),
        help_text=_("First name of the person"),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last Name"),
        help_text=_("Last name of the person"),
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Birth Date"),
        help_text=_("Birth date of the person"),
    )

    class Meta:
        verbose_name = _("Company Person")
        verbose_name_plural = _("Company Persons")
        indexes = [
            models.Index(fields=["company", "officer_or_owner", "physical_or_moral"]),
        ]
        ordering = ["officer_or_owner", "physical_or_moral", "-created_at"]

    @property
    def full_name(self):
        if self.physical_or_moral == "physical":
            return f"{self.first_name} {self.last_name}"
        return self.denomination

    def __str__(self):
        return f"{self.company.denomination} - {self.officer_or_owner} - {self.physical_or_moral}"
        