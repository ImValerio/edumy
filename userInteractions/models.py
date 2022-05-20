from django.db import models

# Create your models here.
from courseHandler.models import Video, Course
from userAuth.models import UserType


class Question(models.Model):
    body = models.CharField(max_length=1024)
    video = models.ForeignKey(Video, related_name='question_video', on_delete=models.PROTECT)
    student = models.ForeignKey(UserType, related_name='question_user', on_delete=models.PROTECT)

class Answer(models.Model):
    body = models.CharField(max_length=1024)
    question = models.ForeignKey(Question, related_name='answer_question', on_delete=models.PROTECT)
    author = models.ForeignKey(UserType, related_name='answer_user', on_delete=models.PROTECT)

class Review(models.Model):
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=1024)
    rating = models.IntegerField()
    student = models.ForeignKey(UserType, related_name='review_user', on_delete=models.PROTECT)
    course = models.ForeignKey(Course, related_name='review_course', on_delete=models.PROTECT)
