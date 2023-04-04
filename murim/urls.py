from django.urls import path
from . import views
urlpatterns = [
 path('', views.CharacterList.as_view(), name='character-list' ),
 path('add/', views.CharacterAdd.as_view(), name='character-murim-add' ),
 path('<slug:slug_character>/', views.character, name='character-murim' ),
 path('<slug:slug_character>/edit/', views.characterEdit.as_view(), name='character-murim-edit' ),
       
#atribute
 path('<slug:slug_character>/atribute/add/<int:pk_realm>/', views.AtributeAdd.as_view(), name='atribute-add' ),
 path('<slug:slug_character>/atribute/add/<int:pk_realm>/<int:pk>', views.AtributeEdit.as_view(), name='atribute-edit' ),

#realm
 path('<slug:slug_character>/Realm/add/', views.RealmAdd.as_view(), name='realm-add' ),
 
#proficience
 path('<slug:slug_character>/Proficience/add/', views.ProficienceAdd.as_view(), name='proficience-add' ),
 path('<slug:slug_character>/Proficience/<int:pk>/edit/', views.EditProficience.as_view(), name='proficience-edit' ),
 path('<slug:slug_character>/Proficience/<int:pk>/delete/', views.deleteProficience, name='proficience-delete' ),


#skill
 path('skill/add', views.Skill.as_view(), name='newskill' ),
 path('<slug:slug_character>/skill/add/', views.CharacterSkillAdd.as_view(), name='skill-add' ),
 path('<slug:slug_character>/skill/add/newskill/', views.Skill2.as_view(), name='newskill-add' ),
 path('<slug:slug_character>/skill/<int:pk>/edit/', views.EditSkill.as_view(), name='skill-edit' ),
 path('<slug:slug_character>/skill/<int:pk>/delete/', views.deleteSkill, name='skill-delete' ),

#item
 path('skill/add', views.Skill.as_view(), name='newskill' ),
 path('<slug:slug_character>/item/add/', views.AddItem.as_view(), name='item-add' ),
 path('<slug:slug_character>/item/<int:pk>/edit/', views.EditItem.as_view(), name='item-edit' ),
 path('<slug:slug_character>/item/<int:pk>/delete/', views.deleteItem, name='item-delete' ),
 path('<slug:slug_character>/coins/add/', views.AddCoin.as_view(), name='coin-add' ),
]