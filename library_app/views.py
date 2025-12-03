from django.shortcuts import render  # html page return render
from django.shortcuts import render, redirect, get_object_or_404 # kisi dusre url par bhej deta hai agr object mil gya toh de deta hai.warna 404 error
from django.contrib.auth.decorators import login_required, user_passes_test #user login nahi hoga toh page nahi khulega login required,custom condition (jise hun staff only set kar rahe) apply karta hai.
from django.contrib import messages #succes error message dikhane ke liye
from django.contrib.auth import login #register ke bad login karne ke liye.
from .models import Book, BorrowRecord #database models import ho rhe hain
from .forms import BookForm, PatronRegistrationForm #django forms import ho rahe hai.
from datetime import timedelta #Date/time manage karne ke liye
from django.utils import timezone #date /time manage karne ke liye
from django.db.models import Q, F, ExpressionWrapper, fields  # added this import

def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all().order_by('-created_at')
    
    if query:
        # Search in title, author, or ISBN (case-insensitive)
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) |
            Q(isbn__iexact=query)
        )
    
    return render(request, 'library_app/book_list.html', {
        'books': books,
        'search_query': query
    })
#Book.object.all database saare books lata hai,order_by(-created_at) new books sbse pehele.
#html page book_list ko open krta hai.page ko books ka data bhejta hai.   

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    current_borrower = None
    borrow_record = None
    
    # Check if the book is currently borrowed
    if not book.is_available:
        current_borrowal = BorrowRecord.objects.filter(book=book, return_date__isnull=True).first()
        if current_borrowal:
            current_borrower = {
                'name': current_borrowal.user.get_full_name() or current_borrowal.user.username,
                'email': current_borrowal.user.email,
                'is_staff': current_borrowal.user.is_staff
            }
            borrow_record = current_borrowal
    
    # Get all borrow records for this book (for history)
    borrow_history = BorrowRecord.objects.filter(book=book).exclude(return_date__isnull=True).order_by('-borrow_date')
    
    # Get the latest return date for the book
    latest_return = BorrowRecord.objects.filter(
        book=book, 
        return_date__isnull=False
    ).order_by('-return_date').first()
    
    # Get the current borrow record (if any)
    current_borrowal = BorrowRecord.objects.filter(
        book=book,
        return_date__isnull=True
    ).first()
    
    # If there's a current borrow, use it, otherwise use the latest return
    borrow_record = current_borrowal or latest_return
    
    return render(request, 'library_app/book_detail.html', {
        'book': book,
        'current_borrower': current_borrower,
        'borrow_record': borrow_record,
        'latest_return': latest_return,
        'borrow_history': borrow_history
    })

def is_staff_user(user):
    return user.is_active and user.is_staff
#agr user/staf admin hai->true warna false


@user_passes_test(is_staff_user, login_url='login')
#agr user staff nahi hai->login page pe bhej do 
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully.")
            return redirect('book_list')
#form data + image(request.files)   read hoti hai
#valid hogi -> database me save
#success message book list page redirect hoga
           
    else:
        form = BookForm()
    return render(request, 'library_app/create_book.html', {'form': form})
#jab open kare->empty form show karo

def register(request):
    if request.method == 'POST':
        form = PatronRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('book_list')
#form data validate , user create, 
#user ko login bhi kar dete ho  
#return redirect to book list.          
    else:
        form = PatronRegistrationForm()
    return render(request, 'library_app/register.html', {'form': form})
#jab open kare->empty form show karo

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
#bool load karo    
    if not book.is_available:
        messages.error(request, "Sorry, this book is currently unavailable.")
        return redirect('book_detail', pk=pk)
