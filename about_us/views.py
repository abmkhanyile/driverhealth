from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .models import About_Us

# dispalys the about us page.
class AboutUs(View, ContextMixin):
    template_name = "about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_us'] = About_Us.objects.get(about_us_id=0)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())
