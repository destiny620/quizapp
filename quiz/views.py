from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import addQuestionform
from django.views.generic import CreateView
import random


# Create your views here.

def home(request):
    return render(request, 'home.html')

def quiz(request):
    if request.method == 'POST':
        print(request.POST)
        questions = Question.objects.all()
        
        score = 0
        correct = 0
        wrong = 0
        total = 0

        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.answer)
            print()
            if q.answer == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1

        percentage = score/(total*10) * 100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong': wrong,
            'total': total,
            'percentage': percentage
        }

        return render(request, 'result.html', context)
    else:
        questions = Question.objects.all()
        return render(request, 'quiz.html', {'questions': questions})
    
class AddQuesView(CreateView):
    model = Question
    form_class = addQuestionform
    template_name = 'add_ques.html'
    #fields = '__all__'
    #fields = ('title', 'content')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password not the same')
            return redirect('register')
        
    else:
        return render(request, 'register.html')
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')