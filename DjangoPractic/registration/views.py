from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
        
    return render(request, 'registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            error_message = 'Неверные почта или пароль'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})


def logout_user(request):
    logout(request)
    return redirect('/login')


def main(request):
    return HttpResponse('<h4>Будущая главная страница</h4>')


@login_required
def home(request):
    return render(request, 'home.html')
