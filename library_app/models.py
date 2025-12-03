
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

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
    borrow_date = models.DateField(default=timezone.now)
    borrow_time = models.TimeField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    due_time = models.TimeField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    return_time = models.TimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    fine_calculated = models.BooleanField(default=False)
    
    @property
    def full_borrow_datetime(self):
        if self.borrow_date and self.borrow_time:
            return datetime.combine(self.borrow_date, self.borrow_time)
        return None
        
    @property
    def full_due_datetime(self):
        if self.due_date and self.due_time:
            return datetime.combine(self.due_date, self.due_time)
        return None
        
    @property
    def full_return_datetime(self):
        if self.return_date and self.return_time:
            return datetime.combine(self.return_date, self.return_time)
        return None

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username} (Due: {self.due_date})"
    
    def calculate_fine(self):
        if not self.return_date or not self.due_date or self.fine_calculated:
            return 0
            
        if self.return_date > self.due_date:
            # Calculate days late (only count full days)
            days_late = (self.return_date - self.due_date).days
            if days_late > 0:
                # ₹5 per day fine
                fine = days_late * 5
                self.fine_amount = fine
                self.fine_calculated = True
                self.save()
                return fine
        return 0

