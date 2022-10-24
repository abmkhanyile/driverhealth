from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .models import Gallery_image

# displays the gallery.
class Gallery(View, ContextMixin):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_photos'] = Gallery_image.objects.all()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())