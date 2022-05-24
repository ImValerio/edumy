from django.urls import path

from courseHandler.views import VideoUploadView

app_name = 'courseHandler'

urlpatterns = [
    path('user/course/<int:pk>', VideoUploadView, name='course-upload-video')

]
