from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Chat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'type', 'users')


class MessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'time', 'content', 'author', 'chat')


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'author', 'chat')

# class MessageSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Message
#         fields = ('id', 'time', 'text', 'author')
