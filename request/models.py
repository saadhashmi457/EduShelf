from django.conf import settings
from django.db import models
from books.models import Book

class BookRequest(models.Model):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # 👈 yahan fix
        on_delete=models.CASCADE,
        related_name="book_requests"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="requests"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} → {self.book.title} ({self.status})"
