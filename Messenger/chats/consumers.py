import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User
import datetime


class LiveChat(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        print(f"соединение установлено для чата {self.room_name}")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print(f"соединение для {self.room_name} разорвано")


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        author = text_data_json["author"]
        chat = text_data_json["chat"]
        print(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "content": content, "authorID": author, "chat": chat}
        )


    def chat_message(self, event):
        content = event["content"]
        authorID = event["authorID"]
        user = User.objects.get(id=authorID)
        author = user.username
        chat = event["chat"]
        time = str(datetime.datetime.now())
        print({"content": content, "authorID": authorID, "author": author, "chat": chat, "time": time})
        self.send(text_data=json.dumps({"content": content, "authorID": authorID, "author": author, "chat": chat, "time": time}))