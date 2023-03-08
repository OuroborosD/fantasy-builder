from django.urls import path

from .views import (CharacterList ,characterPage,AddCharacter,EditCharacter, DeleteCharacter, characterDetailView, skillAdd, skillCharacter,proficienceAdd,
                    editProficience, statusAdd,statusEdit)

urlpatterns = [
    #character
    path('', CharacterList.as_view(), name='characters'),
    path('details/<slug:slug>/', characterDetailView, name='character-page'),
    path('details/add/', AddCharacter.as_view(), name='character-add'),# se não tivesse um page/ no de baixo o django pensaria que essa poderia ser um slug, foi slug é texto 
    path('details/edit/<slug:slug>', EditCharacter.as_view(), name='character-edit'),
    path('details/del/<slug:slug>', DeleteCharacter.as_view(), name='character-del'),
    #skill
    path('details/<slug:slug>/skills/add/', skillCharacter, name='skill-character'),
    path('details/<slug:slug>/skills/add/new', skillAdd, name='skill-add'),
    path('details/<slug:slug>/skills/edit/', skillAdd, name='skill-edit'),
    path('details/<slug:slug>/skills/delete/', skillAdd, name='skill-delete'),
    #status
    path('details/<slug:slug>/status/add', statusAdd, name='status-add'),
    path('details/<slug:slug>/status/edit/<int:pk>', statusEdit, name='status-edit'),
    #proficience
    path('details/<slug:slug>/proficience/add/', proficienceAdd, name='proficience-add'),
    #path('<slug:slug>/proficience/edit/', proficienceAdd, name='proficience-edit'),
    path('details/<slug:slug>/proficience/edit/<int:pk>/', editProficience, name='proficience-edit'),
    
]



