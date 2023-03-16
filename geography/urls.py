from django.urls import path
from . import views

urlpatterns = [
    path('', views.Countries.as_view(), name='country'),
    path('add/', views.CountriesAdd.as_view(), name='country-add'),
    #Region
    path('<slug:slug>/region/', views.RegionView.as_view(), name='region'),
    path('<slug:slug>/region/add/', views.RegionAdd.as_view(), name='region-add'),
    #Fief
    # path('<int:pk>/region/<int:pk>/', views.CountriesAdd.as_view(), name='teste'),
    # path('<int:pk>/region/add/', views.CountriesAdd.as_view(), name='teste'),
    #Settement
    path('settlement/add/', views.AddSettlements.as_view(), name='settlements-add'),
]