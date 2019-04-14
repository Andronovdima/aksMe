from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    questions_list = [
        {"name": "my best question1", "id": 1},
        {"name": "my best question2", "id": 2},
        {"name": "my best question3", "id": 3},

    ]
    return render (request , 'index.html' , {
        "questions": questions_list,
    })

def login (request):
    return render(request , 'login.html' , {})

def base (request):
    return render(request , 'base.html' , {})

def question(request, id):
    return render(request, 'question.html', {})

def ask (request):
    return render(request, 'ask.html' , {})

def settings (request):
    return render(request, 'settings.html' , {})

def login (request):
    return render(request , 'login.html' , {})

def register (request):
    return render(request , 'register.html' , {})
#
# def hot (request)
#     return
#
# def tag (request)
#     return
# Create your views here.
