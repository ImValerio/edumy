

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=1024)),
                ('category', models.CharField(max_length=100)),
                ('image', models.FileField(default='settings.MEDIA_ROOT/imgs/default.jpg', upload_to='imgs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])])),
                ('duration', models.IntegerField(blank=True, default=0)),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('creation_date', models.DateField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_user', to='userAuth.usertype')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=1024)),
                ('duration', models.IntegerField(default=0)),
                ('file', models.FileField(default='settings.MEDIA_ROOT/imgs/default.jpg', upload_to='videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='video_course', to='courseHandler.course')),
            ],
        ),
        migrations.CreateModel(
            name='FollowCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='followCourse_course', to='courseHandler.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='followCourse_user', to='userAuth.usertype')),
            ],
        ),
    ]
