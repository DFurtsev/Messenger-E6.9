from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *




class UserInline(admin.TabularInline):
    model = UserChat
    extra = 2


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    inlines = (UserInline,)


admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Chat, ChatAdmin)
admin.site.register(UserChat)
