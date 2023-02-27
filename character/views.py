from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Characters, Status
# Create your views here.

# BOOK colocar view


class CharacterList(ListView):
    model = Characters  # aqui coloca a classe que está vindo
    template_name = 'character/home.html'
    # tem o retorno do contexto implicito, ele vai como o nome do model em caixa baixo 'characters' e apartir dele pode usar
    # loops para mostrar as informações

def characterDetailView(request, slug):
    character = Characters.objects.get(slug=slug)
    status = Status.objects.filter(fk_character = character).order_by('page').last()#pega o registro com a ultima pagina alterada.
    context = {
        's':status,
        'c':character
    }
    
    return render(request,'character/character-murim.html',context)


class characterPage(DetailView):
    model = Characters
    template_name = 'character/character-murim.html'
    context_object_name = 'character'  # muda o nome padrão do contexto


class AddCharacter(CreateView):
    model = Characters
    template_name = 'character/add_character.html'
    fields = ['name', 'alias','birth_year','season','periode']


class EditCharacter(UpdateView):
    model = Characters
    template_name = 'character/edit_character.html'
    fields = ['name', 'alias','birth_year','season','periode']


class DeleteCharacter(DeleteView):
    model = Characters
    template_name = 'character/del_character.html'
    success_url = reverse_lazy('character')
