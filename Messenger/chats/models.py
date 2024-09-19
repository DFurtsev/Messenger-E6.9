from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    dialog = 'DIALOG'
    group_chat = 'GROUP_CHAT'

    CHAT_TYPES = [
        (dialog, 'Приватная беседа'),
        (group_chat, 'Групповой чат')
    ]
    type = models.CharField(max_length=255, choices=CHAT_TYPES, default=dialog)
    users = models.ManyToManyField(User, through='UserChat')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')


class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)




