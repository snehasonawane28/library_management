
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
]
