# Create your views here.index'
from django.views.generic import DetailView, DeleteView, UpdateView
from courseHandler.forms import CreateVideo, SearchCourseForm
from courseHandler.models import Video, Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from courseHandler.forms import CourseForm
from userAuth.models import UserType
from userInteractions.forms import QuestionForm, AnswerForm
from userInteractions.models import Question, Answer

"""
class VideoUploadView(CreateView):
    model = Video
    form_class = CreateVideo
    template_name = 'courseHandler/video/upload-video.html'

"""
'''
class VideoUploadDetail(DetailView):
    model = Video
    template_name = 'courseHandler/video/upload-video-detail.html' 

    def get_context_data(self, **kwargs):
        context = super(VideoUploadDetail, self).get_context_data(**kwargs)
        form = QuestionForm()
        context['form'] = form
        return context
        '''

def VideoUpUploadDetail(request, course_id, pk):
    if request.user.is_authenticated:
        print(request.user)
        if request.method == 'POST':
            formQuestion = QuestionForm(request.POST, request.FILES)
            if formQuestion.is_valid():
                instance = formQuestion.save(commit=False)
                instance.student_id = request.user.id
                instance.video_id = int(pk)
                instance.save()
                return HttpResponse("You have created a question", content_type='text/plain')
        else:
            formQuestion = QuestionForm()
            questions = Question.objects.all().filter(video_id=pk)
            answers = Answer.objects.all().filter(video_id=pk)
            questionsAnswerList = list(zip(questions, answers))
            video = Video.objects.get(pk=pk)
            context = {
                "formQuestion": formQuestion,
                "questionsAnswerList": questionsAnswerList,
                "video": video,
                "pk": pk
            }
            return render(request, 'courseHandler/video/upload-video-detail.html', context)
    else:
        return HttpResponseRedirect('/')


def VideoUploadView(request, pk):
    if request.user.is_authenticated:
        print(request.user)
        if request.method == 'POST':
            form = CreateVideo(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.course_id = int(pk)
                instance.save()
                return redirect('courseHandler:course-upload-video', pk)
        else:
            form = CreateVideo()
            videos = Video.objects.all().filter(course_id=pk)
            context = {
                "form": form,
                "videos": videos,
                "pk": pk
            }
            return render(request, 'courseHandler/video/upload-video.html', context)
    else:
        return HttpResponseRedirect('/')


class CourseCreate(LoginRequiredMixin, CreateView):
    template_name = 'courseHandler/course/create.html'
    success_url = reverse_lazy('homepage')
    form_class = CourseForm

    def form_valid(self, form):
        #author = get_object_or_404(UserType, pk=form.instance.author_id)
        #if author.type == "Teacher":
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)
        #else:
            #print("Tu non sei un teacher")

class CourseDetail(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courseHandler/course/detail.html"

class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courseHandler/course/delete.html'
    success_url = reverse_lazy('courseHandler:course-list')

class CourseUpdate(LoginRequiredMixin, UpdateView):
    model = Course
    template_name = 'courseHandler/course/update.html'
    success_url = reverse_lazy('courseHandler:course-list')
    form_class = CourseForm

class CourseList(ListView):
    model = Course
    template_name = 'courseHandler/course/list.html'

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


    """   def createCourse(request):
            if request.user.is_authenticated and request.user.type == "teacher":
                if request.method == 'POST':
                    form = CourseForm(request.POST, request.FILES)
                    if form.is_valid():
                        instance = form.save(commit=False)
                        instance.author_id = request.user.id
                        instance.save()
                        return redirect('courseHandler:course-create')
                else:
                    form = CourseForm()
                    context = {
                        "form": form,
                    }
                    return render(request, 'courseHandler/course/create.html', context)
            else:
                return HttpResponseRedirect('/') """
