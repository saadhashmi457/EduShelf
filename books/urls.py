# books/urls.py
from django.urls import path
from books import views

urlpatterns = [
    path("upload/", views.upload_book, name="upload_book"),
    path("Suceessmsg/", views.Suceessmsg, name="Suceessmsg"),
    path("<int:book_id>/", views.book_detail, name="book_detail"),
    path("<int:book_id>/request/", views.request_book, name="request_book"),
    path("read/<int:notif_id>/", views.mark_notification_read, name="mark_notification_read"),
    
]




