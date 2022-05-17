from django.db import models
from django.contrib.auth.models import User
class UserType(User):
    type = models.CharField(max_length=20)
