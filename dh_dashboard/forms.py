from cProfile import label
from email.policy import default
from random import choices
from django import forms
from training_courses.models import TrainingCourse, TrainingDays, TrainingEvent, Training


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


class PostTrainingForm(forms.ModelForm):
    class Meta:
        model = TrainingEvent
        exclude = (
            'training_course',
            'slots',
            'date_created',
        )
        fields = (
            
        )


# form 1 of the multi-step form for creating a training session post.
class Form1(forms.Form):
    HOURLY_TRAINING = [
        (1, "Yes"),
        (2, "No")
    ]
    hr_training = forms.IntegerField(required=True, label="Are you posting an hourly training session?", widget=forms.RadioSelect(
        choices=HOURLY_TRAINING,
    ))


# this forms displays the different types of all hourly courses.
class Form2(forms.Form):
    selected = forms.ModelMultipleChoiceField(queryset=TrainingCourse.objects.filter(hourly_training=True), widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'forms-control',
    }))
  


# displays all the non-hourly courses.
class Form3(forms.Form):
    selcourse = forms.ModelChoiceField(queryset=TrainingCourse.objects.filter(hourly_training=False), widget=forms.RadioSelect(attrs={
        'class': 'form.control',
    }))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

class Form4(forms.ModelForm):
    seldate_time = forms.DateTimeField(required=True, label="Training Date", widget=forms.DateTimeInput(attrs={
        'class': 'form-control trdate',
        'type': 'date',
        'onchange': 'populate_date(this)'
    }))
    start_time = forms.DateTimeField(required=True, label="Start Time", widget=forms.DateTimeInput(attrs={
        'class': 'form-control stime',
        'type': 'datetime-local',
    }))
    end_time = forms.DateTimeField(required=True, label="End Time", widget=forms.DateTimeInput(attrs={
        'class': 'form-control etime',
        'type': 'datetime-local',
    }))
    class Meta:
        model = Training
        exclude = (
            'enrollees_num',
        )
        fields = (
            'trcourse',
            'hourly_limit',
            'comment',
        )
        widgets = {
            'trcourse': forms.Select(attrs={
                'class': 'form-control',
            }),
            'hourly_limit': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
    
    


class Form5(forms.Form):
    start_date = forms.DateTimeField(required=True, label="Start Date", widget=forms.DateTimeInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local',
    }))
    end_date = forms.DateTimeField(required=True, label="End Date", widget=forms.DateTimeInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local',
    }))


# this is a confirmation form for the hourly training post.
class Form6(forms.Form):
    course = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    courseid = forms.IntegerField(widget=forms.HiddenInput())
    time1 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time2 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time3 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time4 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time5 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time6 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time7 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time8 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time9 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))
    time10 = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))




 
class Form7(forms.Form):
    trdate = forms.CharField(required=False, widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',
    }))

    







# this form handles the booking process for hourly trainings.
class TimeSelectionForm(forms.Form):
    time = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'timecb m-2',
        'onchange': 'display_tot()',
    }))
    timepk = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'time_pk',
    }))



