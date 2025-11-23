Tech Stack
-----------
1.Django (Python)
2.SQLite (Default Database)
3.Django Template System
4.Django Forms / ModelForms
5.Authentication System + Access Control
       |
Create Virtual Environment
python -m venv venv
       |
Windows
venv\Scripts\activate
       |
python --version          3.14
       |
pip install django
       |
django-admin --version    5.2.8
       |
django-admin startproject library_management
       |
cd library_management
python manage.py startapp library_app
       |
settings.py page
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'library_app',  # Add this
]
       |
settings.py page #Login/Logout Settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'book_list'
LOGOUT_REDIRECT_URL = 'book_list'
       |
python manage.py makemigrations
python manage.py migrate
       |
python manage.py runserver
       |
Models:
1.Book Model
2.BorrowRecord Model
       |
Librarian Account:
username : sneha
password : sne12345678
       |
patron Account :
username : patron
password : patron123
       |
Create Book (Librarian Only) : 
Uses @user_passes_test(lambda u: u.is_staff).
On POST, saves new book.
1. Login with librarian credentials 
2. Click "Add Book" in navigation
3. Fill the form and submit
4. Book should appear in the book list
       |
Add User (Patron Registration)
Uses UserCreationForm.
On success → redirects to Login.
1. Click "Register" (no login required)
2. Fill registration form
3. Submit to create new patron account
4. Automatically logged in after registration
      |
Borrowing logic
1.Clicking Borrow creates a BorrowRecord linking the user and the book
2.Book availability switches to False after successful borrowing
     |
Authentication & Security :
Login / Logout implemented using Django's built-in views.
Access control:
Borrow Book → Only authenticated users
Add Book → Only staff users
Decorators used:
@login_required
@user_passes_test
     |
Template inheritance
Pages included:
1.base.html
2.register.html
3.login.html
4.book_list.html
5.book_detail.html
6.add_book.html
     |
http://127.0.0.1:8000/book/create/ = add book /staff 
     |
http://127.0.0.1:8000/login/       = login  /patron,staff
     |
http://127.0.0.1:8000/register/    = register /patron 
     |
http://127.0.0.1:8000/book/6/      = details
     |
Library Management System successfully
     |
Django MVC (Models, Views, Templates)
ModelForms
Authentication
Access Control
CRUD logic
Database relationships
