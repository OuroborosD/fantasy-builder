from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView
from geography.forms import CountryForm, FiefForm, RegionForm, SettlementForm

from geography.models import Country, Fief, Region
from helper.models import Localization
# Create your views here.


# def helloWorld(request):
#     return HttpResponse('Hello, World')


navigator = None
################################ Country ######################################


class Countries(ListView):
    model = Country
    context_object_name = 'countries'
    template_name = 'geography/country/dashboard.html'


class CountriesAdd(CreateView):
    model = Country
    context_object_name = 'form'
    form_class = CountryForm
    template_name = 'generic_form.html'
    success_url = reverse_lazy('country')


class CountryUpdate(UpdateView):
    model = Country
    template_name = 'generic_form.html'
    fields = ['name', 'rank']

    def get_success_url(self):
        #                    URL_name          Name_filed_url : object_atribute
        return reverse_lazy('region', kwargs={'slug': self.object.slug})


################################ Region  ######################################
class RegionView(ListView):
    model = Region
    context_object_name = 'values'
    template_name = 'geography/region/dashboard.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs, ):
        context = super(RegionView, self).get_context_data(**kwargs)
        print(f'	linha52 -------arquivo: {self.kwargs["slug"]}------- valor:')
        context['slug'] = self.kwargs['slug']

        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        return Region.objects.filter(fk_country__slug=self.kwargs['slug'])


class RegionAdd(View):
    def get(self, request, slug):
        form = RegionForm()
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug):
        country = Country.objects.get(slug=slug)
        localization = Localization.objects.all()
        form = RegionForm(request.POST)

        if form.is_valid():
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            region = Region(
                fk_country=country,
                name=form.cleaned_data['name'],

                description=form.cleaned_data['description'],
            )
            region.save()
            for l in form.cleaned_data["localization"]:
                region.localization.add(localization.get(name=l))
            return redirect('region', slug=country.slug)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


class RegionEdit(View):
    def get(self, request, slug_country, slug_region):
        form = RegionForm()
        region = Region.objects.get(slug=slug_region)
        form.initial['name'] = region.name
        # form.initial['localization'] = region.localization
        form.initial['description'] = region.description
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_country, slug_region):
        country = Country.objects.get(slug=slug_country)

        localization = Localization.objects.all()
        form = RegionForm(request.POST)

        if form.is_valid():
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            region = Region.objects.get(slug=slug_region)
            region.name = form.cleaned_data['name']
            region.description = form.cleaned_data['description']
            region.save()
            for l in form.cleaned_data["localization"]:
                region.localization.add(localization.get(name=l))
            return redirect('region', slug=country.slug)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


################################ Fief  ######################################


class FiefView(ListView):
    model = Fief
    context_object_name = 'values'
    template_name = 'geography/fief/dashboard.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs):
        context = super(FiefView, self).get_context_data(**kwargs)
        print(f'	linha 136-------arquivo: {self.kwargs}------- valor:')
        context['slug'] = self.kwargs['slug_region']
        context['slug_country'] = self.kwargs['slug_country']
        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        print(f'	linha 144-------arquivo: {self.kwargs}------- valor:	')
        return Fief.objects.filter(fk_region__slug=self.kwargs['slug_region'])


class FiefAdd(View):
    def get(self, request, slug_country, slug_region):
        form = FiefForm()
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_country, slug_region):
        region = Region.objects.get(slug=slug_region)
        localization = Localization.objects.all()
        form = FiefForm(request.POST)

        if form.is_valid():
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            fief = Fief.objects.create(
                fk_region=region,
                name=form.cleaned_data['name'],
                size=form.cleaned_data['size'],
                description=form.cleaned_data['description'],
            )
            # fief.save()

            for l in form.cleaned_data["localization"]:
                fief.localization.add(localization.get(name=l))
            return redirect('fief', slug_country = slug_country, slug_region=slug_region)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


################################   ######################################
class AddSettlements(View):
    def get(self, request):
        form = SettlementForm()
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)

    def post(self, request):
        form = SettlementForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['economy'])
            economy = form.cleaned_data['economy']
            context = {
                'form': form
            }
            return render(request, 'generic_form.html', context)
################################   ######################################