#book already borrowed hai -> error show     

    # Get current datetime with timezone
    from django.utils import timezone
    now = timezone.localtime(timezone.now())
    
    # Set due date to 14 days from now at the same time
    due_datetime = now + timezone.timedelta(days=14)

    # Debug output
    print(f"Borrowing at: {now}")
    print(f"Due at: {due_datetime}")

    # Create BorrowRecord with both date and time
    borrow_record = BorrowRecord.objects.create(
        book=book, 
        user=request.user,
        borrow_date=now.date(),
        borrow_time=now.time(),
        due_date=due_datetime.date(),
        due_time=now.time()  # Keep the same time for due
    )
    
    # Debug output
    print(f"Created record with borrow_time: {borrow_record.borrow_time}")
    print(f"And due_time: {borrow_record.due_time}")
    
    book.is_available = False
    book.save()
    messages.success(request, f"You have borrowed '{book.title}'. Due date: {due_datetime.strftime('%Y-%m-%d %I:%M %p')}")
    return redirect('book_detail', pk=pk)


#book table me books ka data hota hai
#user table me logonn ka data hota hai.
#BorrowRecord table transaction hota hai (kisne konsi book kab li hai)
#foreign key : book_id links -> borrowrecord ->book
#foreign key : user_id links -> borrowrecor -> user
#isse database samjhta hai ki kis user ne kaunsi book li hai.
#foreign key : borrow_date links -> borrowrecord -> borrow_date
#foreign key : due_date links -> borrowrecord -> due_date
#foreign key : return_date links -> borrowrecord -> return_date
#foreign key : is_returned links -> borrowrecord -> is_returned
#isse database samjhta hai ki kis user ne kaunsi book kab li hai.

#ek table ka column dusre table ke primary key ko refer kare

#book = foreignkey (book) = yeh bata rha hai kis book se yeh recod linked hai
#user = foreignkey (user) = yeh bata rha hai kis user ne borrow kiya

@login_required
def return_book(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk, user=request.user)
    
    if borrow_record.return_date is None:
        # Get current datetime
        now = timezone.localtime(timezone.now())
        
        # Mark book as returned with both date and time
        borrow_record.return_date = now.date()
        borrow_record.return_time = now.time()
        
        # Check if book is returned after due date
        if borrow_record.due_date and now.date() > borrow_record.due_date:
            # Calculate fine based on full days late
            days_late = (now.date() - borrow_record.due_date).days
            if days_late > 0:
                borrow_record.fine_amount = days_late * 5  # ₹5 per day
        
        # Update book availability
        book = borrow_record.book
        
        # Make the book available
        book.is_available = True
        messages.success(request, f"Book '{book.title}' has been returned successfully.")
        
        book.save()
        borrow_record.save()
    
    return redirect('borrowed_books_history')

@login_required
def pay_fine(request, pk):
    if request.method == 'POST':
        borrow_record = get_object_or_404(BorrowRecord, pk=pk, user=request.user)
        if borrow_record.fine_amount > 0 and not borrow_record.fine_paid:
            borrow_record.fine_paid = True
            borrow_record.save()
            messages.success(request, f"Fine of ₹{borrow_record.fine_amount} paid successfully.")
    return redirect('borrowed_books_history')

@login_required
def borrowed_books_history(request):
    # Get all borrow records for the current user, ordered by most recent first
    borrow_records = BorrowRecord.objects.filter(
        user=request.user
    ).select_related('book').order_by('-borrow_date')
    
    # Calculate days late and fine for each record
    for record in borrow_records:
        if record.return_date and record.due_date and not record.fine_calculated:
            if record.return_date > record.due_date:
                days_late = (record.return_date - record.due_date).days
                if days_late > 0:
                    record.fine_amount = days_late * 5
                    record.fine_calculated = True
                    record.save()
    
    # Annotate each record with the number of days the book was kept
    borrow_records = borrow_records.annotate(
        days_kept=ExpressionWrapper(
            F('return_date') - F('borrow_date'),
            output_field=fields.DurationField()
        )
    )
    
    # Calculate total fine amount for unpaid fines
    total_fine = sum(record.fine_amount for record in borrow_records if not record.fine_paid and record.fine_amount > 0)
    
    return render(request, 'library_app/borrowed_books_history.html', {
        'borrow_records': borrow_records,
        'total_fine': total_fine
    })
