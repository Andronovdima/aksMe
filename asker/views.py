from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from faker import Faker
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from asker.models import Profile , Question, Tag

# from asker.forms import LoginForm

from django.contrib import auth

def index(request):

    questions_list = Question.objects.new()
    objects_page  = paginate(questions_list , request , 4)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main = {}
    main ['questions'] = objects_page
    main ['is_login'] = 0
    main ['users_top'] = users_top
    main ['popular_tags'] = popular_tags
    return render (request , 'index.html' , context = main)




def login (request):
    flag = 0;
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'login.html', {'is_login': flag,
                                          'users_top': users_top,
                                          'popular_tags': popular_tags})
# def login_prepod (request):
#     if (request.POST):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_date
#             user = auth.authetificate(**cleaned_data)
#             if user is not None:
#                 auth.login(request , user)
#                 return redirect ('/')
#
#     else:
#         form = LoginForm()
#     return redirect('/')
#

def base (request):
    return render(request , 'base.html' , {})

def question(request, id):
    question = get_object_or_404(Question, pk = id)
    flag = 1;
    answers = Question.objects.answers(question)
    answers = paginate(answers, request, 30)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main = {}
    main['question'] = question
    main['answers'] = answers
    main['is_login'] = 0
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags

    return render(request, 'question.html', context = main)

def ask (request):
    flag = 1;
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()

    return render (request, 'ask.html', {'is_login' : flag , 'users_tops' : users_top , 'popular_tags' : popular_tags})


def settings (request):
    flag = 1;
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'settings.html' , {'is_login' : flag , 'users_tops' : users_top , 'popular_tags' : popular_tags})


def register (request):
    flag = 0;
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'register.html', {'is_login' : flag , 'users_tops' : users_top , 'popular_tags' : popular_tags})





def paginate(objects_list, request, page_size=10):
    paginator = Paginator(objects_list, page_size)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)

    return objects_page
#

def tag(request, tagname):
    flag = 1;
    tag = get_object_or_404(Tag,tagname=tagname)
    questions = Tag.objects.questions(tag)
    questions = paginate (questions, request,5)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main = {}
    main['questions'] = questions
    main['is_login'] = flag
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags
    main['tagname'] = tagname
    return render(request,'index.html',context=main)

def hot(request):
    questions = Question.objects.hot()
    questions = paginate (questions, request ,5)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main =  {}
    main['questions'] = questions
    main['is_login'] = 0
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags
    return render(request,'index.html',context=main)