from datetime import timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.detail import DetailView
from django.utils import timezone
import calendar
from training_courses.models import TrainingBooking, TrainingCourse, TrainingEvent
from django.core import serializers
from .serializers import TrainingEventSerializer, TrainingDaysSerializer
from rest_framework.renderers import JSONRenderer
import json
import random
from django.contrib import messages
from .forms import TrainingBookingForm


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
        training_course = TrainingCourse.objects.get(pk=self.kwargs['pk'])
        context['course'] = training_course
        training_events = TrainingEvent.objects.filter(training_course = training_course, fully_booked=False)
        data = serializers.serialize('json', training_events, use_natural_foreign_keys=True, indent=4)
        context['training_events'] = json.dumps(data, separators=(',', ':'))
        context['booking_form'] = TrainingBookingForm(initial={
            'training_dates': training_events,
        })
       
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        if 'training_event' in request.GET:
            eventpk = request.GET['training_event']
            event = TrainingEvent.objects.get(pk=eventpk)
            user = request.user

            if user.dhclient in event.enrollees.all():
                messages.warning(request, "You've already booked training for this course")
                return HttpResponseRedirect(reverse("book-training", kwargs={'pk': context['course'].pk, 'month': context['calendar_month'].month, 'year': context['calendar_month'].year}))
            
            enrollees_num = event.enrollees_num
            training_booking = TrainingBooking.objects.create(client=user, training_event=event, booking_id=random.randint(100000000,999999999))
            
            if enrollees_num > 0:
                enrollees_num -= 1
                event.enrollees_num = enrollees_num
                if enrollees_num == 0:
                    event.fully_booked = True
                event.save()
                event.enrollees.add(user.dhclient)
            return HttpResponseRedirect(reverse("booking-success", kwargs={'pk': training_booking.pk}))
        return render(request, self.template_name, self.get_context_data())



class BookingSuccess(DetailView):
    template_name = "booking-success.html"
    model = TrainingBooking


class GetTimes(View):
    def get(self, request, **kwargs):
        if 'date' in request.GET:
            print(request.GET['date'])

    def post(self, request, **kwargs):
        date = request.POST.get('date')
        print(date)


