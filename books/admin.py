from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'language', 'condition', 'price', 'upload_date', 'uploader')
    list_filter = ('category', 'language', 'condition', 'upload_date')
    search_fields = ('title', 'author', 'genre', 'uploader__full_name')


# # books/admin.py
# from django.contrib import admin
# from .models import Book

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'author',       
#         'genre',
#         'category',
#         'condition',    
#         'language',
#         'price',
#         'uploader',    
#         'upload_date',
#     )

#     list_filter = (
#         'category',
#         'condition',  
#         'language',
#     )

#     search_fields = ('title', 'author', 'genre', 'language')
