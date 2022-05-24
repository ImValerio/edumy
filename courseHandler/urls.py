from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from courseHandler.views import VideoUploadView, VideoUploadDetail

app_name = 'courseHandler'

urlpatterns = [
    path('user/course/<int:pk>', VideoUploadView, name='course-upload-video'),
    path('user/course/<int:course_id>/video/<int:pk>', VideoUploadDetail.as_view(), name='course-upload-video-detail')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
