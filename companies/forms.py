from django import forms
from .models import Company
from countries.models import Country

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


# this form is for filtering drivers by location.
class ClientFilterForm(forms.Form):
    search_field = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'places_search_field',
        'placeholder': 'Filter by DriverHealth ID or Location',
        'aria-label': 'Filter by DriverHealth ID or Location',
        'aria-describedby': 'basic-addon2'
    }))
    placeid = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'placeid',
    }))
    locality = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'locality',
    }))
    sublocality = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'sublocality',
    }))
    country = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'country',
    }))
    administrative_area_level_1 = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'administrative_area_level_1',
    }))
    administrative_area_level_2 = forms.CharField(max_length=150, required=False, widget=forms.HiddenInput(attrs={
        'id': 'administrative_area_level_2',
    }))





