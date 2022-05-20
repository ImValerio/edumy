from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from courseHandler.forms import CreateVideo
from courseHandler.models import Video


class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'