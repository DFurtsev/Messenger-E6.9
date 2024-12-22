from datetime import datetime


from rest_framework import serializers
from .models import Message, Chat, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar')


class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'type', 'users')


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    time = serializers.DateTimeField(format="%d.%m.%y %H:%M")

    class Meta:
        model = Message
        fields = ('id', 'time', 'content', 'author', 'chat')


class MessagePostSerializer(serializers.ModelSerializer):
    # time = serializers.DateTimeField(format="%d.%m.%y %H:%M")

    class Meta:
        model = Message
        fields = ('content', 'author', 'chat')

