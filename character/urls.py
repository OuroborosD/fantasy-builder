from django.urls import path

from .views import CharacterList,characterPage,AddCharacter,EditCharacter, DeleteCharacter, characterDetailView, skillAdd

urlpatterns = [
    #character
    path('', CharacterList.as_view(), name='character'),
    path('add/', AddCharacter.as_view(), name='character-add'),# se não tivesse um page/ no de baixo o django pensaria que essa poderia ser um slug, foi slug é texto 
    path('teste/<slug:slug>/', characterDetailView, name='character-page'),
    path('edit/<slug:slug>', EditCharacter.as_view(), name='character-edit'),
    path('del/<slug:slug>', DeleteCharacter.as_view(), name='character-del'),
    #skill
    path('<slug:slug>/skills/add/', skillAdd, name='skill-add'),
    path('<slug:slug>/skills/edit/', skillAdd, name='skill-edit'),
    path('<slug:slug>/skills/delete/', skillAdd, name='skill-delete'),
    
]



