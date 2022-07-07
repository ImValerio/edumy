# Create your views here.
import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from courseHandler.models import Video, FollowCourse
from notifications.signals import notify
from courseHandler.models import Video, Course
from courseHandler.views import teacher_is_authorized
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer, Review
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.forms.models import model_to_dict


def QuestionList(request, video):
    course_id = Video.objects.get(id=video).course_id
    if teacher_is_authorized(request, course_id):
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
        return render(request, "userInteractions/question/list.html", context)
    return HttpResponseRedirect('/')


def listing_reviews(request):
    review_list = Review.objects.all()
    paginator = Paginator(review_list, 5)
    page_number = request.GET.get('page')
    data = False
    if paginator.num_pages >= int(page_number):
        page_obj = list(paginator.get_page(page_number).object_list)
        data = [model_to_dict(e) for e in page_obj]  # Converto gli oggetti di tipo Review in dizionari
        for review in data:
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
        Answer.objects.create(author_id=request.user.id, video_id=video_id, question_id=question_id,body=json_data['answer'])
        return JsonResponse({'msg': 'Answer added'})

    return HttpResponseBadRequest()
