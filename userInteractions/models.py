from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from courseHandler.models import Video, Course
from userAuth.models import UserType

class Question(models.Model):
    body = models.CharField(max_length=1024)
    video = models.ForeignKey(Video, related_name='question_video', on_delete=models.CASCADE)
    student = models.ForeignKey(UserType, related_name='question_user', on_delete=models.PROTECT)

class Answer(models.Model):
    body = models.CharField(max_length=1024)
    author = models.ForeignKey(UserType, related_name='answer_user', on_delete=models.PROTECT)
    video = models.ForeignKey(Video, related_name='answer_video', on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

class Review(models.Model):
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=1024)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    #evaluation_author = models.IntegerField(default=0)
    student = models.ForeignKey(UserType, related_name='review_user', on_delete=models.PROTECT)
    course = models.ForeignKey(Course, related_name='review_course', on_delete=models.PROTECT)
