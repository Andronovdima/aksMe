from django import forms
from django.contrib import auth
from asker.models import Question
from django.contrib.auth.models import User
#
# # #django crispy forms
# # #django-widget-tweaks


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=16)
    email = forms.EmailField(max_length=16)
    password = forms.CharField(min_length=3, max_length=16)
    repeat_password = forms.CharField(min_length=3, max_length=16)


class QuestionForm(forms.ModelForm):
    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['title', 'text']
    title = forms.CharField(required=True)


def save(self, commit=True):
    cdata = self.cleaned_data
    question = Question(
        title=cdata['title'],
        text=cdata['text'],
        author_id=self.profile.profile_id
    )
    if commit:
        question.save()
    return question

