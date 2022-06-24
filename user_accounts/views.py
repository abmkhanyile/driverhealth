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
