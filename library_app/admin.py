
from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_available', 'created_at')

@admin.register(BorrowRecord)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'return_date')
