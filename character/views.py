from django.shortcuts import render
from django.views.generic import ListView

from .models import Characters
# Create your views here.

#BOOK colocar view
class CharactersView(ListView):
    model = Characters #aqui coloca a classe que está vindo
    template_name = 'character/home.html'
    # tem o retorno do contexto implicito, ele vai como o nome do model em caixa baixo 'characters' e apartir dele pode usar 
    #loops para mostrar as informações