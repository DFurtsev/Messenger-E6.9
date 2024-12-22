from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'userChats', UserChats, basename='user_chats')
router.register(r'chatMessages', MessageChats, basename='chat_messages')


urlpatterns = [
    path('chat/', ChatPage.as_view(), name='chat'),
    path('chat/<int:pk>/', ChatPage.as_view(), name='redirect_to_chat'),
    path('api/', include(router.urls)),
    path('user/<int:pk>', UserProfile.as_view(), name='profile'),
    path('user/<int:pk>/edit/', UserUpdateForm.as_view(), name='profile_update'),
    path('users/', Users.as_view(), name='users'),
    path('createGroupChat/', CreateGroupChat.as_view(), name='create_group_chat'),
    path('addUserSearch/', search_user_result, name='search_user_result'),
    path('addingUser/', add_user_to_group_chat, name='add_user_to_group_chat'),
    # path('personalPage/', UserPage.as_view(), name='personal_page'),
    # path('get_user_info/', get_info, name='get_user_info'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
