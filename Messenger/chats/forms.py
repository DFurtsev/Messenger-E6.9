from django import forms

from .models import Message, User
from django.core.exceptions import ValidationError


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Введите текст"

    class Meta:
        model = Message
        fields = [
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'avatar'
        ]

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if username is None or len(username) < 3:
            raise ValidationError({"username": "Никнейм должно быть больше 2 символов "})
        if first_name is None or len(first_name) < 3:
            raise ValidationError({"first_name": "Имя должно быть больше 2 символов "})
        if last_name is None or len(last_name) < 3:
            raise ValidationError({"second_name": "Фамилия должна быть больше 2 символов "})

        return cleaned_data

