from django.urls import path
from contactform import views

urlpatterns = [
    path("", views.contact_view, name="contact"), 
]
