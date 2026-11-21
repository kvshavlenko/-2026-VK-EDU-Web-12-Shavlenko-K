from django.shortcuts import render, get_object_or_404
from .utils import paginate
from .models import Question


def index(request):
    questions = Question.objects.new_questions()
    page_obj = paginate(questions, request, per_page=20)
    return render(request, 'questions/index.html', {'page_obj': page_obj, 'empty': not questions.exists()})


def hot(request):
    questions = Question.objects.hot_questions()
    page_obj = paginate(questions, request, per_page=20)
    return render(request, 'questions/hot.html', {'page_obj': page_obj, 'empty': not questions.exists()})


def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions, request, per_page=20)
    return render(request, 'questions/tag.html', {'page_obj': page_obj, 'tag_name': tag_name, 'empty': not questions.exists()})


def question(request, pk):
    q = get_object_or_404(Question, pk=pk)
    answers = q.answers_with_likes()
    page_obj = paginate(answers, request, per_page=30)
    return render(request, 'questions/question.html', {'question': q, 'page_obj': page_obj, 'empty': not answers.exists()})


def ask(request):
    return render(request, 'questions/ask.html')