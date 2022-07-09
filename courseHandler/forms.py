from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from courseHandler.models import Course, Payment
from courseHandler.models import Video
import datetime

class CreateVideo(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "create_video_crispy_form"
    helper.form_method = 'POST'

    class Meta:
        model = Video
        fields = ['title', 'description', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('description', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-6'),
                Submit('submit', 'UPLOAD', css_class="btn btn-success ml-1 col-md-1"),
                css_class="d-flex align-items-center"
            ),

        )



class UpdateVideoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "update_video_crispy_form"
    helper.form_method = 'POST'

    class Meta:
        model = Video
        fields = ('title', 'description', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('description', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-6'),
            ),
            Row(
                Submit('submit', 'Update', css_class="btn btn-success col-md-1"),
                css_class="d-flex justify-content-end"
            )

    )


class CourseForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "add_course_crispy_form"
    helper.form_method = 'POST'
    creation_date = forms.DateField(widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

    class Meta:
        model = Course
        fields = ('title', 'description', 'category', 'image', 'price', 'creation_date')

    categories = [('Programming', 'Programming'), ('Science', 'Science'), ('Sport', 'Sport'), ('Cooking', 'Cooking'), ('Language', 'Language')]
    sorted_categories = sorted(categories, key=lambda tup: tup[0])
    category = forms.ChoiceField(choices=sorted_categories, label='Categories',required=True)

    def clean_creation_date(self):
        date = self.cleaned_data['creation_date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('category', css_class='form-group col-md-6'),
                Column('image', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('price', css_class='form-group col-md-6'),
                Column('creation_date', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'description',
            Row(
                Submit('submit', 'Submit', css_class="btn btn-success col-md-1"),
                css_class="d-flex justify-content-end mr-1"
            )
        )

class SearchCourseForm(forms.Form):

    CHOICE_LIST = [("Title","Search among course"), ("Author","Search among author"),
                   ("Category","Search among category")]
    helper = FormHelper()
    helper.form_id = "search_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Cerca"))
    search_string = forms.CharField(label="Search somethings",max_length=100, min_length=3, required=True)
    search_where = forms.ChoiceField(label="Where?", required=True, choices=CHOICE_LIST)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('search_string', css_class='form-group'),
                Column('search_where', css_class='form-group'),
                Submit('submit', 'Submit', css_class="btn btn-success"),
                css_class='d-flex align-items-center'
            ),
        )

PAYMENTS_OPTIONS = [(method, method) for method in ["Paypal", "Paysafecard", "Credit card"]]

class PaymentsForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'BUY'))
    helper.inputs[0].field_classes = 'btn btn-success'
    class Meta:
        fields = ()
        model = Payment

    payments = forms.ChoiceField(choices = PAYMENTS_OPTIONS, help_text='select your payment method')