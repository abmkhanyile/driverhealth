from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Job
from django.core.paginator import Paginator


# displays a job and click to apply
class JobView(DetailView):
    template_name = "job.html"
    model = Job
    
# displays a list of all the available jobs.
class JobList(View, ContextMixin):
    template_name = "jobs-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        jobs = Job.objects.filter(active_listing=True)
        context = self.get_context_data()
        paginator = Paginator(jobs, 25) # Show 25 jobs per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return render(request, self.template_name, context)



