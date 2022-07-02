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
            'closing_date': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'jobclosing_date',
            })
        }

# collects data for a job application
class JobApplicationForm(forms.ModelForm):
    pass