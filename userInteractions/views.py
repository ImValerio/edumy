
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse

from courseHandler.models import Video
from userInteractions.forms import AnswerForm
from userInteractions.models import Question, Answer
from django.shortcuts import render


def QuestionList(request, video):
    context = {}
    answer_list = Answer.objects.all().filter(video_id=video)
    question_list = Question.objects.all().filter(video_id=video)
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
                return HttpResponse("You have created a answer", content_type='text/plain')
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