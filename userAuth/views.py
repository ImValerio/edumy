from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from userAuth.models import UserCreation


class UserCreationView(CreateView):
    form_class = UserCreation
    template_name = 'userAuth/user/signup.html'
    success_url = reverse_lazy('homepage')