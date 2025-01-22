from tkinter.messagebox import QUESTION

import page
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.dispatch import receiver
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from app import utils, models
from app.models import Question, Answer, Profile, Tag

themes = {
    'будущем технологий': ['технологии', 'инновации', 'будущее'],
    'экологические проблемы': ['экология', 'окружающая среда', 'изменение климата'],
    'исторические события': ['история', 'прошлое', 'важные события'],
    'будущем искусственного интеллекта': ['ИИ', 'технологии', 'машинное обучение']
}

QUESTIONS = []
for i in range(1, 30):
    theme = list(themes.keys())[i % len(themes)]
    QUESTIONS.append({
        'title': f'Вопрос #{i} Какое ваше мнение о {theme}?',
        'id': i,
        'text': f' Вопрос #{i} Что вы думаете о {theme}? Какие изменения в этой области могут произойти в ближайшее время и как они могут повлиять на нас?',
        'tags': themes[theme]
    })

ANSWERS = []
for i in range(1, 30):
    theme = list(themes.keys())[i % len(themes)]
    ANSWERS.append({
        'title': f'Ответ на вопрос #{i} по теме: {theme}',
        'id': i,
        'theme': theme,
        'response': f'Ответ #{i} на тему {theme}: Ответ на вопрос о возможных изменениях в области {theme} будет заключаться в том, что новые технологии могут существенно изменить жизнь общества, улучшив качество жизни в различных аспектах.'
    })


# Create your views here.

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your login here'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def index(request):
    question_list = Question.objects.all()

    paginator = Paginator(question_list, 3)
    page_number = request.GET.get('page')
    question_obj = paginator.get_page(page_number)

    context = {'question_obj': question_obj, 'is_main_page': True}
    return render(request, 'index.html', context)



def main_authorized(request):
    question_obj = paginate(QUESTIONS, request, per_page=3)
    context = {'question_obj': question_obj, 'is_main_page': True}
    return render(request, 'main_authorized.html', context)


def login(request):
    return render(request, 'login.html')

def question(request):
    return render(request, 'question.html')

def setting(request):
    return render(request, 'setting.html')


def one_question(request: HttpRequest, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question=question)

    context = {
        'question': question,
        'answers': answers,
        'is_auth': False,
        'if_empty': {
            'title': 'So far there are no answers.',
            'description': 'You can be the first to answer!'
        },
        'top_users': models.Profile.objects.get_top_users(),
        'top_tags': models.Tag.objects.get_top_tags(count=7)
    }

    return render(request, 'one_question.html', context)

def ask(request):
    return render(request, 'ask.html')

def tags(request, tag):
    tag = get_object_or_404(Tag, name=tag)
    questions = Question.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'questions': questions,
    }

    return render(request, 'tags.html', context)


def signup(request):
    if request.method == "POST":
        login = request.POST.get("login")
        email = request.POST.get("email")
        nickname = request.POST.get("nickname")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        avatar = request.FILES.get("avatar")

        if password != repeat_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        try:
            user = User.objects.create_user(
                username=login,
                email=email,
                password=password
            )
            user.first_name = nickname
            user.save()

            authenticated_user = authenticate(username=login, password=password)
            if authenticated_user:
                login(request, authenticated_user)

            messages.success(request, "Registration successful.")
            return redirect("main_authorized")
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
            return render(request, "signup.html")

    return render(request, "signup.html")


def logout(request):
    return redirect('index')


def hot(request: HttpRequest):
    page = utils.paginate(models.Question.objects.get_top_questions(), request)
    context = {
        'questions': page['object_list'],
        'page': page,
        'is_auth': False,
        'if_empty': {
            'title': 'So far there are no questions.',
            'description': 'But you can ask your question!'
        },
        'top_users': models.Profile.objects.get_top_users(),
        'top_tags': models.Tag.objects.get_top_tags(count=7)
    }

    return render(request, 'hot.html', context)

def get_answers_for_question(question):
    answers = Answer.objects.filter(question=question)
    return answers

def Profile_list(request):
    questions = Question.objects.all().order_by()
    page = paginate(questions, request, per_page=10)
    return render(request, 'Profile_list.html', {'page_obj': page})

def Profile_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'Profile_detail.html', {'question': question})


def answer(request):
    return render(request, 'answer.html')

