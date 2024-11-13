from tkinter.messagebox import QUESTION

from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from app.models import Question

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
    question_obj = paginate(QUESTIONS, request, per_page=3)
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


def one_question(request, question_id):
    question = None
    for q in QUESTIONS:
        if q['id'] == question_id:
            question = q
            break
    if not question:
        return render(request, 'base.html')

    relevant_answers = []
    for answer in ANSWERS:
        if answer['id'] == question_id:
            relevant_answers.append(answer)

    answer_obj = paginate(relevant_answers*30,request, per_page=3)
    context = {'question': question, 'answer_obj': answer_obj, 'is_main_page': False}
    return render(request, 'one_question.html', context)


def ask(request):
    return render(request, 'ask.html')

def tags(request, tag):

    filtered_questions = []
    for q in QUESTIONS:
        if tag in q['tags']:
            filtered_questions.append(q)

    tag_obj = paginate(filtered_questions,request, per_page=3)

    context = {
        'tag': tag,
        'tag_obj': tag_obj
    }
    return render(request, 'tags.html', context)


def signup(request):
    return render(request, 'signup.html')


def logout(request):
    return redirect('index')

def answer(request):
    return render(request, 'answer.html')








def Profile_list(request):
    questions = Question.objects.all().order_by()
    page = paginate(questions, request, per_page=10)
    return render(request, 'Profile_list.html', {'page_obj': page})

def Profile_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'Profile_detail.html', {'question': question})