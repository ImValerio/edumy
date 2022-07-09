from django.core.paginator import Paginator
from django.db.models import Avg

from django.views.generic import TemplateView

from courseHandler.forms import SearchCourseForm
from courseHandler.models import FollowCourse, Course
from collections import Counter

from userInteractions.models import Review
from django.shortcuts import render

def homepage(request):
    context = {}
    #query che prende tutte le recensioni che hanno almento un corso, le raggruppa per id e fa la media dei rating per quell'id
    reviews_courses = Review.objects.select_related('course')\
        .values('course').annotate(rating__avg=Avg('rating')).order_by("-rating__avg")
    id_courses = [course for course in reviews_courses.values_list('course', flat=True)]
    all_courses = Course.objects.filter(is_active='True')
    all_courses = all_courses.values()
    courses_list = [course for course in all_courses if course['id'] in id_courses]
    for course in courses_list:
        course['rating__avg'] = -1
    for course in all_courses:
        for review_course in reviews_courses:
            if course['id'] == review_course['course']:
                course['rating__avg'] = review_course['rating__avg']
    sort_course = sorted(courses_list, key=lambda x: x['rating__avg'])[::-1]
    paginator = Paginator(sort_course, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, "homepage.html", context)

