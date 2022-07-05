# Create your views here.
import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from courseHandler.models import Video
from notifications.signals import notify
from courseHandler.models import Video, Course
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer, Review
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.forms.models import model_to_dict


def QuestionList(request, video):
    context = {}
    answer_list = Answer.objects.filter(video_id=video)
    question_list = Question.objects.filter(video_id=video)
    ids = [answer.question_id for answer in answer_list]  # id che vogliamo escludere dalle question
    question_no_answer = [question for question in question_list if
                          question.id not in ids]  # seleziono le question che non hanno una risposta
    context["list"] = question_no_answer[:5]
    return render(request, "userInteractions/question/list.html", context)


def AnswerCreate(request, question, video):
    video_course = Video.objects.filter(pk=video).select_related('course')
    course_author_id = [c.course.author_id for c in video_course]
    if request.user.is_authenticated and request.user.id == course_author_id[0]:

        if request.method == 'POST':
            form_answer = AnswerForm(request.POST, request.FILES)
            if form_answer.is_valid():
                instance = form_answer.save(commit=False)
                instance.author_id = course_author_id[0]
                instance.question_id = question
                instance.video_id = video
                instance.save()
                sender = User.objects.get(id=request.user.id)
                question_row = Question.objects.get(id=question)
                recipient = User.objects.get(id=question_row.student_id)
                video_id = Video.objects.values_list('id').get(id=question_row.video_id)
                course_title = Course.objects.values_list('title').get(id=video_id[0])
                message = f"[{course_title[0]}] {request.user.first_name} answered your question"
                notify.send(sender, recipient=recipient, verb='Message',
                            description=message)
                return redirect('courseHandler:userInteractions:question-list', video)
        else:
            form_answer = AnswerForm()
            context = {
                "form_answer": form_answer,
                "question": question,
                "video": video
            }
            return render(request, 'userInteractions/answer/create.html', context)
    else:
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
