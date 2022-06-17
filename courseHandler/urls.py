from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from courseHandler.views import VideoUploadView, VideoUploadDetail, CourseCreate, CourseDetail, CourseList, \
    CourseDelete, CourseUpdate, search, CourseSearchView, VideoUpdateView, CourseListStore, add_product, CartView, \
    remove_product, CourseListView, publish_course, read_notifications

app_name = 'courseHandler'

urlpatterns = [
    path('<int:pk>/readNotifications', read_notifications, name='read-notifications'),
    path('user/course/<int:pk>', VideoUploadView, name='course-upload-video'),
    path('user/course/<int:course_id>/video/<int:pk>', VideoUploadDetail, name='course-upload-video-detail'),
    path('user/course/<int:course_id>/video/<int:pk>/update', VideoUpdateView.as_view(), name='video-update'),
    path('course/create', CourseCreate.as_view(), name='course-create'),
    path('course/<int:pk>/detail', CourseDetail.as_view(), name='course-detail'),
    path('course/<int:pk>/delete', CourseDelete.as_view(), name='course-delete'),
    path('course/<int:pk>/update', CourseUpdate.as_view(), name='course-update'),
    path("course/search", search, name="course-search"),
    path("course/search/result/<str:sstring>/<str:where>/", CourseSearchView.as_view(), name="course-search-result"),
    path('course/list', CourseListView, name='course-list'),
    path('course/<int:pk>/publish', publish_course, name='course-publish'),
    path('store', CourseListStore, name='course-list-store'),
    path('cart', CartView, name='cart-view'),
    path('cart/add/<int:pk>', add_product, name='add-product'),
    path('cart/remove/<int:pk>', remove_product, name='remove-product'),
    path('', include('userInteractions.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
