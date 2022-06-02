from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from courseHandler.views import VideoUploadView, CourseCreate, CourseDetail, CourseList, \
    CourseDelete, CourseUpdate, search, CourseSearchView, VideoUpUploadDetail

app_name = 'courseHandler'

urlpatterns = [
    path('user/course/<int:pk>', VideoUploadView, name='course-upload-video'),
    path('user/course/<int:course_id>/video/<int:pk>', VideoUpUploadDetail, name='course-upload-video-detail'),
    path('course/create', CourseCreate.as_view(), name='course-create'),
    path('course/<int:pk>/detail', CourseDetail.as_view(), name='course-detail'),
    path('course/<int:pk>/delete', CourseDelete.as_view(), name='course-delete'),
    path('course/<int:pk>/update', CourseUpdate.as_view(), name='course-update'),
    path("course/search", search, name="course-search"),
    path("course/search/result/<str:sstring>/<str:where>/", CourseSearchView.as_view(), name="course-search-result"),
    path('course/list', CourseList.as_view(), name='course-list'),
    path('', include('userInteractions.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
