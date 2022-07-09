from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, DetailView, UpdateView

from userAuth.forms import UserSignup, UserUpdate
from userAuth.models import UserType

from django.contrib import messages


class UserCreationView(SuccessMessageMixin, CreateView):
    form_class = UserSignup
    template_name = 'userAuth/user/signup.html'
    success_url = reverse_lazy('homepage')
    success_message = "Successfully Created Your User Profile"

class UserDetailView(DetailView):
    model = UserType
    template_name = 'userAuth/user/detail.html'

class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = UserType
    form_class = UserUpdate
    template_name = 'userAuth/user/update.html'
    success_message = "Successfully Updated Your User Profile"

    def form_valid(self, form):
        pk = str(form.instance.pk)
        instance = form.instance
        instance.save()
        return redirect('userAuth:profile', pk)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'userAuth/user/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('homepage')

@require_GET
def delete_account(request, user_id):
    if request.user.id == user_id:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "Account deleted successfully")
        return render(request, 'homepage.html')

    return render(request, 'homepage.html')
