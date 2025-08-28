# books/models.py
from django.db import models
from django.conf import settings  # This ensures we use the custom User model

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('sell', 'Sell'),
        ('exchange', 'Exchange'),
        ('free', 'Free'),
        ('buy', 'Buy'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('used', 'Used'),
        ('old', 'Old'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Only if Sell
    description = models.TextField()
    cover_image = models.ImageField(upload_to="book_covers/")

    # Auto fields
    upload_date = models.DateTimeField(auto_now_add=True)

    # Link to uploader (your custom user model)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Custom User compatibility
        on_delete=models.CASCADE,
        related_name="uploaded_books"
    )

    def __str__(self):
        return f"{self.title} by {self.author}"
