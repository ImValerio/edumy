# Create your views here.index'
from django.views.generic import DetailView
from courseHandler.forms import CreateVideo
from courseHandler.models import Video
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from courseHandler.forms import CourseForm
from userAuth.models import UserType

"""
class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'

"""
class VideoUploadDetail(DetailView):
    model = Video
    template_name = 'courseHandler/video/upload-video-detail.html'


def VideoUploadView(request, pk):
    if request.user.is_authenticated:
        print(request.user)
        if request.method == 'POST':
            form = CreateVideo(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.course_id = int(pk)
                instance.save()
                return redirect('courseHandler:course-upload-video', pk)
        else:
            form = CreateVideo()
            videos = Video.objects.all().filter(course_id=pk)
            context = {
                "form": form,
                "videos": videos,
                "pk": pk
            }
            return render(request, 'courseHandler/video/upload-video.html', context)
    else:
        return HttpResponseRedirect('/')

class CourseCreate(LoginRequiredMixin,CreateView):
    template_name = 'courseHandler/course/create.html'
    success_url = reverse_lazy('homepage')
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        return super().form_valid(form)


    """   def createCourse(request):
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
                return HttpResponseRedirect('/') """
