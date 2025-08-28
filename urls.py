from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from accounts.forms import UniversityEmailPasswordResetForm


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    path('browsebook/', views.browsebooks, name='browsebook'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),  
    # path('addbook/', views.addbook, name='addbook'),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("my-requests/", views.my_requests, name="my_requests"),
    
    path('editprofile/', views.editprofile, name='editprofile'),
    path('password_reset/', views.password_reset, name='password_reset'),
    
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            form_class=UniversityEmailPasswordResetForm,
            template_name='main/password_reset.html',
            email_template_name='auth/password_reset_email.html',
            subject_template_name='auth/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    
    
    path('manage_user/', views.manage_user, name='manage_user'),
    path('manage_contacter/', views.manage_contacter, name='manage_contacter'),
    path('respond_contact/<int:contact_id>/', views.respond_contact, name='respond_contact'),
    path('FAQ_S/', views.FAQ_view, name='FAQ_S'),
    
   
    
]

