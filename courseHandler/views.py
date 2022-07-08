# Create your views here.index'
from collections import Counter
from django.db.models import Avg

from dj_shop_cart.cart import get_cart_class
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Max, Count
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView, DeleteView, UpdateView

from courseHandler.forms import CreateVideo, SearchCourseForm, UpdateVideoForm, PaymentsForm
from courseHandler.models import Video, Course, FollowCourse, Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from courseHandler.forms import CourseForm

from userInteractions.forms import QuestionForm, ReviewForm
from userInteractions.models import Question, Answer, Review

"""
class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'

"""

Cart = get_cart_class()


def teacher_is_authorized(request, pk):
    if not request.user.is_authenticated:
        return False
    course_check = Course.objects.get(pk=pk)
    if course_check.author_id != request.user.id:
        return False

    return True


def VideoUploadDetail(request, course_id, pk):
    check_follow = FollowCourse.objects.filter(course_id=course_id, student_id=request.user.id)
    if (request.user.is_authenticated and check_follow) or teacher_is_authorized(request, course_id) :
        if request.method == 'POST':
            form_question = QuestionForm(request.POST, request.FILES)
            if form_question.is_valid():
                instance = form_question.save(commit=False)
                instance.student_id = request.user.id
                instance.video_id = int(pk)
                instance.save()
                messages.add_message(request, messages.SUCCESS, 'The question was created successfully')
                return redirect('courseHandler:course-upload-video-detail', course_id, pk)
        else:
            form_question = QuestionForm()
            questions = Question.objects.all().filter(video_id=pk)
            answers = Answer.objects.all().filter(video_id=pk)
            course = Course.objects.get(pk=course_id)
            questions_answer_list = list(zip(questions, answers))[:5]
            video = Video.objects.get(pk=pk)
            context = {
                "form_question": form_question,
                "questions_answer_list": questions_answer_list,
                "video": video,
                "course": course,
            }
            return render(request, 'courseHandler/video/upload-video-detail.html', context)
    else:
        return HttpResponseRedirect('/')


