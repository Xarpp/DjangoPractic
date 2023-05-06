from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser


class Region(models.Model):
    name = models.CharField(max_length=255)


class Country(models.Model):
    name = models.CharField(max_length=255)


SEX = [
    (1, 'Мужской'),
    (2, 'Женский')
]

AFFILIATION = [
    (1, 'Научное сообщество'),
    (2, 'Министерство'),
    (3, 'Организация')
]

COUNTRY_CHOICES = Country.objects.values_list('id', 'name')

REGIONS_CHOICES = Region.objects.values_list('id', 'name')


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     first_name = models.CharField(max_length=30, null=True)
#     last_name = models.CharField(max_length=30, null=True)
#     patronymic = models.CharField(max_length=30, null=True, blank=True)
#     affiliation = models.PositiveIntegerField('affiliation', choices=AFFILIATION, default=1, null=True)
#     phone_number = PhoneNumberField(region='RU', null=True)
#     birth_date = models.DateField(null=True, blank=True)
#     sex = models.PositiveIntegerField('sex', choices=SEX, default=1, null=True)
#
#     class Meta:
#         verbose_name = 'Профиль пользователя'
#         verbose_name_plural = 'Профили пользователей'


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class CustomUserFields(AbstractBaseUser, PermissionsMixin):

    last_name = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    gender = models.PositiveIntegerField('Пол', choices=SEX, null=True)
    birth_date = models.DateField(null=True, blank=True)
    affiliation = models.PositiveIntegerField('Принадлежность', choices=AFFILIATION, null=True)
    phone_number = PhoneNumberField(region='RU', null=True)
    email = models.EmailField(unique=True)
    country = models.PositiveIntegerField('Страна', choices=COUNTRY_CHOICES, null=True, blank=True)
    region = models.PositiveIntegerField('Регион', choices=REGIONS_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Новый профиль пользователя'
        verbose_name_plural = 'Новые профили пользователей'
        abstract = False
