from django.db import models

# Create your models here.
from userAuth.models import UserType


class Course(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=100)
    image = models.ImageField(width_field=1920, height_field=1080)
    duration = models.IntegerField()
    price = models.IntegerField()
    author = models.ForeignKey(UserType, related_name='course_user', on_delete=models.PROTECT)
    is_active = models.BooleanField()
    creation_date = models.DateField()
