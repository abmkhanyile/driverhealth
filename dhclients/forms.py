from django import forms
from .models import DHClient, ClientDocument, EmploymentHistory
from ckeditor.widgets import CKEditorWidget


CHOICES=[
   (True, 'Yes.'),
   (False, 'No'),        
]

# this form collect client details on registration.
class DHClientRegForm(forms.ModelForm):
    placeid = forms.CharField(required=False, widget=forms.HiddenInput(attrs={
        'id': 'placeid',
    }))
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
                'id': 'places_search_field',
            }),           
        }

# this form handles editing client details
class EditClientForm(forms.ModelForm):
    class Meta:
        model = DHClient
        exclude = (
            'user',
            'date_created',
            'tested',
            'profile_picture',
            'rating',
            'dh_test_comment',
        )
        fields = '__all__'

        labels = {
            'crossborder': 'Are you willing to do crossborder work?',
            'in_job_market': 'Are you actively looking for a job?',
            'has_passport': 'Do you have a passport?',
            'passport_num': 'What is your passport number?'
        }

        widgets = {
            'nationality': forms.Select(attrs={
                'class': 'form-control',
            }),  
            'has_passport': forms.RadioSelect(
                choices=CHOICES
            ),  
            'passport_num': forms.TextInput(attrs={
                'class': 'form-control',
            }),  
            'crossborder': forms.RadioSelect(
                choices=CHOICES
                ),  
            'location': forms.TextInput(attrs={
                'class': 'form-control',
            }),  
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),  
            'in_job_market': forms.RadioSelect(
                choices=CHOICES
                ),  
        }
        

# handles the upload of driver documents.
class ClientDocForm(forms.ModelForm):
    class Meta:
        model = ClientDocument
        exclude = (
            'client',
        )
        fields = (
            'doc_type',
            'other_type',
            'document',
        )
        labels = {
            'other_type': 'Specify Document Type',
            'doc_type': 'Document Type',
            'document': 'Select document (i.e. 5MB size limit)',
        }
        widgets = {
            'document': forms.ClearableFileInput(attrs={
                'class': 'form-control clientdoc-fileinput',
            }),
            'doc_type': forms.Select(attrs={
                'class': 'form-control client-doctype',
                'onchange': 'checkSel(this)',
            }),
            'other_type': forms.TextInput(attrs={
                'class': 'form-control client-otherdoctype',
                'id': "othertype",
                'placeholder': 'Please specify the type of document',
            }),
        }


# collects data of previous work experience.
class EmploymentHistoryForm(forms.ModelForm):
    duties = forms.CharField(widget=CKEditorWidget(attrs={
        'class': 'form-control',
    }))
    contact_permission = forms.BooleanField(required=False, label="Do you give permission to contact this person?", widget=forms.RadioSelect(
        choices=CHOICES
    ))
    class Meta:
        model = EmploymentHistory
        exclude = (
            'dhclient',
            'creation_date',
        )
        fields = '__all__'

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control startdate'
            }),
             'end_date': forms.DateInput(attrs={
                'class': 'form-control enddate'
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control'
            }),
             'contact_person': forms.TextInput(attrs={
                'class': 'form-control'
            }),
             'contact_num': forms.TextInput(attrs={
                'class': 'form-control'
            }),
             'contact_permission': forms.RadioSelect(attrs={
                'class': 'form-control'
            }),
            
        }