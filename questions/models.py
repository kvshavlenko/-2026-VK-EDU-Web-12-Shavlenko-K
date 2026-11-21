from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from core.models import Tag


class QuestionManager(models.Manager):
    def new_questions(self):
        return (
            self.select_related('author')
            .prefetch_related('tags')
            .annotate(
                answers_count=Count('answers', distinct=True),
                likes=Sum('questionlike__value'),
            )
            .order_by('-created_at')
        )

    def hot_questions(self):
        return (
            self.select_related('author')
            .prefetch_related('tags')
            .annotate(
                rating=Sum('questionlike__value'),
                answers_count=Count('answers', distinct=True),
                likes=Sum('questionlike__value'),
            )
            .order_by('-rating', '-created_at')
        )

    def by_tag(self, tag_name):
        return (
            self.filter(tags__name=tag_name)
            .select_related('author')
            .prefetch_related('tags')
            .annotate(
                answers_count=Count('answers', distinct=True),
                likes=Sum('questionlike__value'),
            )
            .order_by('-created_at')
        )


class AnswerManager(models.Manager):
    def with_likes(self):
        return (
            self.select_related('author')
            .annotate(likes=Sum('answerlike__value'))
        )


class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('question', kwargs={'pk': self.pk})

    def answers_with_likes(self):
        """Выборка ответов вопроса с лайками и сортировкой."""
        return (
            Answer.objects.with_likes()           # 1. Сначала вызываем метод менеджера (он вернет QuerySet с аннотацией)
            .filter(question=self)                # 2. Потом фильтруем по текущему вопросу (аннотация сохранится!)
            .order_by('-is_correct', 'created_at')
        )


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'Ответ на вопрос "{self.question.title}"'


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    value = models.IntegerField(verbose_name='Значение')

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    value = models.IntegerField(verbose_name='Значение')

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'