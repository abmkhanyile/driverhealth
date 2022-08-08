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
        )

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

# this form handles the booking.
class TrainingBookingForm(forms.ModelForm):
    class Meta:
        model = TrainingBooking
        exclude = (
            'date_created',
            'paid',
            'booking_id',
        )
        fields = (
            'training_event',
        )
