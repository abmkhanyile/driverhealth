from django import forms
from .models import Driver_Request, RequestStatus

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

# handles the capturing of a request status.
class DRStatusForm(forms.ModelForm):

    class Meta:
        model = RequestStatus
        exclude = (
            'driver_req',
            'date_created',
        )
        fields = (
            'status',
            'note',
        )
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control status-dropdown',
                'id': 'statuses_id',
                'onchange': 'check_status(this)',
            }),
            'note': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'status-note',
                'disabled': True,
                'placeholder': 'Enter Request Status',
                'aria-label': "Recipient's username",
                'aria-describedby': "button-addon2",
            }),
        }
    