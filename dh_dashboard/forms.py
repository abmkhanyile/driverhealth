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


# remark form and star rating
class RemarkForm(forms.Form):
    STAR_RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    star_rating = forms.IntegerField(required=False, label="Star Rating", widget=forms.Select(
        choices=STAR_RATING,
        attrs={
        'class': 'form-control',
    }))
    remark = forms.CharField(required=False, label="DH Remarks", widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))
    tested = forms.BooleanField(required=False, label="Driver Tested?", widget=forms.CheckboxInput(attrs={
        
    }))

