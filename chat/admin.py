from django.contrib import admin
from .models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "message", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("sender__username", "receiver__username", "message")
    ordering = ("-timestamp",)


admin.site.register(ChatMessage, ChatMessageAdmin)
