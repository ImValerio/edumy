from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from courseHandler.forms import SearchCourseForm
from courseHandler.models import FollowCourse, Course
from collections import Counter

from userInteractions.models import Review
from django.shortcuts import render, redirect


class Homepage(TemplateView):
    template_name = 'homepage.html'


def recomandation(request):
    context = {}
    # se userCourses è vuoto fare una ricerca totale dei corsi
    if request.method == 'POST':
        form = SearchCourseForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("homepage-search-result", sstring, where)
    else:
        form = SearchCourseForm()
        context['form'] = form
    if request.user.is_authenticated:
        user_courses = FollowCourse.objects.filter(student_id=request.user.id).select_related('course')
        courses = [course.course for course in user_courses]
        list_price = [c.price for c in courses]
        list_category = [c.category for c in courses]
        avg = sum(list_price) / len(list_category)
        price_percentage = avg * 0.3
        min_avg = avg - price_percentage
        max_avg = avg + price_percentage
        popular_category = list(Counter(list_category))[0]
        all_courses = Course.objects.filter(category=popular_category, price__range=(min_avg,max_avg), is_active='True')
        ids = [course.pk for course in user_courses]
        course_list = [course for course in all_courses if course.id not in ids]
        context['courseList'] = course_list
        if len(course_list):
            paginator = Paginator(course_list, 6)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            return render(request, "homepage.html", context)
    #query che prende tutte le recensioni che hanno almento un corso, le raggruppa per id e fa la media dei rating per quell'id
    reviews_courses = Review.objects.select_related('course')\
        .values('course').annotate(rating__avg=Avg('rating')).order_by("-rating__avg")
    id_courses = [course for course in reviews_courses.values_list('course', flat=True)]
    all_courses = Course.objects.filter(is_active='True')
    courses_list = [course for course in all_courses if course.id in id_courses]
    context['courseList'] = courses_list
    paginator = Paginator(courses_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, "homepage.html", context)

