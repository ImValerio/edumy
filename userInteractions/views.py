# Create your views here.
import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import UpdateView, DeleteView

from Edumy.settings import MEDIA_URL
from courseHandler.models import Video, FollowCourse
from notifications.signals import notify
from courseHandler.models import Video, Course
from courseHandler.views import teacher_is_authorized
from userAuth.models import UserType
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer, Review
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.forms.models import model_to_dict
from django.contrib import messages


def QuestionList(request, video):
    video = Video.objects.get(id=video)
    if teacher_is_authorized(request, video.course_id):
        context = {}
        answer_list = Answer.objects.filter(video_id=video)
        question_list = Question.objects.filter(video_id=video)
        ids = [answer.question_id for answer in answer_list]  # id che vogliamo escludere dalle question
        question_no_answer = [question for question in question_list if
                              question.id not in ids]  # seleziono le question che non hanno una risposta

        paginator = Paginator(question_no_answer, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        context["course_id"] = video.course_id
        context["video_id"] = video.id
        return render(request, "userInteractions/question/list.html", context)
    return HttpResponseRedirect('/')


class AnswerUpdate(UpdateView):
    model = Answer
    template_name = 'userInteractions/answer/update.html'
    form_class = AnswerForm

    def dispatch(self, request, *args, pk, **kwargs):
        answer = Answer.objects.get(id=pk)
        video = Video.objects.get(id=answer.video_id)
        if not teacher_is_authorized(request, video.course_id):
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        video = Video.objects.get(id=self.object.video_id)
        return reverse("courseHandler:course-upload-video-detail",
                       kwargs={'course_id': video.course_id, 'pk': self.object.video_id})


def listing_reviews(request):
    review_list = Review.objects.all()
    paginator = Paginator(review_list, 5)
    page_number = request.GET.get('page')
    data = False
    if paginator.num_pages >= int(page_number):
        page_obj = list(paginator.get_page(page_number).object_list)
        data = [model_to_dict(e) for e in page_obj]  # Converto gli oggetti di tipo Review in dizionari
        for review in data:
            review['img'] = MEDIA_URL+'/'+UserType.objects.values_list('image', flat=True).get(id=int(review['student']))
            review['student'] = User.objects.values_list('username', flat=True).get(id=int(review['student']))

        max_page = paginator.num_pages == int(page_number)

    return JsonResponse({'page_obj': data, 'max_page': max_page})


def listing_question_answer(request):
    pk = int(request.GET.get('video'))
    questions = Question.objects.all().filter(video_id=pk)
    answers = Answer.objects.all().filter(video_id=pk)
    questions_answer_list = list(zip(questions, answers))
    paginator = Paginator(questions_answer_list, 5)
    page_number = request.GET.get('page')

    data = False
    max_page = True
    if paginator.num_pages >= int(page_number):
        page_obj = list(paginator.get_page(page_number).object_list)
        data = []
        for qa in page_obj:
            data.append([model_to_dict(qa[0]), model_to_dict(qa[1])])

        max_page = paginator.num_pages == int(page_number)

    return JsonResponse({'page_obj': data, 'max_page': max_page})


@require_POST
def add_answer(request, video_id, question_id):
    course_id = (get_object_or_404(Video, id=video_id)).course_id
    if course_id and teacher_is_authorized(request, course_id):
        json_data = json.loads(request.body)
        Answer.objects.create(author_id=request.user.id, video_id=video_id, question_id=question_id,
                              body=json_data['answer'])
        return JsonResponse({'msg': 'Answer added'})

    return HttpResponseBadRequest()


@require_GET
def delete_answer(request, answer_id):
    video_id = Answer.objects.get(id=answer_id).video_id
    course_id = Video.objects.get(id=video_id).course_id
    if teacher_is_authorized(request, course_id):
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.delete()
            return HttpResponse()
        except:
            return HttpResponseBadRequest()

    return render(request, 'homepage.html')

@require_GET
def delete_question(request, question_id):
    video_id = Question.objects.get(id=question_id).video_id
    course_id = Video.objects.get(id=video_id).course_id
    print(question_id)
    if teacher_is_authorized(request, course_id):
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            return HttpResponse()
        except:
            return HttpResponseBadRequest()

    return render(request, 'homepage.html')