def VideoUploadView(request, pk):
    if request.user.is_authenticated:
        is_author = teacher_is_authorized(request, pk)
        if request.method == 'POST' and is_author:
            form = CreateVideo(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.course_id = int(pk)
                instance.save()
                messages.add_message(request, messages.SUCCESS, 'The video was created successfully')
                return redirect('courseHandler:course-upload-video', pk)

        user_follow_course = False
        if not is_author:
            user_follow_course = FollowCourse.objects.get(student_id=request.user.id, course_id=pk)
        if is_author or user_follow_course:
            max_video_page = 6
            videos = Video.objects.filter(course_id=pk)
            paginator = Paginator(videos, max_video_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            video_index = 0
            if page_number:
                video_index = (int(page_number) - 1) * max_video_page
            context = {
                "page_obj": page_obj,
                "video_index": video_index,
                "pk": pk,

            }
            if is_author:
                form = CreateVideo()
                context['form'] = form

            return render(request, 'courseHandler/video/videos.html', context)
        else:
            return HttpResponseRedirect('/')

    else:
        return HttpResponseRedirect('/')


class VideoUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Video
    form_class = UpdateVideoForm
    template_name = 'courseHandler/video/update.html'
    success_message = "The video was updated successfully"

    def form_valid(self, form):
        form.instance.save()
        pk = str(form.instance.course_id)
        return redirect('courseHandler:course-upload-video', pk)


class CourseCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'courseHandler/course/create.html'
    form_class = CourseForm
    success_url = reverse_lazy('courseHandler:course-list')
    success_message = "The course was created successfully"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.usertype.type == 'teacher':
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # author = get_object_or_404(UserType, pk=form.instance.author_id)
        # if author.type == "Teacher":
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
        # else:
        # print("Tu non sei un teacher")


class CourseDetail(FormMixin, DetailView):
    model = Course
    template_name = "courseHandler/course/detail.html"
    form_class = ReviewForm

    def dispatch(self, request, *args, pk, **kwargs):
        course_check = Course.objects.get(pk=pk)
        if not course_check.is_active and course_check.author_id != request.user.id:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('courseHandler:course-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        if teacher_is_authorized(self.request, self.object.id):
            student_count = FollowCourse.objects.filter(course_id=self.object.id)
            context['student_count'] = len(student_count)
        # se userCourses è vuoto fare una ricerca totale dei corsi
        # userCourses = FollowCourse.objects.filter(student_id=self.request.user.id).select_related('course')
        # courses = [course.course for course in userCourses]
        # listPrice = [c.price for c in courses]
        # listcategory = [c.category for c in courses]
        # avg = sum(listPrice) / len(listcategory)
        # percentage = avg * 0.3
        # minAvg = avg - percentage
        # maxAvg = avg + percentage
        # popularCategory = list(Counter(listcategory))[0]
        # fare la ricerca su corso preso in dettaglio(utilizzare self)
        # all_courses = Course.objects.filter(category=popularCategory, price__range=(minAvg,maxAvg))
        percentage = self.object.price * 0.3
        min_price = self.object.price - percentage
        max_price = self.object.price + percentage
        all_courses = Course.objects.filter(category=self.object.category, price__range=(min_price, max_price), is_active='True').order_by('-price')[:4]
        # ids = [course.pk for course in userCourses]
        course_no_follow = [course for course in all_courses if course.id != self.object.id]
        videos_count = len(Video.objects.filter(course_id=self.object.id))
        context['couseList'] = course_no_follow
        # context['couseList'] = all_courses
        reviews = Review.objects.filter(course_id=self.object.id).select_related('student')
        ratings = [review.rating for review in reviews]
        cart = Cart.new(self.request)
        context['prodInCart'] = self.object in cart.products
        if ratings:
            context['rating_avg'] = round(sum(ratings) / len(ratings), 1)
            context['reviews'] = reviews[:5]
        check_follow = FollowCourse.objects.filter(course_id=self.object.id, student_id=self.request.user.id)
        if check_follow :
            context['formReview'] = ReviewForm(initial={'post': self.object})
        context['videosCount'] = videos_count
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, formReview):
        course = self.get_object()
        instance = formReview.save(commit=False)
        instance.course_id = int(course.pk)
        instance.student_id = int(self.request.user.id)
        formReview.save()
        return super(CourseDetail, self).form_valid(formReview)


class CourseDelete(SuccessMessageMixin, DeleteView):
    model = Course
    template_name = 'courseHandler/course/delete.html'
    success_url = reverse_lazy('courseHandler:course-list')
    success_message = "The course was deleted successfully"

    def dispatch(self, request, *args, pk, **kwargs):
        course = Course.objects.get(id=pk)
        if not teacher_is_authorized(request, pk) or course.is_active:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class CourseUpdate(SuccessMessageMixin, UpdateView):
    model = Course
    template_name = 'courseHandler/course/update.html'
    success_url = reverse_lazy('courseHandler:course-list')
    form_class = CourseForm
    success_message = "The course was updated successfully"

    def dispatch(self, request, *args, pk, **kwargs):
        if not teacher_is_authorized(request, pk):
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class CourseList(ListView):
    model = Course
    template_name = 'courseHandler/course/search_result.html'

    def get_context_data(self, **kwargs):
        courses_bought_id = []
        if hasattr(self.request.user, 'usertype') and self.request.user.usertype.type == 'student':
            courses_bought = FollowCourse.objects.filter(student_id=self.request.user.id)
            courses_bought_id = [e.course_id for e in courses_bought]
        cart = Cart.new(self.request)

        id_courses_follow = [course for course in FollowCourse.objects.filter(student_id=self.request.user.id).values_list('course_id',
                                                                                                 flat=True)]

        self.object_list = self.object_list.values()
        print(self.object_list)
        all_courses = [course for course in self.object_list if course['id'] not in id_courses_follow]
        student_count = FollowCourse.objects.select_related('course').values('course')\
            .annotate(student__count=Count('student_id'))


        student_count = student_count.values()
        for course in all_courses:
            course['student__count'] = -1

        for course in all_courses:
            for count in student_count:
                if course['id'] == count['course_id']:
                    course['student__count'] = count['student__count']

        sort_course = sorted(all_courses, key=lambda x: x['student__count'])[::-1]

        context = {
            "object_list": sort_course,
            "cartProd": cart.products,
            "coursesBought": courses_bought_id,
        }

        return context

class CourseListHomepage(ListView):
    model = Course
    template_name = 'search_result_homepage.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.request.user.is_authenticated and self.request.user.usertype.type != 'teacher':
            user_courses = FollowCourse.objects.filter(student_id=self.request.user.id).select_related('course')
            print(len(user_courses))
            if len(user_courses):
                courses = [course.course for course in user_courses]
                list_price = [c.price for c in courses]
                list_category = [c.category for c in courses]
                avg = sum(list_price) / len(list_category)
                price_percentage = avg * 0.3
                min_avg = avg - price_percentage
                max_avg = avg + price_percentage
                popular_category = list(Counter(list_category))[0]
                all_courses = Course.objects.filter(category=popular_category, price__range=(min_avg, max_avg),
                                                    is_active='True')
                ids = [course.pk for course in user_courses]
                course_list = [course for course in all_courses if course.id not in ids]
                course_list_search = [course for course in self.object_list for c2 in course_list if course.id == c2.id]
                paginator = Paginator(course_list_search, 6)
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                context['page_obj'] = page_obj
                return context
        # query che prende tutte le recensioni che hanno almento un corso, le raggruppa per id e fa la media dei rating per quell'id
        reviews_courses = Review.objects.select_related('course') \
            .values('course').annotate(rating__avg=Avg('rating')).order_by("-rating__avg")
        id_courses = [course for course in reviews_courses.values_list('course', flat=True)]
        all_courses = self.object_list
        courses_list = [course for course in all_courses if course.id in id_courses]
        context['courseList'] = courses_list
        paginator = Paginator(courses_list, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context



def CourseListView(request):
    if not request.user.is_authenticated:
        return redirect('homepage')

    if request.user.usertype.type == 'student':
        courses = FollowCourse.objects.all().filter(student_id=request.user.id).select_related('course').order_by('-start_date')
        courses = [e.course for e in courses]
    else:
        courses = Course.objects.all().filter(author_id=request.user.id).order_by('-creation_date')
    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "courses": courses,
        'page_obj': page_obj
    }
    return render(request, 'courseHandler/course/list.html', context)


def CourseListStore(request):
    if request.method == 'POST':
        form = SearchCourseForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("courseHandler:course-search-result", sstring, where)
    else:
        courses = Course.objects.all().filter(is_active=True)
        courses_bought_id = []
        print(request.user)
        if hasattr(request.user, 'usertype') and request.user.usertype.type == 'student':
            courses_bought = FollowCourse.objects.filter(student_id=request.user.id)
            courses_bought_id = [e.course_id for e in courses_bought]
        cart = Cart.new(request)
        form = SearchCourseForm()
        context = {
            "courses": courses,
            "cartProd": cart.products,
            "coursesBought": courses_bought_id,
            "form": form
        }
        return render(request, 'courseHandler/course/store.html', context)


"""class CourseListStore(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courseHandler/course/store.html'

"""


def search(request):
    if request.method == "POST":
        form = SearchCourseForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("courseHandler:course-search-result", sstring, where)
    else:
        form = SearchCourseForm()
    return render(request, template_name="courseHandler/course/search.html", context={"form": form})


class CourseSearchView(CourseList):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        where = self.request.resolver_match.kwargs["where"]
        if "Title" in where:
            res = self.model.objects.filter(title__icontains=sstring)
        elif "Author" in where:
            res = self.model.objects.filter(author__username__icontains=sstring)
        else:
            res = self.model.objects.filter(category__icontains=sstring)
        return res

        return super().form_valid(form)


class CourseSearchViewHompage(CourseListHomepage):
    titolo = "La tua ricerca ha dato come risultato"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        where = self.request.resolver_match.kwargs["where"]
        if "Title" in where:
            res = self.model.objects.filter(title__icontains=sstring)
        elif "Author" in where:
            res = self.model.objects.filter(author__username__icontains=sstring)
        else:
            res = self.model.objects.filter(category__icontains=sstring)
        return res

        return super().form_valid(form)


def courses_statistic(request, pk):
    context = {}
    courses = Course.objects.filter(author_id=request.user.id)
    courses_id = [course.id for course in courses]
    bests_sellers = FollowCourse.objects.filter(course_id__in=courses_id).values('course').annotate(Count('course'))
    print(bests_sellers[0]['course'])
    courses = courses.values()
    for c in courses:
        for c1 in bests_sellers:
            if c['id'] == c1['course']:
                c['course_sold'] = c1['course__count']
    context['courses'] = courses
    return render(request, "courseHandler/course/statistic.html")


def CartView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PaymentsForm(request.POST)
            if form.is_valid():
                cart = Cart.new(request)
                for item in cart:
                    Payment.objects.create(method=request.POST['payments'], course_id=int(item.product.id),
                                           user_id=int(request.user.id))

                    FollowCourse.objects.create(course_id=int(item.product.id), student_id=request.user.id)

                empty_cart(request)
                return redirect('courseHandler:course-list')
        else:
            cart = Cart.new(request)
            items_prices = [item.price for item in cart.products]
            tot_price = sum(items_prices)
            payments_form = PaymentsForm()
            context = {
                "cart": cart,
                "totPrice": tot_price,
                "paymentsForm": payments_form
            }
            return render(request, 'cart.html', context)
    else:
        return HttpResponseRedirect('/')


@require_GET
def add_product(request, pk):
    cart = Cart.new(request)
    course = Course.objects.get(pk=pk)
    cart.add(course, quantity=1)
    return JsonResponse({'msg': 'Course added'})


@require_GET
def remove_product(request, pk):
    course = Course.objects.get(pk=pk)
    cart = Cart.new(request)
    cart.remove(course, quantity=1)
    return redirect(reverse('courseHandler:cart-view'))


@require_POST
def empty_cart(request: HttpRequest):
    Cart.new(request).empty()


@require_GET
def publish_course(request, pk):
    course = Course.objects.get(id=pk)
    course.is_active = True
    course.save()
    return JsonResponse({'msg': 'Now the course is visible'})


@require_GET
def read_notifications(request, pk):
    user = User.objects.get(pk=pk)
    user.notifications.mark_all_as_read()
    return JsonResponse({'msg': 'There are 0 unread notifications'})
