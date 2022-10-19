from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from dhclients.models import DHClient
from driver_requests.models import Driver_Request, RequestStatus
from .forms import DriverRequestForm
import random
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


# handles the process of requesting a driver.
class RequestDriver(View, ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['driver'] = DHClient.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, **kwargs):
        context = self.get_context_data()
        reqform = DriverRequestForm(request.POST)
    
        driver_req = Driver_Request.objects.filter(driver=context['driver'], company=request.user.company, closed=False)
        
        # checks if there isn't an existing request on the system.
        if driver_req.exists():
            messages.warning(request, "You already have an active request for this driver.")
            return HttpResponseRedirect(reverse("clientprofile", kwargs={'pk': context['driver'].pk}))

        if reqform.is_valid():
            dreq = reqform.save(commit=False)
            dreq.driver = context['driver']
            dreq.company = request.user.company
            dreq.req_id = random.randint(100000000000,999999999999)
            dreq.save()
            RequestStatus.objects.create(status=1, driver_req=dreq)
            messages.success(request, "Your request was sent successfully.")
            return HttpResponseRedirect(reverse("clientprofile", kwargs={'pk': context['driver'].pk}))

    



    
