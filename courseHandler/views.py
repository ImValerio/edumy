# Create your views here.index'
from audioop import avg
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
                return redirect('courseHandler:course-upload-video-detail', course_id, pk)
        else:
            form_question = QuestionForm()
            questions = Question.objects.all().filter(video_id=pk)
            answers = Answer.objects.all().filter(video_id=pk)
            course = Course.objects.get(pk=course_id)
            questions_answer_list = list(zip(questions, answers))
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


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = UpdateVideoForm
    template_name = 'courseHandler/video/update.html'

    def form_valid(self, form):
        form.instance.save()
        pk = str(form.instance.course_id)
        return redirect('courseHandler:course-upload-video', pk)


class CourseCreate(LoginRequiredMixin, CreateView):
    template_name = 'courseHandler/course/create.html'

    form_class = CourseForm
    success_url = reverse_lazy('courseHandler:course-list')
    success_message = "The course was delete successfully"

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
        all_courses = Course.objects.filter(category=self.object.category, price__range=(min_price, max_price), is_active='True')[:4]
        # ids = [course.pk for course in userCourses]
        course_no_follow = [course for course in all_courses if course.id != self.object.id]
        videos_count = len(Video.objects.filter(course_id=self.object.id))
        context['couseList'] = course_no_follow
        # context['couseList'] = all_courses
        context['reviews'] = Review.objects.filter(course_id=self.object.id).select_related('student')[:5]
        if self.request.user.is_authenticated:
            check_follow = FollowCourse.objects.filter(course_id=self.object.id, student_id=self.request.user.id)
            if check_follow:
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
    success_message = "The course was delete successfully"

    def dispatch(self, request, *args, pk, **kwargs):
        course = Course.objects.get(id=pk)
        if not teacher_is_authorized(request, pk) or course.is_active:
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class CourseUpdate(UpdateView):
    model = Course
    template_name = 'courseHandler/course/update.html'
    success_url = reverse_lazy('courseHandler:course-list')
    form_class = CourseForm

    def dispatch(self, request, *args, pk, **kwargs):
        if not teacher_is_authorized(request, pk):
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class CourseList(ListView):
    model = Course
    template_name = 'courseHandler/course/search_result.html'


def CourseListView(request):
    if not request.user.is_authenticated:
        return redirect('homepage')

    if request.user.usertype.type == 'student':
        courses = FollowCourse.objects.all().filter(student_id=request.user.id).select_related('course')
        courses = [e.course for e in courses]
    else:
        courses = Course.objects.all().filter(author_id=request.user.id)
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
            qq = self.model.objects.filter(title__icontains=sstring)
        elif "Author" in where:
            qq = self.model.objects.filter(author__username__icontains=sstring)
        else:
            qq = self.model.objects.filter(category__icontains=sstring)
        return qq

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
