from django import forms
from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from courseHandler.models import Course


class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_course_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = ('title', 'description', 'category', 'image' ,'price', 'creation_date')