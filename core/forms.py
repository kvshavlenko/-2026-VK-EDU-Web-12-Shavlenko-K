from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

def validate_avatar(file):
    if file.size > 2 * 1024 * 1024:
        raise ValidationError('Размер файла не должен превышать 2 МБ.')
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    ext = file.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Неподдерживаемый формат. Разрешены: jpg, jpeg, png, gif.')

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(max_length=150, required=True, label='Никнейм')
    avatar = forms.ImageField(required=False, label='Аватар', validators=[validate_avatar])

    class Meta:
        model = Profile
        fields = ('avatar',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('Этот никнейм уже занят.')
        return username

    def save(self, commit=True):
        # 1. Сохраняем изменения в модели User
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        # 2. Сохраняем модель Profile (super().save обновит существующий instance, а не создаст новый!)
        return super().save(commit=commit)