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
class ClientList(View, ContextMixin):
    template_name = "client-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = DHClient.objects.filter(user__is_active = True)
        
        paginator = Paginator(clients, 25) # Show 25 clients per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        context['stars_list'] = [1,2,3,4,5]

        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied
        context = self.get_context_data()
        return render(request, self.template_name, context)