from django.shortcuts import render
from django.views.generic.base import View, ContextMixin
from .models import AnimatedText
from training_courses.models import TrainingCourse, Code14Course

# displays the homepage.
class Home(ContextMixin, View):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['animated_txt'] = AnimatedText.objects.all()
        context['training_course'] = TrainingCourse.objects.all()
        context['code14courses'] = Code14Course.objects.all()
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())