from django import forms
from .models import Message
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
