from django.urls import path

from .views import CharactersView

urlpatterns = [
    path('', CharactersView.as_view(), name='character')
]



