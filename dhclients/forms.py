from django import forms
from .models import DHClient, ClientDocument, EmploymentHistory
from ckeditor.widgets import CKEditorWidget


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

# this form handles editing client details
class EditClientForm(forms.ModelForm):
    class Meta:
        model = DHClient
        exclude = (
            'date_created',
            'tested',
            'profile_picture',
            'rating',
            'dh_test_comment',
        )
        fields = '__all__'
        

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

CHOICES=[
   (True, 'Yes.'),
   (False, 'No'),        
]
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