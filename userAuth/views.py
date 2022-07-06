
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from userAuth.forms import UserSignup, UserUpdate
from userAuth.models import UserType


class UserCreationView(CreateView):
    form_class = UserSignup
    template_name = 'userAuth/user/signup.html'
    success_url = reverse_lazy('homepage')

class UserDetailView(DetailView):
    model = UserType
    template_name = 'userAuth/user/detail.html'

class UserUpdateView(UpdateView):
    model = UserType
    form_class = UserUpdate
    template_name = 'userAuth/user/update.html'

    def form_valid(self, form):
        pk = str(form.instance.pk)
        return redirect('userAuth:profile', pk)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'userAuth/user/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('homepage')

