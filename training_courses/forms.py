from django import forms
from .models import TrainingEvent, TrainingBooking, TrainingTime, ElearningEnquiries, TrainingCourse



# this form handles the booking.
class TrainingBookingForm(forms.Form):
    def __init__(self, *args, found_dates, course, **kwargs):
        super(TrainingBookingForm, self).__init__(*args, **kwargs)
        events = []
        for date in found_dates:
            if date.event is not None and date.event.fully_booked == False and date.event.training_course == course:
                events.append(date.event)

        field_choices = []
        for event in events:
            dates_str = ''
            event_dates = event.training_event_dates.all()
            for d in event_dates:
                dates_str += '{}, '.format(d.training_slot)
            event_data = tuple((event.pk, dates_str))
            field_choices.append(event_data)
        self.fields['training_dates'].widget.choices = field_choices
        if course.hourly_training == True:
            self.fields['times'].queryset = found_dates[0].training_date_times.all()
            self.fields['times'].required = True
        
    training_dates = forms.IntegerField(widget=forms.RadioSelect(attrs={
        'onclick': 'getComments(this)',
    }))
    times = forms.ModelChoiceField(queryset=TrainingTime.objects.none(), empty_label="Choose Time Slot", required=False, widget=forms.Select(attrs={
        'class': 'form-control',
    }))


class ElearningForm(forms.ModelForm):
    class Meta:
        model = ElearningEnquiries
        fields = (
            'full_name',
            'contact_num',
            'email',
            'message',
        )
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'contact_num': forms.TextInput(attrs={
                'class': 'form-control'
            }),
             'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }


# this form handles the booking process for hourly trainings.
class TimeSelectionForm(forms.Form):
    time = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'timecb m-2',
        'onchange': 'display_tot()',
    }))
    timepk = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'time_pk',
    }))


