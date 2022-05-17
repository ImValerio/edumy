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

class FollowCourse(models.Model):
    course_id = models.ForeignKey(Course, related_name='followCourse_course', on_delete=models.CASCADE)
    student_id = models.ForeignKey(UserType, related_name='followCourse_user', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
