
# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from courseHandler.models import Video
from notifications.signals import notify
from courseHandler.models import Video, Course
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer
from django.shortcuts import render, redirect



def QuestionList(request, video):
    context = {}
    answer_list = Answer.objects.filter(video_id=video)
    question_list = Question.objects.filter(video_id=video)
    ids = [answer.question_id for answer in answer_list] #id che vogliamo escludere dalle question
    question_no_answer = [question for question in question_list if question.id not in ids] #seleziono le question che non hanno una risposta
    context["list"] = question_no_answer
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