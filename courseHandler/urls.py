from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from courseHandler.views import VideoUploadView, VideoUploadDetail, CourseCreate, CourseDetail, CourseList

app_name = 'courseHandler'

urlpatterns = [
    path('user/course/<int:pk>', VideoUploadView, name='course-upload-video'),
    path('user/course/<int:course_id>/video/<int:pk>', VideoUploadDetail.as_view(), name='course-upload-video-detail'),
    path('course/create', CourseCreate.as_view(), name='course-create'),
    path('course/<int:pk>/detail', CourseDetail.as_view(), name='course-detail'),
    path('course/list', CourseList.as_view(), name='course-list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
