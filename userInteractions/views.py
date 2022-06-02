
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from userInteractions.forms import QuestionForm, AnswerForm
from userInteractions.models import Question, Answer
from django.shortcuts import render

def QuestionList(request, video):
    context = {}
    context["object_list"] = Question.objects.all().filter(video_id=video)
    return render(request, "userInteractions/question/list.html", context)

def AnswerCreate(request, question, video):
    if request.user.is_authenticated:
        print(request.user)
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


