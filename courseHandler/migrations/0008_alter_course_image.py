# Generated by Django 4.0.4 on 2022-07-08 08:40

import courseHandler.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseHandler', '0007_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.FileField(upload_to='imgs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'svg', 'jpeg']), courseHandler.models.validate_image]),
        ),
    ]