from django.urls import path

from userInteractions.views import QuestionList, AnswerCreate, listing_reviews

app_name = 'userInteractions'

urlpatterns = [
    path('reviews',listing_reviews, name='get-reviews'),
    path('question/list/<int:video>', QuestionList, name='question-list'),
    path('answer/<int:question>/<int:video>/create', AnswerCreate, name='answer-create'),
]