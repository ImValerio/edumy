from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from userAuth.views import UserCreationView, UserDetailView, UserUpdateView, ChangePasswordView

app_name = 'userAuth'

urlpatterns = [
    path('signup/', UserCreationView.as_view(), name='signup'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update', UserUpdateView.as_view(), name='update-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

]
