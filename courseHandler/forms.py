from django import forms
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from courseHandler.models import Course


class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = ('title', 'description', 'category','price', 'creation_date')

    #title = forms.CharField(help_text='Title')
    #description = forms.CharField(help_text='Description')
    #category = forms.CharField(max_length=64, help_text='Category')
    #image = forms.ImageField(blank=True, upload_to='album_logos', width_field=1920, height_field=1080)
    #price = forms.IntegerField()
    #creation_date = forms.DateInput()