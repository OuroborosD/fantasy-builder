from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from utils.rank import Rank

from .models import Characters, Status, Proficience, Skills
# Create your views here.

# BOOK colocar view


class CharacterList(ListView):
    model = Characters  # aqui coloca a classe que está vindo
    template_name = 'character/home.html'
    # tem o retorno do contexto implicito, ele vai como o nome do model em caixa baixo 'characters' e apartir dele pode usar
    # loops para mostrar as informações


def characterDetailView(request, slug):
    character = Characters.objects.get(slug=slug)
    # pega o registro com a ultima pagina alterada.
    status = Status.objects.filter(
        fk_character=character).order_by('page').last()
    proficiencia = Proficience.objects.filter(
        fk_character=character).order_by('weapon', '-pk').distinct('weapon')
    proficiencia_page = proficiencia.all().order_by('weapon', 'page').values().last()
    skill = Skills.objects.filter(fk_character=character)
    context = {
        's': status,
        'c': character,
        'proficiences': proficiencia,
        'proficiencia_page': proficiencia_page,
        'skills': skill,
    }

    return render(request, 'character/character-murim.html', context)


class characterPage(DetailView):
    model = Characters
    template_name = 'character/character-murim.html'
    context_object_name = 'character'  # muda o nome padrão do contexto


class AddCharacter(CreateView):
    model = Characters
    template_name = 'character/add_character.html'
    fields = ['name', 'alias', 'birth_year', 'season', 'periode']


class EditCharacter(UpdateView):
    model = Characters
    template_name = 'character/edit_character.html'
    fields = ['name', 'alias', 'birth_year', 'season', 'periode']


class DeleteCharacter(DeleteView):
    model = Characters
    template_name = 'character/character_del.html'
    success_url = reverse_lazy('character')


#################### skill#############################

def skillAdd(request, slug):
    ranks = Rank()
    if request.method == 'POST':
        name_skill = request.POST['name']
        rank_skill = request.POST['rank']
        print(f'{name_skill} --- {rank_skill}')
        # não é boa pratica redirecionar na mesma pagina
    else:
        ranks = Rank()

    context = {
        'ranks': ranks.skill_rank_list,
        'sub_ranks': ranks.skill_sub_rank_list,
        'masteries': ranks.skill_mastery_list
    }

    return render(request, 'character/skill_add.html', context)


############################ utils###########################
# def redirectCharacterDetails(request, slug):
#     return render
