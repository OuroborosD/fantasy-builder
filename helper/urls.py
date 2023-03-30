from django.urls import path

from . import views


urlpatterns =[
    path('', views.BooksView.as_view(), name='books'),
    path('add/', views.BookAdd.as_view(), name='books-add'),
]