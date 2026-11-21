from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .utils import paginate
from .models import Question, Answer, QuestionLike, AnswerLike
from .forms import QuestionForm, AnswerForm


# ==========================================
# DZ3: Основные страницы (не трогаем)
# ==========================================

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


# ==========================================
# DZ4: Добавление вопроса и ответа
# ==========================================

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('questions:question', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})


@login_required
def add_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            # Редирект с якорем на конкретный ответ
            return redirect(f'/question/{pk}/#answer-{answer.pk}')
    return redirect('questions:question', pk=pk)


# ==========================================
# DZ4: AJAX запросы (Лайки и правильный ответ)
# ==========================================

@login_required
def ajax_like_question(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    
    question = get_object_or_404(Question, pk=pk)
    like, created = QuestionLike.objects.get_or_create(user=request.user, question=question)
    
    if not created:
        like.delete()  # Убираем лайк при повторном нажатии
    else:
        like.value = 1
        like.save()
        
    new_rating = QuestionLike.objects.filter(question=question).aggregate(Sum('value'))['value__sum'] or 0
    return JsonResponse({'rating': new_rating, 'user_liked': not created})


@login_required
def ajax_like_answer(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    
    answer = get_object_or_404(Answer, pk=pk)
    like, created = AnswerLike.objects.get_or_create(user=request.user, answer=answer)
    
    if not created:
        like.delete()
    else:
        like.value = 1
        like.save()
        
    new_rating = AnswerLike.objects.filter(answer=answer).aggregate(Sum('value'))['value__sum'] or 0
    return JsonResponse({'rating': new_rating, 'user_liked': not created})


@login_required
def ajax_mark_correct(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)
    
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer_id')
    
    question = get_object_or_404(Question, pk=question_id)
    
    # Проверка авторства (ТЗ 8.1)
    if question.author != request.user:
        return JsonResponse({'error': 'Только автор вопроса может отметить правильный ответ'}, status=403)
    
    answer = get_object_or_404(Answer, pk=answer_id, question=question)
    
    # Снимаем правильность со всех остальных ответов этого вопроса
    Answer.objects.filter(question=question).update(is_correct=False)
    answer.is_correct = True
    answer.save()
    
    return JsonResponse({'success': True, 'answer_id': answer.pk})