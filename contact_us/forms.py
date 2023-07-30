from django import forms
from .models import ContactFormEnquiry

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormEnquiry
        exclude = (
            'date_created',
        )
        fields = '__all__'

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),          
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'contact_num': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control cf-textarea',
                'id': 'message',
            }),
        }

    