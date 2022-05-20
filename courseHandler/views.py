from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from courseHandler.forms import CourseForm
from courseHandler.models import Course


class CourseCreate(CreateView):
    model = Course
    template_name = 'courseHandler/course/create.html'
    #fields = ['title', 'description', 'category', 'price', 'creation_date']
    success_url = reverse_lazy('hompage')
    form_class = CourseForm
