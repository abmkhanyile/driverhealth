from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .models import AnimatedText

from careers.models import Job
from django.utils import timezone
from contact_us.forms import ContactForm


# displays the homepage.
class Home(ContextMixin, View):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animated_txt'] = AnimatedText.objects.all()
        jobs = list(Job.objects.filter(active_listing=True, closing_date__gte=timezone.now()))
        context['available_jobs'] = jobs[:12]
        context['current_date'] = timezone.now()
        context['contact_form'] = ContactForm()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())