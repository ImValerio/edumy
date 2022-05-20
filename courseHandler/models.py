from django.db import models

# Create your models here.
from userAuth.models import UserType

# Qunado un autore viene eliminato anche i suoi corsi vengono cancellati
# Il corso se viene eliminato rimane attivo(is_active) solo per gli utenti che lo hanno gia acquistato
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1024)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='imgs', width_field=1920, height_field=1080)
    duration = models.IntegerField()
    price = models.IntegerField()
    author = models.ForeignKey(UserType, related_name='course_user', on_delete=models.CASCADE)
    is_active = models.BooleanField()
    creation_date = models.DateField()

# Se il corso o lo studente vengono eliminati le tuple rimangono inveriate
class FollowCourse(models.Model):
    course = models.ForeignKey(Course, related_name='followCourse_course', on_delete=models.PROTECT)
    student = models.ForeignKey(UserType, related_name='followCourse_user', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()

# Se il corso viene eliminato i video rimangono disponibili per gli utenti che hanno gia acquistato il corso
class Video(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1024)
    duration = models.IntegerField()
    course = models.ForeignKey(Course, related_name='video_course', on_delete=models.PROTECT)

