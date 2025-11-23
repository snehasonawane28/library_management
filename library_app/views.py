from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from .models import Book, BorrowRecord
from .forms import BookForm, PatronRegistrationForm
from datetime import timedelta
from django.utils import timezone

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'library_app/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    current_borrow = None
    expected_available_date = None
    actual_return_date = None
    
    # Get the most recent borrow record for this book
    current_borrow = BorrowRecord.objects.filter(
        book=book
    ).order_by('-borrow_date').first()
    
    if current_borrow:
        # If admin has set a return date, use that
        if current_borrow.return_date:
            actual_return_date = current_borrow.return_date
        # If book is not available but no return date is set
        elif not book.is_available and current_borrow.due_date:
            expected_available_date = current_borrow.due_date + timezone.timedelta(days=1)
    
    return render(request, 'library_app/book_detail.html', {
        'book': book,
        'current_borrow': current_borrow,
        'expected_available_date': expected_available_date,
        'actual_return_date': actual_return_date,
    })

def is_staff_user(user):
    return user.is_active and user.is_staff

@user_passes_test(is_staff_user, login_url='login')
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully.")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library_app/create_book.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = PatronRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('book_list')
    else:
        form = PatronRegistrationForm()
    return render(request, 'library_app/register.html', {'form': form})

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_available:
        messages.error(request, "Sorry, this book is currently unavailable.")
        return redirect('book_detail', pk=pk)
    
    # Set due date to 14 days from now
    due_date = timezone.now() + timezone.timedelta(days=14)
    
    # Create BorrowRecord with due date
    BorrowRecord.objects.create(
        book=book, 
        user=request.user,
        borrow_date=timezone.now(),
        due_date=due_date
    )
    
    book.is_available = False
    book.save()
    messages.success(request, f"You have borrowed '{book.title}'. Due date: {due_date.strftime('%Y-%m-%d')}")
    return redirect('book_detail', pk=pk)
