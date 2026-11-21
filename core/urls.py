from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),       # Оставляем твое имя
    path('logout/', views.logout_view, name='logout'),  # Добавляем выход
    path('profile/', views.profile, name='profile'),    # Оставляем твое имя
]