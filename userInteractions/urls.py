from django.urls import path

from userInteractions.views import QuestionList, AnswerCreate

app_name = 'userInteractions'

urlpatterns = [
    path('question/list/<int:video>', QuestionList, name='question-list'),
    path('answer/<int:question>/<int:video>/create', AnswerCreate, name='answer-create')

]