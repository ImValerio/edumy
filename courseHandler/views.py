
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from courseHandler.forms import CourseForm
from courseHandler.models import Course
from userAuth.models import UserType


class CourseCreate(LoginRequiredMixin,CreateView):
    template_name = 'courseHandler/course/create.html'
    success_url = reverse_lazy('homepage')
    form_class = CourseForm

    def form_valid(self, form):
        author = get_object_or_404(UserType, pk=form.instance.author_id)
        if author.type == "Teacher":
            form.instance.author_id = self.request.user.id
            return super().form_valid(form)
        else:
            print("Tu non sei un teacher")

'''def createCourse(request):
    if request.user.is_authenticated and request.user.type == "teacher":
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author_id = request.user.id
                instance.save()
                return redirect('courseHandler:course-create')
        else:
            form = CourseForm()
            context = {
                "form": form,
            }
            return render(request, 'courseHandler/course/create.html', context)
    else:
        return HttpResponseRedirect('/')'''




