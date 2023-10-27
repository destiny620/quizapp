from django.urls import path
from . import views
from .views import AddQuesView


urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz, name='quiz'),
    path("add_ques/", AddQuesView.as_view(), name="add_ques"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]