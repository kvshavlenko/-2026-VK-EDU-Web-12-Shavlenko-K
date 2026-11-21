from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from .forms import SignupForm, ProfileForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next', request.GET.get('next', '/'))
        
        if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
            next_url = '/'
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Неверный логин или пароль.')
            
    return render(request, 'core/login.html', {'next': request.GET.get('next', '/')})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def logout_view(request):
    next_url = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return redirect(next_url)

@login_required
def profile(request):
    # Берем СУЩЕСТВУЮЩИЙ профиль пользователя, чтобы обновить его, а не создавать новый
    profile_instance = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('core:profile')
    else:
        form = ProfileForm(instance=profile_instance, user=request.user)
        
    return render(request, 'core/profile.html', {'form': form})