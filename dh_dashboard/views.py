from email import message
from mimetypes import init
from urllib import request
from xml.etree.ElementTree import Comment
from django import forms
from django.forms import DateTimeField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic import TemplateView
from training_courses.models import TrainingCourse, TrainingDays, TrainingEvent, TrainingTime, Training
from training_courses.views import BookTraining
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta, tzinfo
from django.contrib import messages
import pytz
from django.conf import settings
from django.forms import formset_factory, modelformset_factory, inlineformset_factory, BaseModelFormSet
from .forms import PostTraining_Form, RemarkForm, TimeSelectionForm, PostTrainingForm, Form1, Form2, Form3, Form4, Form5, Form6, Form7
from calendar import HTMLCalendar
from companies.views import ClientList
from dhclients.models import DHClient
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from countries.models import Country
from dhclients.views import ClinetProfile
from driver_requests.models import Driver_Request, RequestStatus
from driver_requests.forms import DRStatusForm
from formtools.wizard.views import SessionWizardView
from formtools import wizard



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

    

# driver list.
class DriverList(ClientList):
    template_name = "clientlist.html"

    def get(self, request, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        context = self.get_context_data()
        if 'country' in request.GET:
            country = Country.objects.get(pk=request.GET.get('country'))
            clients = DHClient.objects.filter(user__is_active = True, nationality=country)
            paginator = Paginator(clients, 25) # Show 25 clients per page.
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        return render(request, self.template_name, context)


# driver profile
class DProfile(ClinetProfile):
    template_name = "dhdriver-profile.html"

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context['remark_form'] = RemarkForm(initial={
            'star_rating': context['client'].rating,
            'remark': context['client'].dh_test_comment,
            'tested': context['client'].tested,
        })
        return render(request, self.template_name, context)


# add DH Remark and star rating
class AddRemark(View, ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = DHClient.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data()
        remark_form = RemarkForm(request.POST)
        if remark_form.is_valid():
            client = context['client']
            client.rating = remark_form.cleaned_data['star_rating']
            client.dh_test_comment = remark_form.cleaned_data['remark']
            client.tested = remark_form.cleaned_data['tested']
            client.save()

        messages.success(request, "DH Remarks added successfully...")
        return HttpResponseRedirect(reverse('driverprofile', kwargs={'pk': context['client'].pk}))


# this view displays all driver requests made made by companies.
class RequestedDrivers(View, ContextMixin):
    template_name = "requested-drivers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_reqs = Driver_Request.objects.all()
        paginator = Paginator(driver_reqs, 25) # Show 25 clients per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

# displays the actual request.
class DriverReq(View, ContextMixin):
    template_name = "driver-req.html"
    form_class = DRStatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req = Driver_Request.objects.get(pk=self.kwargs['pk'])
        context['req'] = req
        request_statuses = req.request_statuses.all()
      
        paginator = Paginator(request_statuses, 25) # Show 25 clients per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
     
        context['status_form'] = self.form_class()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        context = self.get_context_data()
        statusform = self.form_class(request.POST)

        if statusform.is_valid():
            status = statusform.save(commit=False)
            status.driver_req = context['req']
            status.save()
            messages.success(request, "Status captured successfully.")
            return HttpResponseRedirect(reverse("driver-req", kwargs={'pk': context['req'].pk}))

# accepts a driver request.
class AcceptRequest(View, ContextMixin):
    def get(self, request, **kwargs):
        if not request.user.is_staff == True:
            raise PermissionDenied
        req = Driver_Request.objects.get(pk=kwargs['pk'])
        req.access_granted = True
        req.save()
        RequestStatus.objects.create(status=8, driver_req=req)
        messages.success(request, "Request Accepted")
        return HttpResponseRedirect(reverse("driver-req", kwargs={'pk': req.pk}))


# accepts a driver request.
class RejectRequest(View, ContextMixin):
    def get(self, request, **kwargs):
        if not request.user.is_staff == True:
            raise PermissionDenied
        req = Driver_Request.objects.get(pk=kwargs['pk'])
        req.access_granted = False
        req.save()
        RequestStatus.objects.create(status=9, driver_req=req)
        messages.success(request, "Request Rejected")
        return HttpResponseRedirect(reverse("driver-req", kwargs={'pk': req.pk}))
        



# this view handles the act of posting a training session.
FORMS = [
    ("form1_template", Form1),
    ("form2_template", Form2),
    ("form3_template", Form3),
    ("form4_template", Form4),
    ("form5_template", Form5),
    ("form6_template", Form6),
    ("form7_template", Form7)
]

TEMPLATES = {
    '0': "post_training_forms/form1.html",
    '1': "post_training_forms/form2.html",
    '2': "post_training_forms/form3.html",
    '3': "post_training_forms/form4.html",
    '4': "post_training_forms/form5.html",
    '5': "post_training_forms/form6.html",
    '6': "post_training_forms/form7.html",
}

def skip_steps2_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return True
    else:
        return False

def skip_steps3_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return False
    else:
        return True


def skip_steps4_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return True
    else:
        return False

def skip_steps5_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return False
    else:
        return True

def skip_steps6_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return True
    else:
        return False

def skip_steps7_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    if cleaned_data.get('hr_training') == 1:
        return False
    else:
        return True

class PostTraingSession(SessionWizardView):
    success_pg = "training-post-success"
  
    seldates_formset = formset_factory(form=Form4)
    
    form_list = [
            Form1, 
            Form2, 
            Form3,
            formset_factory(form=Form4),
            Form5,
            formset_factory(form=Form6),
            formset_factory(form=Form7)
        ]
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        if self.steps.current == '1':        
            context['hourly_training_courses'] = TrainingCourse.objects.filter(hourly_training=True)    
            self.initial_dict = {
                '1': {'selected': True}
            }       
        return context


    def get_form_initial(self, step):  
        if step == '3':
            step3formdata = self.get_cleaned_data_for_step('1')
            datalist = []
            for course in step3formdata['selected']:
                datalist.append({'trcourse': course, 'hourly_limit': course.hourly_limit})
            self.initial_dict['3'] = datalist
            return self.initial_dict.get(step)
        elif step == '5':
            formdata_step3 = self.get_cleaned_data_for_step('3')
             
            datalist = []
            for fdata in formdata_step3:
                initdata_dict = {}
                
                stime = fdata['start_time']
                etime = fdata['end_time']
                trhr = datetime(day=stime.day, month=stime.month, year=stime.year, hour=stime.hour, minute=stime.minute, tzinfo=TIMEZONE)
                endtime = datetime(day=etime.day, month=etime.month, year=etime.year, hour=etime.hour, minute=etime.minute, tzinfo=TIMEZONE)

                times = [trhr]
                while trhr < endtime:
                    trhr += timedelta(hours=1)
                    times.append(trhr)
                initdata_dict['course'] = fdata['trcourse']
                initdata_dict['courseid'] = fdata['trcourse'].pk

                for i, time in enumerate(times):
                    initdata_dict['time{}'.format(i+1)] = time
                datalist.append(initdata_dict)
            self.initial_dict['5'] = datalist
            return self.initial_dict.get(step)
        elif step == '6':
            step5formdata = self.get_cleaned_data_for_step('4')
            sdate = step5formdata['start_date']
            edate = step5formdata['end_date']
            trainingdays_num = edate- sdate
           
            trdates = [{'trdate': sdate}]
            for i in range(trainingdays_num.days):
                trdates.append({'trdate': sdate+timedelta(i+1)})
            self.initial_dict['6'] = trdates
            return self.initial_dict.get(step)
        else:
            return self.initial_dict.get(step, {})


    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == '3':
            step3formdata = self.get_cleaned_data_for_step('1')
            selcourses_num = len(step3formdata['selected'])
            form.extra, form.max_num = selcourses_num, selcourses_num
        
        if step == '5':
            step3formdata = self.get_cleaned_data_for_step('1')
            selcourses_num = len(step3formdata['selected'])
            form.extra, form.max_num = selcourses_num, selcourses_num

        if step == '6':
            step5formdata = self.get_cleaned_data_for_step('4')
            sdate = step5formdata['start_date']
            edate = step5formdata['end_date']
            trainingdays_num = edate- sdate
            form.extra, form.max_num = trainingdays_num.days, trainingdays_num.days         

        return form

        

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    
    def done(self, form_list, form_dict, **kwargs):
        form1data = self.get_cleaned_data_for_step('0')
        if form1data['hr_training'] == 1:
            step3formset = form_dict['3']
            step6formset = self.get_cleaned_data_for_step('5')

            for form in step3formset:
                tr = form.save()
                for tform in step6formset:
                    if tr.trcourse.pk == tform['courseid']:
                        for key, value in tform.items():
                            if key.startswith("time") and value != '':
                                trtime = datetime.fromisoformat(value)
                                TrainingDays.objects.create(training_slot=trtime, selcourse=tr)
                
            return HttpResponseRedirect(reverse("training-post-success"))
        else:
            step6formset = self.get_cleaned_data_for_step('6')
            step2formset = self.get_cleaned_data_for_step('2')
            training = Training.objects.create(trcourse=step2formset['selcourse'], comment=step2formset['comment'])
            for form in step6formset:
                temptrdate = datetime.fromisoformat(form['trdate'])
                TrainingDays.objects.create(training_slot=temptrdate, selcourse=training)
            return HttpResponseRedirect(reverse("training-post-success"))

class TrainingPostSuccess(TemplateView):
    template_name = "training-post-success.html"



    
  