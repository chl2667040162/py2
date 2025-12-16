from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Competition
from django.utils import timezone


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = [
            'name', 'description', 'sport_type', 'location',
            'start_date', 'end_date', 'max_participants',
            'status', 'is_public', 'registration_deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        registration_deadline = cleaned_data.get('registration_deadline')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("Дата окончания должна быть позже даты начала")

            if start_date < timezone.now():
                raise forms.ValidationError("Дата начала не может быть в прошлом")

        if registration_deadline and start_date:
            if registration_deadline > start_date:
                raise forms.ValidationError("Срок регистрации должен быть раньше даты начала")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию или месту...'})
    )
    sport_type = forms.ChoiceField(
        choices=[('', 'Все виды спорта')] + Competition.SPORT_TYPES,
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'Все статусы')] + Competition.STATUS_CHOICES,
        required=False
    )