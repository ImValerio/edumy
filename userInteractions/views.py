
# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from notifications.signals import notify

from courseHandler.models import Video, Course
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer
from django.shortcuts import render, redirect


def QuestionList(request, video):
    context = {}
    answer_list = Answer.objects.all().filter(video_id=video)
    question_list = Question.objects.all().filter(video_id=video)
    ids = [answer.question_id for answer in answer_list] #id che vogliamo escludere dalle question
    question_no_answer = [question for question in question_list if question.id not in ids] #seleziono le question che non hanno una risposta
    context["list"] = question_no_answer
    return render(request, "userInteractions/question/list.html", context)

def AnswerCreate(request, question, video):
    if request.user.is_authenticated and request.user.usertype.type == 'teacher':
        if request.method == 'POST':
            formAnswer = AnswerForm(request.POST, request.FILES)
            if formAnswer.is_valid():
                instance = formAnswer.save(commit=False)
                instance.author_id = request.user.id
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
            formAnswer = AnswerForm()
            context = {
                "formAnswer": formAnswer,
                "question": question,
                "video": video
            }
            return render(request, 'userInteractions/answer/create.html', context)
    else:
        return HttpResponseRedirect('/')