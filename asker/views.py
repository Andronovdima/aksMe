from django.shortcuts import render, redirect , reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from faker import Faker
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from asker.models import Profile , Question, Tag

from asker.forms import LoginForm , RegistrationForm, QuestionForm

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def index(request):
    questions_list = Question.objects.new()
    objects_page = paginate(questions_list, request, 4)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    # questionTags = Tag.objects.questions()
    main = {}
    main['is_login'] = 0
    main['questions'] = objects_page
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags
    if request.user.is_authenticated:
        main['username'] = request.user.username
        main['is_login'] = 1
    return render(request, 'index.html', context=main)


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            user = auth.authenticate(**cdata)
            if user is not None:
                auth.login(request, user)
                return redirect('/')  # TODO: правильные редиректы
            form.add_error(None, 'no such user')
    else:
        form = LoginForm()
    flag = 0
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    return render(request, 'login.html', {
        'form': form,
        'is_login': flag,
        'users_top': users_top,
        'popular_tags': popular_tags
    })


def logout_view(request):
        logout(request)
        return redirect('/')


def base (request):
    return render(request , 'base.html' , {})


def question(request, id):
    question = get_object_or_404(Question, pk=id)
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
    if request.user.is_authenticated:
        main['username'] = request.user.username
        main['is_login'] = 1
    return render(request, 'question.html', context = main)

@login_required
def ask(request):
    if request.POST:
        form = QuestionForm(
            request.user.profile,
            data=request.POST)
        if form.is_valid():
            q = form.save()
            return redirect(reverse(
                'question', kwargs={
                    'qid': q.pk
                }
            ))
    else:
        form = QuestionForm(request.user.profile)
        flag = 0
        username = 'nones'
        if request.user.is_authenticated:
            flag = 1
            username = request.user.username
        users_top = Profile.objects.user_top()
        popular_tags = Tag.objects.popular_tags()

        return render (request, 'ask.html', {'is_login': flag , 'users_top' : users_top , 'popular_tags' : popular_tags,
                                             'username': username, 'form': form})


def settings(request):
    flag = 0
    username = 'none'
    if request.user.is_authenticated:
        flag = 1
        username = request.user.username
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()

    return render(request, 'settings.html' , {'is_login' : flag , 'users_top' : users_top ,
                                              'popular_tags' : popular_tags,
                                              'username': username
                                              })


def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            if cdata['password'] != cdata['repeat_password']:
                form.add_error(None, 'password and repeat password is not equal')
            else:
                try:
                    user = User.objects.get(username=cdata['username'])
                    form.add_error(None, 'user with this login existed yet')
                except User.DoesNotExist:
                    user = User.objects.create_user(cdata['username'], cdata['email'], cdata['password'])
                    return redirect('/')  # TODO: правильные редиректы
    else:
        form = RegistrationForm()
    flag = 0
    username = 'none'
    if request.user.is_authenticated:
        flag = 1
        username = request.user.username
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    return render(request, 'register.html', {'is_login': flag , 'users_top': users_top, 'popular_tags' : popular_tags,
                                             'username': username, 'form': form})





def paginate(objects_list, request, page_size=10):
    paginator = Paginator(objects_list, page_size)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)

    return objects_page


def tag(request, tagname):
    tag = get_object_or_404(Tag, tagname=tagname)
    questions = Tag.objects.questions(tag)
    questions = paginate (questions, request, 5)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main = {}
    main['questions'] = questions
    main['is_login'] = 0
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags
    main['tagname'] = tagname
    if request.user.is_authenticated:
        main['is_login'] = 1
        main['username'] = request.user.username
    return render(request, 'index.html', context=main)


def hot(request):
    questions = Question.objects.hot()
    questions = paginate (questions, request ,5)
    users_top = Profile.objects.user_top()
    popular_tags = Tag.objects.popular_tags()
    main = {}
    main['questions'] = questions
    main['is_login'] = 0
    main['users_top'] = users_top
    main['popular_tags'] = popular_tags
    if request.user.is_authenticated:
        main['username'] = request.user.username
        main['is_login'] = 1
    return render(request, 'index.html', context=main)


def addlike_question(request, qid):
    question = Question.objects.get(id=qid)
