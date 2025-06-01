from django.contrib import admin
from django.urls import path
from . import views



app_name = 'books'


urlpatterns = [
    path('create/', views.CreateBooksView.as_view(), name='create_book'),
    path('update/<int:pk>/', views.UpdateBooksView.as_view(), name='update_book'),
    path('delete/<int:pk>/', views.DeleteBooksView.as_view(), name='delete_book'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('list-books/', views.ListBooksView.as_view(), name='list_books'),
    path('assign-books/', views.AssignBookView.as_view(), name='assign_book'),
]