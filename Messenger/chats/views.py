from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessagePostSerializer


class ChatPage(TemplateView):
    template_name = 'chat.html'
    context_object_name = 'chat_page'


class UserChats(viewsets.ModelViewSet):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Chat.objects.filter(users=user_id)
        return queryset


class MessageChats(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.request.query_params.get('id')
        user_id = self.request.user.id
        queryset = Message.objects.filter(chat=chat_id)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = MessagePostSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                print("сбщ сохранено")
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)


class Users(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users_view'
