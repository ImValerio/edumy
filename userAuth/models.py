from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User

class UserType(User):
    type = models.CharField(max_length=20)
    image = models.ImageField(upload_to='imgs', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg'])], default='imgs/default.jpg')