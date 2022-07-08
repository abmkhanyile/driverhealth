from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .forms import ClientDocForm, EmploymentHistoryForm, EditClientForm
from django.conf import settings
import boto3
import string
import random
from botocore.client import Config
from dhclients.models import DHClient, ClientDocument, EmploymentHistory
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator


# displays the client profile.
class ClinetProfile(View, ContextMixin):
    template_name = "client-profile.html"
    form_class = ClientDocForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user.dhclient
        context['client'] = client
        context['stars_list'] = [1,2,3,4,5]
        context['docform'] = self.form_class()
        context['clientdocs'] = client.client_documents.all()
        context['employment_history_form'] = EmploymentHistoryForm()
        context['work_history'] = client.client_employment_history.all()
        return context

    def get(self, request, **kwargs):
        if not request.user.is_dhclient():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        if len(self.get_context_data()['work_history']) >= 3:
            messages.success(request, "You can't have more than 3 work experience entries")
            return HttpResponseRedirect(reverse('client-profile'))
            
        emp_history_form = EmploymentHistoryForm(request.POST)
        if emp_history_form.is_valid():
            emp_history = emp_history_form.save(commit=False)
            emp_history.dhclient = self.get_context_data()['client']
            emp_history.save()
            messages.success(request, "Employment history created successfully...")
            return HttpResponseRedirect(reverse('client-profile'))
        else:
            messages.warning(request, "Something went wrong, please try again...")
            return HttpResponseRedirect(reverse('client-profile')) 



def randomString(stringLength):
    # Generate a random string of fixed length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

    
# handles the uploading of driver documents.
def upload_client_doc(request):
    if request.method == 'POST':
        file_name = request.POST.get('documents_name')      #extracts a list of all file names for files selected by the user.
        clientId = request.POST.get('clientpk')
        document_type = request.POST.get('doctype')
        otherdoc_type = request.POST.get('otherdoc_type')

        client = DHClient.objects.get(pk=clientId)
        dataList = []
        session = boto3.Session()
        #create an s3 object for uploads.
        s3 = session.client(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config = Config(signature_version = 's3v4')
        )         
                     
        S3BUCKET = settings.AWS_STORAGE_BUCKET_NAME
        fname = "Client_Documents/{}".format(file_name)
        
        presigned_post = s3.generate_presigned_post(
            Bucket=S3BUCKET,
            Key= fname,
            Fields={"acl": "public-read"},
            
            Conditions=[
                {"acl": "public-read"}
            ],
            ExpiresIn=3600
        )
        dataList.append(
            {
                'original_fname': file_name,
                'data': presigned_post,
                'aws_fname': "{}".format(fname),
                'url': 'https://{}.s3.eu-west-2.amazonaws.com/{}'.format(settings.AWS_STORAGE_BUCKET_NAME, fname)
            }
        )
        
        ClientDocument.objects.create(client=client, document=fname, doc_type=document_type, other_type=otherdoc_type, doc_name=file_name)
        return JsonResponse(dataList, safe=False)
    else:
        print("Not post method")


# deletes driver documents uploaded to profile.
class DelDoc(View):
    template_name = "driver-profile.html"

    def get(self, request, **kwargs):
        doc = ClientDocument.objects.get(pk=kwargs['pk'])
        doc.delete()
        messages.warning(request, "Document deleted successfully.")
        return HttpResponseRedirect(reverse('client-profile'))


# changes the document visibility to recruiters.
def change_visibility(request):
    if request.method == 'POST':
        doc_pk = request.POST.get('doc_pk') 
        doc = ClientDocument.objects.get(pk=doc_pk)
        if doc.doc_visibility == 1:
            doc.doc_visibility = 2
            doc.save()
        elif doc.doc_visibility == 2:
            doc.doc_visibility = 1
            doc.save()
        return JsonResponse({"Success": "success"}, safe=False)



# handles the process of uploading a driver's profile pic.
class UplaodProfileImg(View):
    def post(self, request, **kwargs):
        file_name = request.POST.getlist('img_name')   
        client_id = request.POST.get('clientpk')
        client = DHClient.objects.get(pk=int(client_id))
           
        dataList = []
        session = boto3.Session()
        #create an s3 object for uploads.
        s3 = session.client(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config = Config(signature_version = 's3v4')
        )         
                        
        S3BUCKET = settings.AWS_STORAGE_BUCKET_NAME
        
        fname = randomString(30)
        f_name = fname
        fname = "Profile_Pics/{}.webp".format(f_name)
        
        presigned_post = s3.generate_presigned_post(
            Bucket=S3BUCKET,
            Key= fname,
            Fields={"acl": "public-read"},
            
            Conditions=[
                {"acl": "public-read"}
            ],
            ExpiresIn=3600
        )
        dataList.append(
            {
                'original_fname': file_name,
                'data': presigned_post,
                'aws_fname': "{}.webp".format(f_name),
                'url': 'https://{}.s3.eu-west-2.amazonaws.com/{}'.format(settings.AWS_STORAGE_BUCKET_NAME, fname)
            }
        )
        client.profile_picture = 'Profile_Pics/{}.webp'.format(f_name)
        client.save()
        return JsonResponse(dataList, safe=False)


# handles editing client personal details on the dashboard.
class EditClient(View, ContextMixin):
    template_name = "edit-personal-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user.dhclient
        context['client'] = client
        context['editform'] = EditClientForm(instance=client)
        return context

    def get(self, request, **kwargs):
        if request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        editform = EditClientForm(request.POST, instance=self.get_context_data()['client'])
        if editform.is_valid():
            editform.save()
            messages.success(request, "Details successfully updated...")
            return HttpResponseRedirect(reverse("client-profile"))


# handles editing of the work experience section on the dashboard
class EditWorkExp(View, ContextMixin):
    template_name = "edit-workexp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workexp = EmploymentHistory.objects.get(pk=self.kwargs['pk'])
        context['workexp'] = workexp
        context['editform'] = EmploymentHistoryForm(instance=workexp)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        workexp_form = EmploymentHistoryForm(request.POST, instance=self.get_context_data()['workexp'])
        if workexp_form.is_valid():
            workexp_form.save()
            messages.success(request, "Employment history successfully updated...")
            return HttpResponseRedirect(reverse("client-profile"))


# displays all the job applications by the driver.
class JobApplications(View, ContextMixin):
    template_name = "job-applications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.user.dhclient
        applications = client.dhclient_applications.all()

        paginator = Paginator(applications, 25) # Show 25 clients per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context

    def get(self, request, **kwargs):
        if request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())