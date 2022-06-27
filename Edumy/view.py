from django.db.models import Avg
from django.views.generic import TemplateView
from courseHandler.models import FollowCourse, Course
from collections import Counter

from userInteractions.models import Review
from django.shortcuts import render


class Homepage(TemplateView):
    template_name = 'homepage.html'

def recomandation(request):
    context = {}
    # se userCourses è vuoto fare una ricerca totale dei corsi
    user_courses = FollowCourse.objects.filter(student_id=request.user.id).select_related('course')
    if len(user_courses) == 0 and request.user.is_authenticated:
        courses = [course.course for course in user_courses]
        list_price = [c.price for c in courses]
        list_category = [c.category for c in courses]
        avg = sum(list_price) / len(list_category)
        price_percentage = avg * 0.3
        min_avg = avg - price_percentage
        max_avg = avg + price_percentage
        popular_category = list(Counter(list_category))[0]
        all_courses = Course.objects.filter(category=popular_category, price__range=(min_avg,max_avg))
        ids = [course.pk for course in user_courses]
        course_no_follow = [course for course in all_courses if course.id not in ids]
        context['courseList'] = course_no_follow
        return render(request, "homepage.html", context)
    else:
        #query che prende tutte le recensioni che hanno almento un corso, le raggruppa per id e fa la media dei rating per quell'id
        reviews_courses = Review.objects.select_related('course')\
            .values('course').annotate(rating__avg=Avg('rating')).order_by("-rating__avg")
        id_courses = [course for course in reviews_courses.values_list('course', flat=True)]
        all_courses = Course.objects.all()
        courses_list = [course for course in all_courses if course.id in id_courses]
        context['courseList'] = courses_list
        return render(request, "homepage.html", context)
