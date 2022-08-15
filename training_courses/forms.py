from django import forms
from .models import TrainingEvent, TrainingBooking

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
            'enrollees_num',
        )

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'enrollees_num': forms.NumberInput(attrs={
                'class': 'form-control',
            })
        }

# this form handles the booking.
class TrainingBookingForm(forms.Form):
    TRAINING_EVENTS = []
    # training_dates = forms.ModelChoiceField(queryset=TrainingEvent.objects.none(), empty_label="", widget=forms.RadioSelect(attrs={
    #     # 'class': 'form-control',
    # }))
    times = forms.IntegerField(required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))

