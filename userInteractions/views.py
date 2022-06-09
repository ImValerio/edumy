
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            formAnswer = AnswerForm(request.POST, request.FILES)
            if formAnswer.is_valid():
                instance = formAnswer.save(commit=False)
                instance.author_id = request.user.id
                instance.question_id = question
                instance.video_id = video
                instance.save()
                return HttpResponse("You have created a answer", content_type='text/plain')
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