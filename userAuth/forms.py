from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.layout import Submit, HTML, Fieldset, Field
from crispy_forms.helper import FormHelper, Layout
from userAuth.models import UserType


class UserSignup(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserType
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'type')

    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name = forms.CharField(max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64,
                             help_text='Enter a valid email address')
    type = forms.ChoiceField(choices=(
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ))


class UserUpdate(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

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
        fields = ('username', 'first_name', 'last_name', 'email', 'type')

    type = forms.ChoiceField(choices=(
            ('student', 'Student'),
            ('teacher', 'Teacher')
    ))
