
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.create_book, name='create_book'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='library_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('borrowed-books/', views.borrowed_books_history, name='borrowed_books_history'),
    path('return-book/<int:pk>/', views.return_book, name='return_book'),
    path('pay-fine/<int:pk>/', views.pay_fine, name='pay_fine'),
]
