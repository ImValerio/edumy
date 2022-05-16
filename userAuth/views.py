from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from userAuth.forms import UserSignup


class UserCreationView(CreateView):
    form_class = UserSignup
    template_name = 'userAuth/user/signup.html'
    success_url = reverse_lazy('homepage')