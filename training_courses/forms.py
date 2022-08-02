from django import forms
from .models import TrainingEvent

class PostTrainingForm(forms.ModelForm):
    training_slots = forms.CharField(max_length=1500, required=False, widget=forms.HiddenInput(attrs={
        'id': 'dates_input',
    }))
    class Meta:
        model = TrainingEvent
        exclude = (
            'training_course',
            'slots',
            'date_created',
            'enrollees',
        )
        fields = (
            'comment',
        )

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }