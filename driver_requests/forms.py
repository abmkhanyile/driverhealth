from django import forms
from .models import Driver_Request

# handles the creation of requests.
class DriverRequestForm(forms.ModelForm):
    class Meta:
        model = Driver_Request
        exclude = (
            'driver',
            'company',
            'req_id',
            'access_granted',
            'closed',
            'date_created',
        )
        fields = (
            'employment_type',
        )

        labels = {
            'employment_type': 'How do you want to employ this driver?'
        }

        widgets = {
            'employment_type': forms.RadioSelect(attrs={
                
            })
        }