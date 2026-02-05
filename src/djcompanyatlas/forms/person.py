from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.person import CompanyAtlasPerson


class CompanyAtlasPersonForm(forms.ModelForm):
    """Form with radio buttons for choice fields."""

    officer_or_owner = forms.ChoiceField(
        choices=CompanyAtlasPerson._meta.get_field('officer_or_owner').choices,
        widget=forms.RadioSelect,
        label=_("Person Type"),
    )
    physical_or_moral = forms.ChoiceField(
        choices=CompanyAtlasPerson._meta.get_field('physical_or_moral').choices,
        widget=forms.RadioSelect,
        label=_("Physical or Moral"),
    )

    class Meta:
        model = CompanyAtlasPerson
        fields = '__all__'

