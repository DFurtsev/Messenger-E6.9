from django.urls import path, include
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'userChats', UserChats, basename='user_chats')
router.register(r'chatMessages', MessageChats, basename='chat_messages')


urlpatterns = [
    # path('api/messagelist', UserChats.as_view(), name='messages'),
    path('chat/', ChatPage.as_view(), name='chat'),
    path('api/', include(router.urls)),
    path('users/', Users.as_view(), name='users')
    # path('chat-detail/<int:pk>/', ChatView.as_view(), name='person_chat'),
    # path('users/', UsersView.as_view(), name='chat')
    ]
