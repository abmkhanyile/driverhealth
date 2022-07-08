from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .forms import ContactForm
from django.core import mail
from django.core.mail import EmailMessage
from django.template import Context, Template
from django.conf import settings
from django.contrib import messages
from django.urls import reverse


# displays the contact us page.
class ContactUs(View, ContextMixin):
    template_name = "contact-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            surname = contact_form.cleaned_data['surname']
            email = contact_form.cleaned_data['email']
            contact_num = contact_form.cleaned_data['contact_num']
            message = contact_form.cleaned_data['message']

            params = {
                'message': message,
                'name': name,
                'surname': surname,
                'email': email,
                'contact_num': contact_num
            }

            html = Template('<!DOCTYPE html><html lang=en><meta charset=UTF-8><meta content="IE=edge"http-equiv=X-UA-Compatible><meta content="width=device-width,initial-scale=1"name=viewport><title>Truck Stop Email</title><p>{{message}}</p><br><br><h4>Sender\'s Details</h4><table><tr><td>Name:<td>{{name}} {{surname}}<tr><td>Contact Number:<td>{{contact_num}}<tr><td>Email Address:<td>{{email}}</table>')
            contxt = Context(params)
            html_message = html.render(contxt)
          
            connection = mail.get_connection()
            emailMsg = EmailMessage(
                'WEBSITE ENQUIRY',
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                ['asante.dgl@gmail.com'],
                reply_to=[email],
                headers={'Message-ID': 'DH00'},
                connection=connection
            )

            emailMsg.content_subtype = "html"
            emailMsg.send(fail_silently=False)
            messages.success(request, "Message sent")
            return HttpResponseRedirect(reverse('contact-us'))
        return HttpResponseRedirect(reverse('contact-us', kwargs={'contact_form': contact_form}))
