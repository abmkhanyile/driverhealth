from urllib import response
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.core.exceptions import PermissionDenied
from careers.forms import CreateJobForm
import random
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from dhclients.models import DHClient
from django.core.paginator import Paginator
from careers.models import Job
from .forms import ClientFilterForm
from countries.models import Country
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings


class Dashboard(View, ContextMixin):
    template_name = "company-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        context['company'] = company
        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())


# handles the process of posting a job opening
class CreateJob(View, ContextMixin):
    template_name = "create-job.html"
    form_class = CreateJobForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobform'] = self.form_class()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        jobform = self.form_class(request.POST)
        if jobform.is_valid():
            job = jobform.save(commit=False)
            job.owner = request.user.company
            job.dhref = random.randint(100000000000,999999999999)
            job.save()
            messages.success(request, "Job successfully created...awaiting approval by DriverHealth")
            return HttpResponseRedirect(reverse('create-job'))



# displays a list of all the drivers.
@method_decorator(csrf_exempt, name='dispatch')
class ClientList(View, ContextMixin):
    template_name = "client-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = DHClient.objects.filter(user__is_active = True)
        
        paginator = Paginator(clients, 25) # Show 25 clients per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['countries'] = Country.objects.all()
        context['stars_list'] = [1,2,3,4,5]
        context['filterform'] = ClientFilterForm()

        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
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

    def post(self, request, **kwargs):
        context = self.get_context_data()
        filterform = ClientFilterForm(request.POST)
        if filterform.is_valid():
            search_term = filterform.cleaned_data['search_field']
            place_id = filterform.cleaned_data['placeid']

            location_data = None
            if place_id is not None:
                location_data = self.getDetailedLocations(placeid=place_id)

            db_regions = ['locality', 'sublocality', 'country', 'administrative_area_level_1', 'administrative_area_level_2']

            searchterm = {}
            
            if location_data is not None:
                for addr_comp in location_data['result']['address_components']:  
                    region_type = list(set(db_regions) & set(addr_comp['types']))
                    if len(region_type) > 0:
                        searchterm.update({region_type[0]: addr_comp['long_name']})
                    else:
                        continue

            clients = None
            if len(searchterm) > 0:
                clients = DHClient.objects.filter(**searchterm)
            else:
                clients = DHClient.objects.filter(user__is_active = True)
            
            paginator = Paginator(clients, 25) # Show 25 clients per page.
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            
            return render(request, self.template_name, context)

    def getDetailedLocations(self, placeid):
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}".format(placeid, settings.GOOGLE_MAPS_API)

        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        # print(data)
        return data

# displays a list of all the jobs posted by a company.
class PostedJobs(View, ContextMixin):
    template_name = "posted-jobs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = self.request.user.company
        postedjobs = company.company_jobs.all()
        paginator = Paginator(postedjobs, 25) # Show 25 jobs per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())


# displays a job and all the applicants of that job.
# this is in the company Dashboard.
class JobApplicants(View, ContextMixin):
    template_name = "applicants.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = Job.objects.get(pk=self.kwargs['pk'])
        context['job'] = job
        context['stars_list'] = [1,2,3,4,5]
        context['applications'] = job.job_applications.all()
        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())

