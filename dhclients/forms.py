from django import forms
from .models import DHClient



# this form collect client details on registration.
class DHClientRegForm(forms.ModelForm):
    class Meta:
        model = DHClient
        exclude = (
            'user',
            'rating',
            'dh_test_comment',
            'tested',
            'has_passport',
            'passport_num',
            'date_created',
        )
        fields = (
            'nationality',
            'location',
            'postal_code',          
        )
       

        widgets = {
            'nationality': forms.Select(attrs={
                'class': 'form-control',
                'id': 'country',
                'onchange': 'get_geo_layout(this)',
                'data-layout': 'COUNTRY',
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'origin',
            }),

            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
          
     
            
        }

