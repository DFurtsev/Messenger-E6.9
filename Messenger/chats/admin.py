from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *
from modeltranslation.admin import TranslationAdmin


class UserAdmin(TranslationAdmin):
    model = User


class UserInline(admin.TabularInline):
    model = UserChat
    extra = 2


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    inlines = (UserInline,)


admin.site.register(Message)
admin.site.register(Chat, ChatAdmin)
admin.site.register(UserChat)
