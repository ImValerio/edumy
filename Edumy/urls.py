
import notifications.urls
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from Edumy.view import homepage
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('', include('userAuth.urls')),
    path('', include('courseHandler.urls')),
    path('', include('userInteractions.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
