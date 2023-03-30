from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView
from helper.forms import AddBookForm

from helper.models import Books

# Create your views here.


class BooksView(ListView):
    model = Books
    context_object_name = 'books'
    template_name = 'helper/books.html'

    


class BookAdd(CreateView):
    form_class = AddBookForm
    template_name = 'generic_form.html'
    success_url =  reverse_lazy('books')



def bookselector(self, slug):
    book = Books.objects.get(slug=slug)
    if book.type == 'murim':
        return redirect('country-list', slug=slug)
    