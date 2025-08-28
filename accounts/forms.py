from django import forms
from books.models import Book
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'category', 'language', 'condition', 'price', 'description', 'cover_image']



User = get_user_model()
class UniversityEmailPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Use university_email instead of default email
        active_users = User._default_manager.filter(
            is_active=True,
            university_email__iexact=email
        )
        return (u for u in active_users if u.has_usable_password())