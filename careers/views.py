from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import ApplicationDocument, Job, JobApplication
from django.core.paginator import Paginator
from .forms import JobApplicationForm
from django.urls import reverse
import boto3
from django.conf import settings
from botocore.client import Config
from django.contrib import messages
from django.utils import timezone


# displays a job and click to apply
class JobView(DetailView):
    template_name = "job.html"
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user.dhclient
        context['form'] = JobApplicationForm()
        context['clientdocs'] = client.client_documents.all()
        return context
    
# displays a list of all the available jobs.
class JobList(View, ContextMixin):
    template_name = "jobs-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = Job.objects.filter(active_listing=True, closing_date__gte=timezone.now())

        paginator = Paginator(jobs, 25) # Show 25 jobs per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


# handles a job application.
class JobApplicationView(View):
    form_class = JobApplicationForm

    def post(self, request, **kwargs):
        client = request.user.dhclient
        job = Job.objects.get(pk=self.kwargs['pk'])
        existing_application = JobApplication.objects.filter(job=job, dhclient=client)

        # checks if the user has not applied for the same position already.
        if existing_application.exists():
            messages.warning(request, "You have already applied for this position.")
            return HttpResponseRedirect(reverse('job', kwargs={'pk': self.kwargs['pk']})) 

        clientdocs = client.client_documents.all()
        application_form = self.form_class(request.POST)
        if application_form.is_valid():
            application = JobApplication.objects.create(job=job, dhclient=client)
            
            session = boto3.Session()
            #create an s3 object for uploads.
            s3 = session.client(
                's3',
                region_name=settings.AWS_S3_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config = Config(signature_version = 's3v4')
            )         

            s3 = boto3.resource('s3')
            for doc in clientdocs:
                copy_source = {
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': str(doc.document)
                }
                s3.meta.client.copy(copy_source, settings.AWS_STORAGE_BUCKET_NAME, 'Job_Application_Documents/{}'.format(doc.doc_name))
                ApplicationDocument.objects.create(job_application=application, application_doc='Job_Application_Documents/{}'.format(doc.doc_name))
            messages.success(request, "Your application was received, Thank you.")
            return HttpResponseRedirect(reverse('job', kwargs={'pk': self.kwargs['pk']}))
        else:
            messages.warning(request, "Something went wrong. Please try again and make sure to fill all the required form fields.")
            return HttpResponseRedirect(reverse('job', kwargs={'pk': self.kwargs['pk']}))
        

