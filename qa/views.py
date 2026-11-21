from django.shortcuts import render
from .utils import paginate
from .data import QUESTIONS, ANSWERS, TAGS

def index(request):
    page_obj = paginate(QUESTIONS, request, per_page=10)
    return render(request, 'qa/index.html', {'page_obj': page_obj})

# Принимаем tag_name из URL
def tag(request, tag_name):
    # Пока просто передаем имя тега в шаблон, чтобы оно отображалось
    page_obj = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'qa/tag.html', {'page_obj': page_obj, 'tag_name': tag_name})

# Принимаем pk (id вопроса) из URL
def question(request, pk):
    page_obj = paginate(ANSWERS, request, per_page=3)
    return render(request, 'qa/question.html', {'page_obj': page_obj, 'question_id': pk})
ы
def ask(request):
    return render(request, 'qa/ask.html')

def login_view(request):
    return render(request, 'qa/login.html')

def signup(request):
    return render(request, 'qa/signup.html')

def profile(request):
    return render(request, 'qa/profile.html')