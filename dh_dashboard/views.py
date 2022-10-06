from email import message
from django.forms import DateTimeField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from training_courses.models import TrainingCourse, TrainingDays, TrainingEvent, TrainingTime
from training_courses.views import BookTraining
from django.utils import timezone
from django.urls import reverse
from training_courses.forms import PostTrainingForm
from datetime import datetime
from django.contrib import messages
import pytz
from django.conf import settings
from django.forms import formset_factory
from .forms import PostTraining_Form

TIMEZONE  = pytz.timezone(settings.TIME_ZONE)


class DHDashboard(View, ContextMixin):
    template_name = "dhdashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

# handles the process of posting a training event.
class SelectPackage(View, ContextMixin):
    template_name = "select-package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = TrainingCourse.objects.all()
        context['today'] = timezone.now()
        return context
        
    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())



class PostTraining(BookTraining, ContextMixin):
    template_name = "post-training.html"
    form_class = PostTrainingForm

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['training_form'] = self.form_class()    
        context['training_dates_formset'] = formset_factory(PostTraining_Form)            
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        trainingdates = request.POST.getlist('trainingdate')
        training_form = self.form_class(request.POST)
        training_date_formset =  formset_factory(PostTraining_Form)
        trainingdate_formset = training_date_formset(request.POST)

        if training_form.is_valid() and trainingdate_formset.is_valid():
            training_event = training_form.save(commit=False)
            training_event.training_course = context['course']
                        
            training_event.save()

            date_objs = set()
            for dateform in trainingdate_formset.cleaned_data:
                if dateform.get('seldate') is not None or dateform.get('seltime') is not None:
                    date_objs.add(dateform.get('seldate'))
           
            data = {}
            for date_obj in date_objs:
                data.update({date_obj: set()})
     
            for dateform in trainingdate_formset.cleaned_data:
                if dateform.get('seltime') is not None:
                    data[dateform.get('seldate')].add(dateform.get('seltime'))
            
            for key, value in data.items():
                trday = TrainingDays.objects.create(training_slot=key, event=training_event)
                for time in value:
                    trtime = TrainingTime.objects.create(time_slot=time, date=trday)

            messages.success(request, "Training event successfully created.")
            return HttpResponseRedirect(reverse('post-training', kwargs={
                'pk': context['course'].pk,
                'month': context['curr_month'].month,
                'year': context['curr_month'].year,
            }))
        else:
            print("no valid form")

    

