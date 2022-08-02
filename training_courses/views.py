from datetime import timedelta
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.utils import timezone
import calendar
from training_courses.models import TrainingCourse, TrainingEvent
from django.core import serializers
from .serializers import TrainingEventSerializer


# handles booking for training.
class BookTraining(View, ContextMixin):
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calender_days = []
        today = timezone.datetime.now()

        reqmonth = self.kwargs['month']
        reqyear = self.kwargs['year']
        if(today.month != reqmonth):
            if reqmonth == 0:
                reqmonth = 12
                today = today.replace(year=reqyear-1, month=reqmonth)
            elif reqmonth == 13:
                reqmonth = 1
                today = today.replace(year=reqyear+1, month=reqmonth)
            else:
                today = today.replace(year=reqyear, month=reqmonth)
            
        
        first_day_of_the_month = today.replace(day=1)        
        year, month = today.year, today.month
        last_day_of_the_month = calendar.monthrange(year, month)[1]

        weekday = first_day_of_the_month.weekday()
   
        for day in range(1, last_day_of_the_month+1, 1):
            calender_days.append(day)

        while weekday != 6:
            first_day_of_the_month = first_day_of_the_month-timedelta(days=1)
            calender_days.insert(0, first_day_of_the_month.day)
            weekday = first_day_of_the_month.weekday()
            
        next_month_days = 1    
        for day in range(len(calender_days)+1, 43, 1):
            calender_days.append(next_month_days)   
            next_month_days += 1

        context['calender_days'] = calender_days    
        context['calendar_month'] = today
       
        context['prev_month'] = today.month - 1
        context['next_month'] = today.month + 1
        context['course'] = TrainingCourse.objects.get(pk=self.kwargs['pk'])
        context['training_events'] = serializers.serialize("json", TrainingEvent.objects.all())
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())



