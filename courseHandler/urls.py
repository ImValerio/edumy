from django.urls import path

from courseHandler.views import CourseCreate

app_name = 'courseHandler'

urlpatterns = [
    path('course/create', CourseCreate.as_view(), name='course-create'),
]