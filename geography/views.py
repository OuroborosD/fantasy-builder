from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Create your views here.


# def helloWorld(request):
#     return HttpResponse('Hello, World')


class HomePageView(TemplateView):
    template_name = 'geography/home.html'


class TestePage(TemplateView):
    template_name = 'geography/hello.html'