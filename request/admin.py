from django.contrib import admin
from .models import BookRequest

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'requester', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('book__title', 'requester__email') 
