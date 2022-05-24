from django.urls import path

from courseHandler.views import create

app_name = 'courseHandler'

urlpatterns = [
    path('user/course/<int:id>', create, name='course-upload-video')

]
