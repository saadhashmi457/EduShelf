from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.chat_with_user, name="chat_with_user"),
    path('inbox/', views.inbox, name='inbox'),
   
]
