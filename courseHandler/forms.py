from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from courseHandler.models import Course, Payment
from courseHandler.models import Video


class CreateVideo(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'UPLOAD'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Video
        fields = ['title', 'description', 'file']

class UpdateVideoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_course_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Video
        fields = ('title', 'description', 'file')



class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_course_crispy_form"
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Course
        fields = ('title', 'description', 'category', 'image' ,'price', 'creation_date')


class SearchCourseForm(forms.Form):

    CHOICE_LIST = [("Title","Cerca tra i corsi"), ("Author","Cerca tra gli autori"),
                   ("Category","Cerca tra le categorie")]
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_string = forms.CharField(label="Cerca qualcosa",max_length=100, min_length=3, required=True)
    search_where = forms.ChoiceField(label="Dove?", required=True, choices=CHOICE_LIST)


PAYMENTS_OPTIONS = [(method, method) for method in ["Paypal", "Paysafecard", "Credit card"]]

class PaymentsForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'BUY'))
    helper.inputs[0].field_classes = 'btn btn-success'
    class Meta:
        fields = ()
        model = Payment

    payments = forms.ChoiceField(choices = PAYMENTS_OPTIONS, help_text='select your payment method')