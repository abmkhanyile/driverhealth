from django import forms

class PostTraining_Form(forms.Form):
    seldate = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date',
    }))
    seltime = forms.TimeField(required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control trtime',
        'type': 'time',
        'aria-describedby': 'button-addon2',
        # 'onchange': 'distime(this)',
    }))

