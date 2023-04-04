from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import  DetailView, View, ListView, CreateView
from bestiary.forms import LootForm, MonsterLootForm, magicbeast_form_type

from bestiary.models import Loot, MagicBeast, MagicBeastLoot
from helper.models import Books
# Create your views here.


class BestiaryList(ListView):
    model = MagicBeast
    context_object_name = 'beasties'
    template_name = 'bestiary/dashboard.html'

    def get_context_data(self, **kwargs, ):
        context = super(BestiaryList, self).get_context_data(**kwargs)
        print(f'	linha 26-------arquivo: {self.kwargs}------- valor:	')
        context['slug_book'] = self.kwargs['slug_book']

        return context

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        country = MagicBeast.objects.filter(
            fk_book__slug=self.kwargs['slug_book'])
        return country


class BeastiryAdd(View):
    def get(self, request, slug_book):
        type = Books.objects.get(slug=slug_book)
        form = magicbeast_form_type(type=type.type)
        context = {
            'form': form
        }
        return render(request, 'bestiary/add.html', context)

    def post(self, request, slug_book):
        type = Books.objects.get(slug=slug_book)
        form = magicbeast_form_type(
            post=request.POST, file=request.FILES, type=type.type)
        if form.is_valid():
            aux = form.save(commit=False)
            print(f'	linha 43-------arquivo: {aux.img}------- valor:')
            aux.fk_book = type
            aux.save()
            # MagicBeast.objects.create(
            #     fk_book = type,
            #     name = form.cleaned_data['name'],
            #     img = form.cleaned_data['img'],
            #     murim_realm = form.cleaned_data['murim_realm'],
            #     description = form.cleaned_data['description'],
            # )
            return redirect('beastiary-list', slug_book=slug_book)
        context = {
            'form': form
        }
        return render(request, 'bestiary/add.html', context)


class BeastDetail(DetailView):
    model = MagicBeast
    context_object_name = 'beast'
    template_name = 'bestiary/beast.html'

    def get_context_data(self, **kwargs, ):
        context = super(BeastDetail, self).get_context_data(**kwargs)
        print(f'	linha 26-------arquivo: {self.kwargs}------- valor:	')
        context['slug_book'] = self.kwargs['slug_book']
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            print(f'	linha 73-------arquivo: {queryset}------- valor	')
        queryset = queryset.filter(slug=self.kwargs['slug_beast'])
        print(f'	linha 75-------arquivo: {queryset}------- valor	')
        beast = queryset.get()
        loots = MagicBeastLoot.objects.filter(
            fk_beast__slug=self.kwargs['slug_beast'])
        print(f'	linha 77-------arquivo: {beast.name}------- valor	')
        return {"beast": beast,
                'loots': loots
                }


class BeastiryEdit(View):
    def get(self, request, slug_book, slug_beast):
        type = Books.objects.get(slug=slug_book)
        beast = MagicBeast.objects.get(slug=slug_beast)
        form = magicbeast_form_type(type=type.type, model=beast)
        context = {
            'form': form,
        }
        return render(request, 'bestiary/add.html', context)

    def post(self, request, slug_book, slug_beast):
        type = Books.objects.get(slug=slug_book)
        beast = MagicBeast.objects.get(slug=slug_beast)
        form = magicbeast_form_type(
            post=request.POST, file=request.FILES, type=type.type, model=beast)
        if form.is_valid():
            aux = form.save(commit=False)
            print(f'	linha 43-------arquivo: {aux.img}------- valor:')
            aux.fk_book = type
            aux.save()
            # MagicBeast.objects.create(
            #     fk_book = type,
            #     name = form.cleaned_data['name'],
            #     img = form.cleaned_data['img'],
            #     murim_realm = form.cleaned_data['murim_realm'],
            #     description = form.cleaned_data['description'],
            # )
            return redirect('beastiary', slug_book=slug_book, slug_beast=aux.slug)
        context = {
            'form': form
        }
        return render(request, 'bestiary/add.html', context)


class MonsterLootAdd(CreateView):
    model = MagicBeastLoot
    context_object_name = "form"
    form_class = MonsterLootForm
    template_name = 'bestiary/beastloot/add.html'

    def get_context_data(self, **kwargs, ):
        context = super(MonsterLootAdd, self).get_context_data(**kwargs)
        context['slug_book'] = self.kwargs['slug_book']
        context['slug_beast'] = self.kwargs['slug_beast']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('beastiary', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_beast': self.kwargs['slug_beast']})

    def form_valid(self, form):
        self.object = form.save(False)
        # make change at the object
        beast = MagicBeast.objects.get(slug=self.kwargs['slug_beast'])
        print(f'	linha 138-------arquivo: {form.cleaned_data}------- valor:	')
        print(
            f'	linha 138-------arquivo: {form.cleaned_data["filtred_loot"].pk}------- valor:	')
        self.object.fk_loot = Loot.objects.get(
            pk=form.cleaned_data["filtred_loot"].pk)
        self.object.fk_beast = beast
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            print(f'	linha 73-------arquivo: {queryset}------- valor	')
        queryset = queryset.filter(slug=self.kwargs['slug_beast'])
        print(f'	linha 75-------arquivo: {queryset}------- valor	')
        beast = queryset.get()
        print(f'	linha 77-------arquivo: {beast.name}------- valor	')
        return beast


class LootAdd(CreateView):
    model = Loot
    context_object_name = "form"
    form_class = LootForm
    template_name = 'bestiary/loot/add.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('beastloot-add', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_beast': self.kwargs['slug_beast']})

    def form_valid(self, form):
        self.object = form.save(False)
        book = Books.objects.get(slug=self.kwargs['slug_book'])
        beast = MagicBeast.objects.get(slug=self.kwargs['slug_beast'])
        self.object.fk_book = book
        self.object.fk_beast = beast
        print(self.object)
        # make change at the object
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class MonsterLootEdit(View):
    def get(self, request, slug_book, slug_beast, pk_loot):
        loot = MagicBeastLoot.objects.get(pk=pk_loot)
        form = MonsterLootForm(instance=loot)
        # caso tenha o filtro da pk no modelForm, tera que colocar o campo que foi filtaro manualmente.
        form.initial['filtred_loot'] = loot.fk_loot
        context = {
            'loot':loot.pk,
            'form': form,
            'slug_book': slug_book,
            'slug_beast': slug_beast,
        }
        return render(request, 'bestiary/beastloot/edit.html', context)

    def post(self, request, slug_book, slug_beast, pk_loot):
        loot = MagicBeastLoot.objects.get(pk=pk_loot)
        form = MonsterLootForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('beastiary', slug_book=slug_book, slug_beast=slug_beast)
        context = {
            'form': form
        }
        return render(request, 'bestiary/beastloot/edit.html', context)


def montersLootDelete(request, slug_book, slug_beast, pk_loot):
    loot = MagicBeastLoot.objects.get(pk=pk_loot)
    loot.delete()
    return redirect('beastiary', slug_book=slug_book, slug_beast=slug_beast)
