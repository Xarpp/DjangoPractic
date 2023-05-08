from account.auth_backends import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create random password
            user = form.save(commit=False)

            user.is_active = False

            raw_password = User.objects.make_random_password(length=8)
            user.set_password(raw_password)
            # Activate from E-mail

            user.save()
            send_activation_email(request, user, raw_password)

            return redirect('/account_activation_sent')
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


def activation_sent(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print('Не прошло')
        user.is_active = True
        user.save()
        return redirect(reverse('login'))

    if not default_token_generator.check_token(user, token):
        return render(request, 'account_activate_success.html')

    return render(request, 'activation_invalid.html')


def send_activation_email(request, user, password):
    email_template_name = 'account_activation_email.html'
    subject = 'Активация аккаунта'
    c = {
        'email': user.email,
        'password': password,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    email = render_to_string(email_template_name, c)
    send_mail(subject, email, 'noreply@ваш_сайт.com', [user.email], fail_silently=False)
