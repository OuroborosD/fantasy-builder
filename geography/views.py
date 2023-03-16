from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, CreateView
from geography.forms import CountryForm, RegionForm, SettlementForm

from geography.models import Country, Region
# Create your views here.


# def helloWorld(request):
#     return HttpResponse('Hello, World')


navigator =  None
################################ Country ######################################

class Countries(ListView):
    model = Country
    context_object_name = 'countries'
    template_name = 'geography/home.html'

class CountriesAdd(CreateView):
    model = Country
    context_object_name = 'form'
    form_class = CountryForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('country')



################################ Region  ######################################
class RegionView(ListView):
    model = Region
    context_object_name = 'values'
    template_name = 'geography/region/dashboard.html'

    def get_context_data(self,**kwargs, ):
        context = super(RegionView,self).get_context_data(**kwargs)
        context['slug'] =  self.kwargs['slug']
        return context

class RegionAdd(View):
    def get(self,request, slug):
      form = RegionForm()
      context = {
          'form':form,
      }
      return render(request,'generic_form.html', context)  
    def post(self,request, slug):
        country =  Country.objects.get(slug=slug) 
        form = RegionForm(request.POST)

        if form.is_valid():
            Region.objects.create(
                fk_country = country,
                name = form.cleaned_data['name'],
                localization = form.cleaned_data['localization'],
                description = form.cleaned_data['description'],
            )
            return redirect('character-page', slug=country.slug)
        context = {
          'form':form,
        }
        return render(request,'generic_form.html', context)  
################################ Fief  ######################################



################################   ######################################
class AddSettlements(View):
    def get(self,request):
        form = SettlementForm()
        context = {
            'form':form
        }
        return render(request,'generic_form.html',context)

    def post(self,request):
        form = SettlementForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['economy'])
            economy = form.cleaned_data['economy']
            context = {
                'form':form
            }
            return render(request,'generic_form.html',context)
################################   ######################################



