from django.contrib import admin
from .models import Question, Answer, QuestionLike, AnswerLike


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('tags', 'created_at')
    search_fields = ('title', 'text')
    inlines = [AnswerInline]
    raw_id_fields = ('author',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('text',)
    raw_id_fields = ('question', 'author')


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'value')
    search_fields = ('user__username', 'question__title')
    list_filter = ('value',)
    raw_id_fields = ('user', 'question')


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'value')
    search_fields = ('user__username', 'answer__text')
    list_filter = ('value',)
    raw_id_fields = ('user', 'answer')