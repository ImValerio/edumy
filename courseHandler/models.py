from django.core.validators import FileExtensionValidator
from django.db import models
from dj_shop_cart.cart import CartItem
from django.utils import timezone

# Create your models here.
from userAuth.models import UserType
from django.core.exceptions import ValidationError

def validate_image(image):
    correct_width = 1920
    correct_height = 1080
    height = image.height
    width = image.width
    if (width != correct_width) or height != correct_height:
        raise ValidationError("Image must have 1920x1080 resolution")


# Qunado un autore viene eliminato anche i suoi corsi vengono cancellati
# Il corso se viene eliminato rimane attivo(is_active) solo per gli utenti che lo hanno gia acquistato
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1024)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='imgs', validators=[validate_image])
    duration = models.IntegerField(default= 0, blank=True)
    price = models.IntegerField()
    author = models.ForeignKey(UserType, related_name='course_user', on_delete=models.CASCADE)
    is_active = models.BooleanField(default= False)
    creation_date = models.DateField()

    #def get_price(self, item: CartItem) -> Integer: return



# Se il corso o lo studente vengono eliminati le tuple rimangono inveriate
class FollowCourse(models.Model):
    course = models.ForeignKey(Course, related_name='followCourse_course', on_delete=models.PROTECT)
    student = models.ForeignKey(UserType, related_name='followCourse_user', on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)

# Se il corso viene eliminato i video rimangono disponibili per gli utenti che hanno gia acquistato il corso
class Video(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1024)
    duration = models.IntegerField(default=0)
    file = models.FileField(upload_to='videos', validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    course = models.ForeignKey(Course, related_name='video_course', on_delete=models.PROTECT, null=True, blank=True)

class Payment(models.Model):
    method = models.CharField(max_length=120)
    course = models.ForeignKey(Course, related_name='payment_course', on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(UserType, related_name='payment_user', on_delete=models.PROTECT, null=True, blank=True)


