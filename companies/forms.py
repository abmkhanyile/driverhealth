from django import forms
from .models import Company

# this form collects data for a company registration.
class CompanyRegForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = (
            'creation_date',
            'note',
        )
        fields = (
            'company_name',
            'company_reg_num',
            'vat_num',
            'contact_person',
            'contact_num1',
            'contact_num2',
            'email_address',
            'address',
            'country',
        )

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'company_reg_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'vat_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_num1': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_num2': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'country': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
