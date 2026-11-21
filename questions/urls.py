from django.urls import path
from . import views

# ЭТА СТРОКА КРИТИЧЕСКИ ВАЖНА! Она регистрирует пространство имён 'questions'
app_name = 'questions'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:pk>/', views.question, name='question'),
    path('question/<int:pk>/answer/', views.add_answer, name='add_answer'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    
    # AJAX маршруты
    path('ajax/like/question/<int:pk>/', views.ajax_like_question, name='ajax_like_question'),
    path('ajax/like/answer/<int:pk>/', views.ajax_like_answer, name='ajax_like_answer'),
    path('ajax/mark_correct/', views.ajax_mark_correct, name='ajax_mark_correct'),
]