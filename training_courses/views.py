from datetime import datetime, timedelta, date
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.detail import DetailView
from django.utils import timezone

import calendar
from training_courses.models import TrainingBooking, TrainingCourse, BookingTransaction, TrainingEvent, TrainingDays, TrainingTime
from django.core import serializers
from .serializers import TrainingEventSerializer, TrainingDaysSerializer
from rest_framework.renderers import JSONRenderer
import json
import random
from django.contrib import messages
from .forms import TrainingBookingForm, ElearningForm, TimeSelectionForm
from calendar import HTMLCalendar
from dateutil.relativedelta import relativedelta
import pytz
import threading
from .notification_emails import booking_confirmation, elearning_enquiry_notification, booking_confirmation
from django.forms import formset_factory



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
        context['time_formset'] = formset_factory(TimeSelectionForm)
            
        _calendar = HTMLCalendar(firstweekday=6)
        calendar_dates = _calendar.itermonthdates(_year, _month)

        # events = TrainingEvent.objects.filter(fully_booked=False, training_course=training_course)

        # data = []
        # for date in calendar_dates:
        #     datestr = (date,)
        #     if events.exists():
        #         events_list = []
        #         for event in events:
        #             dates = event.training_event_dates.filter(training_slot=date)
        #             if len(dates) > 0:
        #                 events_list.append(event)
        #         data.append(datestr + (events_list,) + (dates,))
        #     else:
        #         data.append(datestr + () + ())
        
        # context['data'] = data              
        context['calendar_dates'] = _calendar.itermonthdates(_year, _month)
        
        context['calendar'] = _calendar
        context['curr_month'] = curr_month
        context['trainingdates'] = TrainingDays.objects.filter(training_slot__month__gte=prevdate.month, training_slot__month__lte=nextdate.month)
        
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

    # handles the process of booking for training.
    def post(self, request, **kwargs):
        context = self.get_context_data()
        trtime_formset =  formset_factory(TimeSelectionForm)
        trainingtime_formset = trtime_formset(request.POST)
        
        if trainingtime_formset.is_valid():
            btransaction = BookingTransaction.objects.create(trans_id=random.randint(100000000000,999999999999)) 
            booking_num = 0
            evnt = None

            for timeform in trainingtime_formset.cleaned_data:
                if timeform.get('time') == True:
                    trtime = TrainingTime.objects.get(pk=int(timeform.get('timepk')))
                    trdate = trtime.date
                    trevent = trdate.event
                    evnt = trevent

                    trbooking = TrainingBooking.objects.filter(client=request.user, training_event=trtime.date.event)
                    if trbooking.exists():
                        messages.warning(request, "You've already booked {} on {}".format(trtime, trtime.date))
                        return HttpResponseRedirect(reverse("book-training", kwargs={
                            'pk': context['course'].pk,
                            'month': context['curr_month'].month,
                            'year': context['curr_month'].year,
                        }))


                    if evnt.enrollees_num > 0:
                        evnt.enrollees_num -= 1
                        if evnt.enrollees_num == 0:
                            evnt.fully_booked = True
                        evnt.save()
                    TrainingBooking.objects.create(client=request.user, training_event=trevent, booking_transaction=btransaction, tdate=trdate, stime=trtime, paid=False)
                    booking_num += 1

            btransaction.trans_tot = booking_num * context['course'].price
            btransaction.save()
            email_thread = threading.Thread(target = booking_confirmation, args=[evnt.training_course, btransaction], daemon=True)
            email_thread.start()
            return HttpResponseRedirect(reverse("booking-success", kwargs={'pk': btransaction.pk}))
        else:
            print("form invalid")



class BookingSuccess(DetailView):
    template_name = "booking-success.html"
    model = BookingTransaction


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
        trdates = TrainingDays.objects.filter(training_slot=context['date'].date(), event__fully_booked=False)
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
            event = TrainingEvent.objects.get(pk=eventpk)
            if TrainingBooking.objects.filter(training_event=event, client=request.user).exists():
                messages.warning(request, "You've already booked this training.")
                return HttpResponseRedirect(reverse("booking", kwargs={'pk':context['course'].pk, 'date': context['datestr']}))

            if event.enrollees_num > 0 and event.fully_booked == False:
                btransaction = BookingTransaction.objects.create(trans_id=random.randint(100000000000,999999999999), trans_tot = context['course'].price) 
                TrainingBooking.objects.create(client=request.user, training_event=event, booking_transaction=btransaction)
                event.enrollees_num -= 1
                if event.enrollees_num == 0:
                    event.fully_booked = True
                event.save()
                email_thread = threading.Thread(target = booking_confirmation, args=[event.training_course, btransaction], daemon=True)
                email_thread.start()
                return HttpResponseRedirect(reverse("booking-success", kwargs={'pk': btransaction.pk}))
            


# handles the process of sending an elearning enquiry
class ElearningEnquiry(View, ContextMixin):
    template_name = "elearning-enquiry.html"
    form_class = ElearningForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = TrainingCourse.objects.get(pk=self.kwargs['course_id'])
        context['course'] = course
        context['form'] = self.form_class(initial={
            'message': 'Hi, I am interested in the course {}. Please contact me regarding this course.'.format(course)
        })
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        elearning_form = self.form_class(request.POST)
        if elearning_form.is_valid():
            el_enq = None
            if request.user is not None:
                el_enq = elearning_form.save(commit=False)
                el_enq.user = request.user
                el_enq.save()
            else:
                el_enq.save()
                
            email_thread = threading.Thread(target = elearning_enquiry_notification, args=[el_enq.full_name, el_enq.contact_num, el_enq.email, el_enq.message], daemon=True)
            email_thread.start()
            messages.success(request, "Enquiry sent succeccfully.")
            return HttpResponseRedirect(reverse('elearning-enquiry', kwargs={'course_id': self.kwargs['course_id']}))


# displays all courses on offer
class Courses(View, ContextMixin):
    template_name = "courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_course'] = TrainingCourse.objects.filter(elearning=False, thirdparty_course=False)
        context['code14courses'] = TrainingCourse.objects.filter(thirdparty_course=True)
        context['current_date'] = timezone.now()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# displays only hourly courses.
class HourlyCourses(View, ContextMixin):
    template_name = "hourly-courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hourly_courses'] = TrainingCourse.objects.filter(hourly_driving_course=True)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# displays only Multi-day courses.
class MultidayCourses(View, ContextMixin):
    template_name = "multiday-courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multiday_courses'] = TrainingCourse.objects.filter(multiday_course=True)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# handles the booking of elearning courses
class ElearningCourses(View, ContextMixin):
    template_name = "elearning-courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['elearning_courses'] = TrainingCourse.objects.filter(elearning_course=True)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())



# displays only Simulator courses.
class HourlySimulatorCourses(View, ContextMixin):
    template_name = "hourly-simulator-courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['simulator_courses'] = TrainingCourse.objects.filter(hourly_simulator_course=True)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# displays only Code 14 courses.
class Code14Courses(View, ContextMixin):
    template_name = "code14-courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code14_courses'] = TrainingCourse.objects.filter(code14_course=True)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# displays course details.
class CourseDetails(DetailView):
    template_name = "course-details.html"
    model = TrainingCourse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = context['current_date'] = timezone.now()
        return context



