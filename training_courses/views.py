from datetime import datetime, timedelta, date
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.detail import DetailView
from django.utils import timezone

import calendar
from training_courses.models import TrainingBooking, TrainingCourse, TrainingEvent, TrainingDays
from django.core import serializers
from .serializers import TrainingEventSerializer, TrainingDaysSerializer
from rest_framework.renderers import JSONRenderer
import json
import random
from django.contrib import messages
from .forms import TrainingBookingForm
from calendar import HTMLCalendar
from dateutil.relativedelta import relativedelta
import pytz


# handles booking for training.
class BookTraining(View, ContextMixin):
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        training_course = TrainingCourse.objects.get(pk=self.kwargs['pk'])
        context['course'] = training_course
      
        _year, _month = self.kwargs['year'], self.kwargs['month']

        curr_month = datetime(int(_year), int(_month), 1)
        prevdate = datetime(int(_year-1 if _month - 1 < 1 else _year ), int(12 if _month-1 < 1 else _month-1), 1)
        nextdate = datetime(int(_year+1 if _month + 1 > 12 else _year ), int(1 if _month+1 > 12 else _month+1), 1)
        
        context['prevdate'] = prevdate
        context['nextdate'] = nextdate
            
        _calendar = HTMLCalendar(firstweekday=6)
        context['calendar_dates'] = _calendar.itermonthdates(_year, _month)
        context['calendar'] = _calendar
        context['curr_month'] = curr_month
        context['trainingdates'] = TrainingDays.objects.filter(training_slot__month__gte=prevdate.month, training_slot__month__lte=nextdate.month, event__fully_booked=False, event__training_course=training_course)
        
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


# this view handles the actual booking process.
class Booking(View, ContextMixin):
    template_name ="booking.html"
    form_class = TrainingBookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utc = pytz.utc
        _date = utc.localize(datetime.strptime(self.kwargs['date'], "%Y-%m-%d"))
        context['date'] = _date
        context['datestr'] = self.kwargs['date']
        course = TrainingCourse.objects.get(pk=self.kwargs['pk'])
        context['course'] = course
        trdates = TrainingDays.objects.filter(training_slot__date=context['date'].date(), event__fully_booked=False)
        context['trdates'] = trdates
    
        bookingform = self.form_class(found_dates=trdates, course=course)
        context['bookingform'] = bookingform
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        trainingform = self.form_class(request.POST, found_dates=context['trdates'], course=context['course'])

        if trainingform.is_valid():
            eventpk = trainingform.cleaned_data['training_dates']
            times = trainingform.cleaned_data['times']
            event = TrainingEvent.objects.get(pk=eventpk)
            training_booking = TrainingBooking.objects.create(client=request.user, training_event=event, booking_id=random.randint(100000000000,999999999999), stime=times)
            return HttpResponseRedirect(reverse("booking-success", kwargs={'pk': training_booking.pk}))