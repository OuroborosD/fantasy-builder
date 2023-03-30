from django.urls import path
from . import views

urlpatterns = [
    #select
    path("goingtocharacter/", views.CharacterType, name ='character-goto' ),

    #country
    path('', views.Countries.as_view(), name='country-list'),
    path('add/', views.CountriesAdd.as_view(), name='country-add'),
    path('<slug:slug_country>/', views.CountryView.as_view(), name='country'),
    path('<slug:slug_country>/edit/', views.CountryUpdate.as_view(), name='country-edit'),
    #Region
    path('<slug:slug_country>/regions/add/', views.RegionAdd.as_view(), name='region-add'),
    path('<slug:slug_country>/regions/<slug:slug_region>/', views.RegionView.as_view(), name='region'),
    path('<slug:slug_country>/regions/<slug:slug_region>/edit/', views.RegionEdit.as_view(), name='region-edit'),
    #Fief
    path('<slug:slug_country>/regions/<slug:slug_region>/add/', views.FiefAdd.as_view(), name='fief-add'),
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/', views.FiefView.as_view(), name='fief'),
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/edit/', views.FiefEdit.as_view(), name='fief-edit'),
    #Settement
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/add/', views.SettlementAdd.as_view(), name='settlement-add'),
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/settlement/<slug:slug_settlement>/', views.SettlementView.as_view(), name='settlement'),
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/settlement/<slug:slug_settlement>/edit/', views.SettlementEdit.as_view(), name='settlement-edit'),
    #Local
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/<slug:slug_settlement>/local/<slug:slug_local>', views.LocalAdd.as_view(), name='local'),
    path('<slug:slug_country>/regions/<slug:slug_region>/fief/<slug:slug_fief>/<slug:slug_settlement>/add/', views.LocalAdd.as_view(), name='local-add'),



  

]