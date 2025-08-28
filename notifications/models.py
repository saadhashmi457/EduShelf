from django.db import models
from django.conf import settings   # 👈 instead of importing auth.User
from books.models import Book

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # 👈 this fixes the error
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"
