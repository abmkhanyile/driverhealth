from django import forms
from .models import Job
from ckeditor.widgets import CKEditorWidget


class CreateJobForm(forms.ModelForm):
    job_details = forms.CharField(widget=CKEditorWidget(attrs={
        'class': 'form-control',
    }))
    class Meta:
        model = Job
        fields = (
            'job_title',
            'ref',
            'job_location',
            'job_details',
            'closing_date',
        )
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'ref': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'job_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type in City, Town, or Province'
            }),
            'closing_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'jobclosing_date',
            })
        }

# collects data for a job application
class JobApplicationForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    surname = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    