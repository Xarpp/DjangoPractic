from django.utils import timezone
from django import forms
from .models import CustomUserFields, SEX, AFFILIATION, COUNTRY_CHOICES, REGIONS_CHOICES


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


# class SignUpForm(UserCreationForm):
#     last_name = forms.CharField(
#         max_length=30,
#         label='Фамилия',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'last_name',
#                 'name': 'last_name',
#                 'placeholder': 'Введите фамилию',
#             })
#
#     )
#     patronymic = forms.CharField(
#         max_length=30,
#         label='Отчество (при наличии)',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'patronymic',
#                 'name': 'patronymic',
#                 'placeholder': 'Введите отчество',
#             })
#     )
#     affiliation = forms.ChoiceField(
#         label='Принадлежность',
#         error_messages={'required': ''},
#         choices=AFFILIATION
#     )
#     sex = forms.ChoiceField(
#         label='Пол',
#         choices=SEX,
#         error_messages={'required': ''}
#     )
#     birth_date = forms.DateField(
#         label='Дата рождения',
#         required=True,
#         error_messages={'required': ''},
#         widget=MyDateInput({
#             'class': 'form-control '
#         }))
#     phone_number = forms.CharField(
#         max_length=15,
#         label='Номер телефона',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'phone_number',
#                 'name': 'phone_number',
#                 'placeholder': '+7XXXXXXXXXX',
#                 'required': 'True'
#             })
#     )
#     password1 = forms.CharField(
#         label='Пароль',
#         strip=False,
#         widget=forms.PasswordInput(attrs={
#             'autocomplete': 'new-password',
#             'placeholder': 'Не менее 8 символов...'
#         }),
#         help_text=None
#     )
#
#     username = forms.CharField(
#         label='Имя пользователя',
#         help_text=None,
#     )
#
#     country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Выберите страну')
#
#     checkbox = forms.BooleanField(label='Согласие на обработку персональных данных')
#     checkbox1 = forms.BooleanField(label='Согласие на публичную оферту')
#     checkbox2 = forms.BooleanField(label='Политика безопасности и работа с персональными данными')
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'patronymic', 'sex', 'birth_date', 'affiliation',
#                   'phone_number', 'email', 'password1')


class RegistrationForm(forms.ModelForm):
    last_name = forms.CharField(label='Фамилия')
    first_name = forms.CharField(label='Имя')
    middle_name = forms.CharField(label='Отчество (При наличии)', required=False)
    gender = forms.ChoiceField(label='Пол', choices=SEX)
    birth_date = forms.DateField(label='Дата рождения', widget=MyDateInput({
             'class': 'form-control '}))
    affiliation = forms.ChoiceField(label='Принадлежность', choices=AFFILIATION)
    phone_number = forms.CharField(label='Номер телефона')
    email = forms.EmailField(label='E-mail')
    country = forms.ChoiceField(label='Страна', choices=COUNTRY_CHOICES)
    region = forms.ChoiceField(label='Регион', choices=REGIONS_CHOICES)
    checkbox = forms.BooleanField()
    checkbox1 = forms.BooleanField(label='Согласие на публичную оферту')
    checkbox2 = forms.BooleanField(label='Политика безопасности и работа с персональными данными')

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError('Дата рождения не может быть больше текущей даты')

    class Meta:
        model = CustomUserFields
        fields = ('last_name', 'first_name', 'middle_name', 'gender', 'birth_date', 'affiliation', 'phone_number',
                  'email', 'country', 'region')
