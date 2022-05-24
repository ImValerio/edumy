# Create your views here.index'
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView

from courseHandler.forms import CreateVideo
from courseHandler.models import Video

"""
class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'

"""


def VideoUploadView(request, pk):
    if request.user.is_authenticated:
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
            print(videos)
            context = {
                "form": form,
                "videos": videos
            }
            return render(request, 'courseHandler/video/upload-video.html', context)
    else:
        return HttpResponseRedirect('/')


