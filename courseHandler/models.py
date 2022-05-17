from django.db import models

# Create your models here.
from userAuth.models import UserType


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1024)
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

class Video(models.Model):
    title = models.CharField(max_length=120)
    duration = models.IntegerField()
    course_id = models.ForeignKey(Course, related_name='video_course', on_delete=models.CASCADE)

class Question(models.Model):
    body = models.CharField(max_length=1024)
    video_id = models.ForeignKey(Video, related_name='question_video', on_delete=models.CASCADE)
    student_id = models.ForeignKey(UserType, related_name='question_user', on_delete=models.PROTECT)

class Answer(models.Model):
    body = models.CharField(max_length=1024)
    question_id = models.ForeignKey(Question, related_name='answer_question', on_delete=models.CASCADE)
    author_id = models.ForeignKey(UserType, related_name='answer_user', on_delete=models.PROTECT)

class Review(models.Model):
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=1024)
    rating = models.IntegerField(max_length=1)
    student_id = models.ForeignKey(UserType, related_name='review_user', on_delete=models.PROTECT)
    course_id = models.ForeignKey(Course, related_name='review_course', on_delete=models.PROTECT)
