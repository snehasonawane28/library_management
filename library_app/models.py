
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.author}"

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username} (Due: {self.due_date})"
