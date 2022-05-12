from django.db import models

# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django.db import models


class UserCreation(UserCreationForm):
    type = models.CharField(max_length=50)
