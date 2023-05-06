from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('home', views.home),
    path('registration', views.registration, name='registration'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
]
