from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from userAuth.views import UserCreationView

app_name = 'userAuth'

urlpatterns = [
    path('signup/', UserCreationView.as_view(), name='signup'),
   
]
