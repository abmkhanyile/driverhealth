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
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        trainingdates = request.POST.getlist('trainingdate')
        training_form = self.form_class(request.POST)
        print(trainingdates)
        
        if training_form.is_valid():
            training_event = training_form.save(commit=False)
            training_event.training_course = context['course']
            
            training_event.save()

            for datestr in trainingdates:
                datestr_list = datestr.split(',')
                training_date = TrainingDays.objects.create(training_slot=datetime.strptime(datestr_list[0].strip(), "%Y-%m-%d"), event=training_event)
                if len(datestr_list) > 1:
                    for timestr in datestr_list[1:]:
                       time = TrainingTime.objects.create(time_slot=datetime.strptime(datestr_list[0]+timestr, "%Y-%m-%d%H:%M"), date=training_date)

            messages.success(request, "Training event successfully created.")
            return HttpResponseRedirect(reverse('post-training', kwargs={
                'pk': context['course'].pk,
                'month': context['calendar_month'].month,
                'year': context['calendar_month'].year,
            }))

    

