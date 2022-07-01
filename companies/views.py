from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from django.core.exceptions import PermissionDenied

class Dashboard(View, ContextMixin):
    template_name = "company-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        context['company'] = company
        return context

    def get(self, request, **kwargs):
        if not request.user.is_company():
            raise PermissionDenied
        return render(request, self.template_name, self.get_context_data())
