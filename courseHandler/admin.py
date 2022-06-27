from django.contrib import admin

# Register your models here.
from courseHandler.models import Course, FollowCourse, Payment, Video
from userAuth.models import UserType
from userInteractions.models import Question, Answer, Review

admin.site.register(Course)
admin.site.register(FollowCourse)
admin.site.register(Video)
admin.site.register(Payment)

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Review)

admin.site.register(UserType)
