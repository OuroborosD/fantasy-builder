from django.urls import path
from . import views

urlpatterns = [
    path('', views.Countries.as_view(), name='country'),
    path('add/', views.CountriesAdd.as_view(), name='country-add'),
    path('<slug:slug>/edit/', views.CountryUpdate.as_view(), name='country-edit'),
    #Region
    path('<slug:slug>/regions/', views.RegionView.as_view(), name='region'),
    path('<slug:slug>/regions/add/', views.RegionAdd.as_view(), name='region-add'),
    path('<slug:slug_country>/regions/<slug:slug_region>/edit/', views.RegionEdit.as_view(), name='region-edit'),
    #Fief
    path('<slug:slug_country>/regions/<slug:slug_region>/', views.FiefView.as_view(), name='fief'),
    path('<slug:slug_country>/regions/<slug:slug_region>/add/', views.FiefAdd.as_view(), name='fief-add'),
    #Settement
    path('settlements/add/', views.AddSettlements.as_view(), name='settlements-add'),
]