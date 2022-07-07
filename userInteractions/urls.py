from django.urls import path

from userInteractions.views import QuestionList, listing_reviews, listing_question_answer, add_answer, AnswerUpdate, \
    delete_answer

app_name = 'userInteractions'

urlpatterns = [
    path('question-answer',listing_question_answer, name='get-question-answer'),
    path('answer/<int:video_id>/<int:question_id>', add_answer, name='add-answer'),
    path('reviews',listing_reviews, name='get-reviews'),
    path('question/list/<int:video>', QuestionList, name='question-list'),
    path('answer/<int:pk>/update', AnswerUpdate.as_view(), name='answer-update'),
    path('answer/<int:answer_id>/delete', delete_answer, name='answer-delete'),
]