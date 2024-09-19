from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/livechat/(?P<room_name>[^/]+)/$', consumers.LiveChat.as_asgi()),
]