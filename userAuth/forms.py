from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field
from crispy_forms.helper import FormHelper
from userAuth.models import UserType


class UserSignup(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserType
        fields = ('username', 'first_name', 'image', 'last_name', 'email', 'password1', 'password2', 'type')

    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name = forms.CharField(max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64,
                             help_text='Enter a valid email address')
    type = forms.ChoiceField(choices=(
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('''<h1>Signup</h1>'''),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6'),
                Column('password2', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-6'),
                Column('type', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Row(
                Submit('submit', 'Submit', css_class="btn btn-success"),
                css_class=""
            ),
        )


class UserUpdate(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'


    """layout = Layout(Fieldset(
        Field('first_name'),
        Field('last_name'),
        Field('username'),
        Field('email'),
        Field('type'),
    ))
    layout.insert(3, HTML(""<a href="{% url 'userAuth:password_change' %}">Change password</a>""))

    helper.layout = layout """

    class Meta:
        model = UserType
        fields = ('username', 'image', 'first_name', 'last_name', 'email', 'type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('''<h1>Update user</h1>'''),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-8'),
                Column('type', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Submit('submit', 'Save' ,css_class="btn btn-success"),
                HTML('''
                <div class="d-flex w-75 justify-content-around">
                    <div>
                        <a class="btn btn-info" href="{% url 'userAuth:password_change' %}">Change password</a>
                    </div>
                    <div class="">    
                        <button class="btn btn-danger" data-toggle="modal" data-target="#exampleModal" id="del-modal" >DELETE ACCOUNT</button>
                    </div>
                </div>
                '''),
                css_class=""
            ),
        )