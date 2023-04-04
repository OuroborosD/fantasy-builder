from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, View, ListView, CreateView
from almanac.forms import AlmanacForm

from almanac.models import Almanac
from helper.models import Books
# Create your views here.


class AlmanacAdd(CreateView):
    model = Almanac
    form_class = AlmanacForm
    template_name = 'almanac/add.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('almanac-list', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_beast': self.kwargs['slug_beast']})

    def form_valid(self, form):
        self.object = form.save(False)
        # make change at the object
        book = Books.objects.get(slug=self.kwargs['slug_book'])
        self.object.fk_book = book
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    