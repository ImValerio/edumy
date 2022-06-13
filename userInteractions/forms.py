from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from userInteractions.models import Question, Answer, Review


class QuestionForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_question_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Question
        fields = ['body']

class AnswerForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_answer_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'


    class Meta:
        model = Answer
        fields = ['body']

class ReviewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_answer_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Review
        fields = ['title', 'body', 'rating']