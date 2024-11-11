from tkinter.messagebox import QUESTION

from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

questions = []
themes = {
    'будущем технологий': ['технологии', 'инновации', 'будущее'],
    'экологические проблемы': ['экология', 'окружающая среда', 'изменение климата'],
    'исторические события': ['история', 'прошлое', 'важные события'],
    'будущем искусственного интеллекта': ['ИИ', 'технологии', 'машинное обучение']
}
for i in range(1, 30):
    theme = list(themes.keys())[i % len(themes)]
    questions.append({
        'title': f'Вопрос #{i} Какое ваше мнение о {theme}?',
        'id': i,
        'text': f' Вопрос #{i} Что вы думаете о {theme}? Какие изменения в этой области могут произойти в ближайшее время и как они могут повлиять на нас?',
        'tags': themes[theme]
    })


# Create your views here.


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


def base(request):
    question_obj = paginate(questions, request, per_page=3)
    return render(request, 'base.html', {'question_obj': question_obj})


def main_authorized(request):
    paginator = Paginator(questions, 3)
    page_number = request.GET.get('page', 1)
    question_obj = paginator.get_page(page_number)
    return render(request, 'main_authorized.html', {'question_obj': question_obj})


def login(request):
    return render(request, 'login.html')


def setting(request):
    return render(request, 'setting.html')


def ask(request):
    return render(request, 'ask.html')


def signup(request):
    return render(request, 'signup.html')


def logout(request):
    return base(request)
