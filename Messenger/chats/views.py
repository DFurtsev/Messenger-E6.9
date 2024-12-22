from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime

from .forms import UserUpdateForm
from .models import Chat, Message, UserChat, User
from .serializers import ChatSerializer, MessageSerializer, MessagePostSerializer, UserSerializer


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
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)


# страничка со всеми юзерами, здесь же обрабатывается создание нового диалога с пользователем с перебрасыванием в этот диалог
class Users(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users_view'

    def get_queryset(self):
        queryset = User.objects.exclude(id=self.request.user.id)
        return queryset

    def post(self, request):
        if 'to_user' not in request.POST:
            return render(self.request, '403.html')
        def get_chat_id(request):
            user_chats = UserChat.objects.filter(user=request.user, chat__type='DIALOG').values_list('chat_id', flat=True)
            target_user = User.objects.get(id=request.POST['to_user'])
            chat_with_target_user = UserChat.objects.filter(user=target_user, chat__type='DIALOG').values_list('chat_id', flat=True)
            if user_chats.count() == 0 or chat_with_target_user.count() == 0:
                chat = Chat.objects.create()
                chat.users.add(request.user)
                chat.users.add(target_user)
                chat.save()
                target_chat_id = Chat.objects.filter(id=chat.id).values_list('id', flat=True)[0]
            else:
                target_chat_id = user_chats.intersection(chat_with_target_user)[0]
            return target_chat_id

        chat_id = get_chat_id(request)
        return redirect(f'/chat/{chat_id}/')


# class UserPage(TemplateView):
#     template_name = 'personal_page.html'
#     context_object_name = 'user_page'
#
#
# def get_info(request):
#     print(request.user.id)
#     user = User.objects.get(id=request.user.id)
#     send_data = {
#         "username": user.username,
#         "first_name": user.first_name,
#         "last_name": user.last_name
#     }
#     return JsonResponse({"user": send_data})


class UserProfile(DetailView):
    model = User
    template_name = 'personal_page.html'
    context_object_name = 'profile'
    queryset = User.objects.all()

    def get_object(self, *args, **kwargs):
        obj = super().get_object(queryset=self.queryset)
        return obj


class CreateGroupChat(ListView):
    model = User
    template_name = 'create_group_chat.html'
    context_object_name = 'create_group'

    def get_queryset(self):
        queryset = User.objects.exclude(id=self.request.user.id)
        return queryset

    def post(self, request):
        users = request.POST.getlist("user_id")
        if len(users) > 0:
            chat = Chat.objects.create()
            chat.type = "GROUP_CHAT"
            chat.users.add(request.user)
            for i in users:
                user = User.objects.get(id=i)
                chat.users.add(user)
            chat.save()
            return redirect(f'/chat/{chat.id}')
        else:
            return redirect('create_group_chat')


def search_user_result(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        send_data = None
        text = request.POST.get("text")
        queryset = User.objects.filter(username__icontains=text)
        if len(queryset) > 0 and len(text) > 0:
            data = []
            for i in queryset:
                user = {
                    "id": i.pk,
                    "username": i.username,
                    "first_name": i.first_name,
                    "last_name": i.last_name
                }
                data.append(user)
            send_data = data
        else:
            send_data = "Пользователи не найдены"
        return JsonResponse({"data": send_data})
    return JsonResponse({})


def add_user_to_group_chat(request):
    user_id = request.POST.get("userID")
    chat_id = request.POST.get("chatNumber")
    if UserChat.objects.filter(chat_id=chat_id, user_id=user_id).exists():
        print('Пользователь уже добавлен в чат')

        send_data = "Пользователь уже добавлен в чат ранее"
    else:
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        chat.users.add(user)
        chat.save()
        send_data = {
            "user": user.username,
            "chat": chat_id,
            "result": "Пользователь добавлен",
        }
    return JsonResponse({"data": send_data})


class UserUpdateForm(UpdateView):
    raise_exception = True
    form_class = UserUpdateForm
    model = User
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('chat')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super().form_valid(form)


