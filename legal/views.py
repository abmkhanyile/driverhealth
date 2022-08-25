from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .models import LegalDocs

class TermsAndConditions(View, ContextMixin):
    template_name = "ts-and-cs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['ts_and_cs'] = LegalDocs.objects.get(doc_id=1)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class TermsOfService(View, ContextMixin):
    template_name = "terms-of-service.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['terms_of_service'] = LegalDocs.objects.get(doc_id=2)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class PrivacyPolicy(View, ContextMixin):
    template_name = "privacy-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['privacy_policy'] = LegalDocs.objects.get(doc_id=3)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class CookiePolicy(View, ContextMixin):
    template_name = "cookie-policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['cookie_policy'] = LegalDocs.objects.get(doc_id=4)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())