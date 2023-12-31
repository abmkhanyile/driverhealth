# from re import template
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib import messages
from django.views.generic.base import View, ContextMixin
from django.contrib import auth
from django.http import HttpResponseRedirect 
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from .forms import PreRegistrationForm
from django.urls import reverse
from .forms import UserCreationForm
from dhclients.forms import DHClientRegForm
from companies.forms import CompanyRegForm
import random
import threading
from .email_notifications import registration_notification
import requests
from django.conf import settings
from django.utils.decorators import method_decorator


# displays the login page.
@csrf_exempt
def login(request):
    msgStorage = messages.get_messages(request)
    c = {'messages': msgStorage}
    c.update(csrf(request))
    print(c)
    return render(request, 'authentication/login.html', c)

@csrf_exempt
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        if 'next' in request.POST:
            messages.warning(request, "Sorry, that's not a valid username and password")
            return redirect(request.POST.get("next"))
        else:
            messages.warning(request, "Sorry, that's not a valid username and password")
            return HttpResponseRedirect('/user_accounts/login')

    
def logout_success_view(request):
    return render(request, 'authentication/logout_success.html')

def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'authentication/password_change.html', args)


#Password reset view
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user_accounts/profile')
        else:
            return redirect('/user_accounts/password_change')
    else:
        form = PasswordResetForm(user=request.user)
        args = {'pwd_change_form': form}
        return render(request, 'authentication/password_change.html', args)


# this view prompts the user to choose if they are a Driver or a Transporter
class UserType(View, ContextMixin):
    template_name = "registration/choose-usertype.html"
    form_class = PreRegistrationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserType, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pre_reg_form'] = self.form_class()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        pre_reg_form = self.form_class(request.POST)
        if pre_reg_form.is_valid():
            ans = pre_reg_form.cleaned_data['user_type']
            if ans == 'Truck Driver':
                return HttpResponseRedirect(reverse("register"))
            elif ans == "Company":
                return HttpResponseRedirect(reverse("company-registration"))



# this view handles user registration i.e. DHClient


class Register(View, ContextMixin):
    template_name = "registration/register.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Register, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        context['client_form'] = DHClientRegForm()
        return context 

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


    def post(self, request, **kwargs):
        userform = UserCreationForm(request.POST)
        clientform = DHClientRegForm(request.POST)

        if userform.is_valid() and clientform.is_valid():
            place_id = clientform.cleaned_data['placeid']

            detailed_location = None
            if place_id is not None:
                detailed_location = self.getDetailedLocations(placeid=place_id)

            user = userform.save(commit=False)
            user.dh_id = random.randint(100000000,999999999)
            user.save()

            client = clientform.save(commit=False)
            client.user = user

            if detailed_location is not None:
                for addr_comp in detailed_location['result']['address_components']:
                    if "locality" in addr_comp['types']:
                        client.locality = addr_comp["long_name"]
                    elif "sublocality" in addr_comp['types']:
                        client.sublocality = addr_comp["long_name"]
                    elif "administrative_area_level_2" in addr_comp['types']:
                        client.administrative_area_level_2 = addr_comp["long_name"]
                    elif "administrative_area_level_1" in addr_comp['types']:
                        client.administrative_area_level_1 = addr_comp["long_name"]
                    elif "country" in addr_comp['types']:
                        client.country = addr_comp["long_name"]
         
            client.save()
            email_thread = threading.Thread(target = registration_notification, args=[user, 'A new user {} has just registered'.format(user)], daemon=True)
            email_thread.start()
            return HttpResponseRedirect(reverse('registration-success'))
        else:
            return render(request, self.template_name, {'user_form': userform, 'client_form': clientform})


    def getDetailedLocations(self, placeid):
        url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}".format(placeid, settings.GOOGLE_MAPS_API)
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        print(type(data))
        return data




# displays a success message after registration.
def registration_success_view(request):
    return render(request, "registration/registration-success.html")


# this view handles Company Registrations
class CompanyRegistration(View, ContextMixin):
    template_name = "registration/company-registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        context['company_form'] = CompanyRegForm()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        userform = UserCreationForm(request.POST)
        companyform = CompanyRegForm(request.POST)

        if userform.is_valid() and companyform.is_valid():
            user = userform.save(commit=False)
            user.dh_id = random.randint(100000000,999999999)
            user.save()

            company = companyform.save(commit=False)
            company.user = user
            company.save()
            return HttpResponseRedirect(reverse('registration-success'))
        else:
            return render(request, self.template_name, {'user_form': userform, 'company_form': companyform})

