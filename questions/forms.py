from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Теги (через запятую)',
        required=True,
        help_text='Например: python, django, web'
    )

    class Meta:
        model = Question
        fields = ('title', 'text')

    def clean_tags_input(self):
        tags_str = self.cleaned_data.get('tags_input')
        if not tags_str.strip():
            raise forms.ValidationError('Укажите хотя бы один тег.')
        return tags_str

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            
        tags_str = self.cleaned_data.get('tags_input')
        tag_names = [name.strip().lower() for name in tags_str.split(',') if name.strip()]
        
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
            
        question.tags.set(tags)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)