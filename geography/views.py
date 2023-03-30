from audioop import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView
from geography.forms import CountryForm, FiefForm, LocalForm, RegionForm, SettlementForm

from geography.models import Country, Fief, Local, Region, Settlement
from helper.models import Books, Economy, Localization, Resource
# Create your views here.


# def helloWorld(request):
#     return HttpResponse('Hello, World')


navigator = None
################################ Country ######################################


class Countries(ListView):
    model = Country
    context_object_name = 'countries'
    template_name = 'geography/dashboard.html'
    def get_context_data(self, **kwargs, ):
        context = super(Countries, self).get_context_data(**kwargs)
        print(f'	linha 26-------arquivo: {self.kwargs}------- valor:	')
        context['slug_book'] = self.kwargs['slug_book']

        return context

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        country = Country.objects.filter(fk_book__slug = self.kwargs['slug_book'])
        return country

class CountriesAdd(CreateView):
    model = Country
    context_object_name = 'form'
    form_class = CountryForm
    template_name = 'generic_form.html'
    #success_url = redirect('country-list', slug=object.kwargs[''])
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('country-list', kwargs={'slug_book': self.kwargs['slug_book']})
    
    def form_valid(self, form):
        self.object = form.save(False)
        # make change at the object
        book =  Books.objects.get(slug=self.kwargs['slug_book'])
        self.object.fk_book = book
        print(f'	linha 43-------arquivo: {self.object.fk_book}------- valor:	')
        self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())


class CountryUpdate(UpdateView):
    model = Country
    template_name = 'generic_form.html'
    fields = ['name', 'rank']
    slug_field = 'slug'
    slug_url_kwarg = 'slug_country'

    def get_success_url(self):
        #                    URL_name          Name_filed_url : object_atribute
        #BOOK como pegar o valor do objeto
        print(f'	linha 65------arquivo: {self.object.slug}------- valor:	')
        return reverse_lazy('country', kwargs={'slug_country': self.object.slug,'slug_book':self.kwargs['slug_book']})


class CountryView(ListView):
    model = Region
    context_object_name = 'values'
    template_name = 'geography/country/country.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs, ):
        context = super(CountryView, self).get_context_data(**kwargs)

        context['slug_book'] = self.kwargs['slug_book']
        context['slug_country'] = self.kwargs['slug_country']

        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        region = Region.objects.filter(fk_country__slug=self.kwargs['slug_country'])
        country = Country.objects.get(slug=self.kwargs['slug_country'])
        return {
            'region':region,
            'country':country,
        }



################################ Region  ######################################
class RegionView(ListView):
    model = Fief
    context_object_name = 'values'
    template_name = 'geography/region/region.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs):
        context = super(RegionView, self).get_context_data(**kwargs)
        print(f'	linha 136-------arquivo: {self.kwargs}------- valor:')
        context['slug_book'] = self.kwargs['slug_book']
        context['slug_region'] = self.kwargs['slug_region']
        context['slug_country'] = self.kwargs['slug_country']
        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        print(f'	linha 144-------arquivo: {self.kwargs}------- valor:	')
        fief =Fief.objects.filter(fk_region__slug=self.kwargs['slug_region'])
        region = Region.objects.get(fk_country__slug = self.kwargs['slug_country'],slug=self.kwargs['slug_region'])
        return {
            'fief':fief,
            'region':region
        }



class RegionAdd(View):
    def get(self, request, slug_country,slug_book):
        form = RegionForm()
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_country,slug_book):
        country = Country.objects.get(slug=slug_country)
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
            return redirect('country', slug_country=country.slug, slug_book=slug_book)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


class RegionEdit(View):
    def get(self, request,slug_book, slug_country, slug_region):
        form = RegionForm()
        region = Region.objects.get(fk_country__slug = self.kwargs['slug_country'],slug=slug_region)
        form.initial['name'] = region.name
        form.initial['localization'] = region.localization.all()
        form.initial['description'] = region.description
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request,slug_book, slug_country, slug_region):
        country = Country.objects.get(slug=slug_country)

        localization = Localization.objects.all()
        form = RegionForm(request.POST)

        if form.is_valid():
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            region = Region.objects.get(fk_country__slug = slug_country,slug=slug_region)
            region.name = form.cleaned_data['name']
            region.description = form.cleaned_data['description']
            region.save()
            for l in form.cleaned_data["localization"]:
                region.localization.add(localization.get(name=l))
            return redirect('region',slug_book=slug_book, slug_country=country.slug, slug_region= region.slug)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


################################ Fief  ######################################


class FiefView(ListView):
    model = Settlement
    context_object_name = 'values'
    template_name = 'geography/fief/fief.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs):
        context = super(FiefView, self).get_context_data(**kwargs)
        print(f'	linha 136-------arquivo: {self.kwargs}------- valor:')
        context['slug_fief'] = self.kwargs['slug_fief']
        context['slug_region'] = self.kwargs['slug_region']
        context['slug_country'] = self.kwargs['slug_country']
        context['slug_book'] = self.kwargs['slug_book']
        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        print(f'	linha 144-------arquivo: {self.kwargs}------- valor:	')
        settlement = Settlement.objects.filter(
            fk_fief__slug=self.kwargs['slug_fief'])
        fief = Fief.objects.get(fk_region__slug = self.kwargs['slug_region'],slug=self.kwargs['slug_fief'])
        return {
            "fief": fief,
            "settlement": settlement
        }



class FiefAdd(View):
    def get(self, request, slug_book,slug_country, slug_region):
        form = FiefForm()
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_book, slug_country, slug_region):
        region = Region.objects.get(fk_country__slug = self.kwargs['slug_country'],slug=slug_region)
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
            return redirect('region', slug_book=slug_book, slug_country=slug_country, slug_region=slug_region)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


class FiefEdit(View):
    def get(self, request, slug_book, slug_country, slug_region, slug_fief):
        fief = Fief.objects.get(slug= slug_fief)
        form = FiefForm()
        form.initial['name'] = fief.name
        form.initial['localization'] = fief.localization.all()
        form.initial['size'] = fief.size
        form.initial['description'] = fief.description
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_book, slug_country, slug_region, slug_fief):
        region = Region.objects.get(slug=slug_region)
        localization = Localization.objects.all()
        form = FiefForm(request.POST)
        fief = Fief.objects.get(slug= slug_fief)
        if form.is_valid():
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            
            fief.name=form.cleaned_data['name']
            fief.size=form.cleaned_data['size']
            fief.description=form.cleaned_data['description']
            fief.save()

            for l in form.cleaned_data["localization"]:
                fief.localization.add(localization.get(name=l))
            return redirect('fief',slug_book=slug_book, slug_country=slug_country, slug_region=slug_region, slug_fief= fief.slug)
        context = {
            'form': form,
        }
        return render(request, 'generic_form.html', context)


################################ Settlement   ######################################



class SettlementView(ListView):
    model = Local
    context_object_name = 'values'
    template_name = 'geography/settlement/settlement.html'

    # pega o slug que foi enviado para a classe
    def get_context_data(self, **kwargs):
        context = super(SettlementView, self).get_context_data(**kwargs)
        print(f'	linha 136-------arquivo: {self.kwargs}------- valor:')
        context['slug_settlement'] = self.kwargs['slug_settlement']
        context['slug_fief'] = self.kwargs['slug_fief']
        context['slug_region'] = self.kwargs['slug_region']
        context['slug_country'] = self.kwargs['slug_country']
        context['slug_book'] = self.kwargs['slug_book']
        
        print(
            f'	linha 357-------arquivo:views------- valor:{self.kwargs["slug_settlement"]}	')
        context['slug_settlement'] = self.kwargs['slug_settlement']
        print(f'	linha 274-------arquivo:views------- valor:{self.queryset}	')
        return context
    # BOOK cmo filtar

    def get_queryset(self, **kwargs):
        # BOOK acessando model pai pela FK
        # os dois undescore, servem para acessar o valor  dela que no caso é o model
        # Country, acessa pela varial fk_country dentro do Region
        print(f'	linha 144-------arquivo: {self.kwargs}------- valor:	')
        local = Local.objects.filter(
            fk_settlement__slug=self.kwargs['slug_settlement'])
        settlement = Settlement.objects.get(
            slug=self.kwargs['slug_settlement'])
        return {
            'local': local,
            'settlement': settlement
        }



class SettlementAdd(View):
    def get(self, request, slug_book, slug_country, slug_region, slug_fief):
        form = SettlementForm()
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_book, slug_country, slug_region, slug_fief):
        form = SettlementForm(request.POST)
        localization = Localization.objects.all()
        economy = Economy.objects.all()
        if form.is_valid():
            print(form.cleaned_data['economy'])
            economy = form.cleaned_data['economy']

            settlement = Settlement.objects.create(
                fk_fief=Fief.objects.get(slug=slug_fief),
                name=form.cleaned_data['name'],
                type=form.cleaned_data['type'],
                population=form.cleaned_data['population'],
                description=form.cleaned_data['description'],
            )
            # fief.save()

            for l in form.cleaned_data["localization"]:
                settlement.localization.add(localization.get(name=l))
            for e in form.cleaned_data["economy"]:
                settlement.economy.add(economy.get(name=e))
            return redirect('fief',slug_book=slug_book,  slug_country=slug_country, slug_region=slug_region, slug_fief=slug_fief)
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)


class SettlementEdit(View):
    def get(self, request, slug_book, slug_country, slug_region, slug_fief, slug_settlement):
        settlement = Settlement.objects.get(slug=slug_settlement)
        form = SettlementForm()
        form.initial['name'] = settlement.name
        form.initial['population'] = settlement.population
        form.initial['localization'] = settlement.localization.all()
        form.initial['type'] = settlement.type
        form.initial['economy'] = settlement.economy.all()
        form.initial['description'] = settlement.description
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_book, slug_country, slug_region, slug_fief, slug_settlement):
        form = SettlementForm(request.POST)
        localization = Localization.objects.all()
        economy = Economy.objects.all()
        if form.is_valid():
            print(form.cleaned_data['economy'])
            economy = form.cleaned_data['economy']
            settlement = Settlement.objects.get(slug=slug_settlement)
            settlement.name = form.cleaned_data['name']
            settlement.type = form.cleaned_data['type']
            settlement.population = form.cleaned_data['population']
            settlement.description = form.cleaned_data['description']

            settlement.save()

            for l in form.cleaned_data["localization"]:
                settlement.localization.add(localization.get(name=l))
            for e in form.cleaned_data["economy"]:
                settlement.economy.add(economy.get(name=e))
            return redirect('settlement', slug_book=slug_book, slug_country=slug_country, slug_region=slug_region, slug_fief=slug_fief, slug_settlement=settlement.slug)
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)


################################ Local  ######################################



class LocalAdd(View):
    def get(self, request,slug_book, slug_country, slug_region, slug_fief, slug_settlement):
        form = LocalForm()
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)

    def post(self, request, slug_book, slug_country, slug_region, slug_fief, slug_settlement):
        form = LocalForm(request.POST)
        localization = Localization.objects.all()
        resource = Resource.objects.all()
        if form.is_valid():

            local = Local.objects.create(
                fk_settlement=Settlement.objects.get(slug=slug_settlement),
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
            )
            # fief.save()

            for l in form.cleaned_data["localization"]:
                local.localization.add(localization.get(name=l))
            for r in form.cleaned_data["resource"]:
                local.resource.add(resource.get(name=r))
            return redirect('settlement',slug_book=slug_book, slug_country=slug_country, slug_region=slug_region, slug_fief=slug_fief, slug_settlement=slug_settlement)
        context = {
            'form': form
        }
        return render(request, 'generic_form.html', context)



#############################selector###############################

def CharacterType(request, slug_book):
    book =  Books.objects.get(slug= slug_book)
    if book.type == 'murim':
        return redirect('character-list', slug_book=slug_book )
    if book.type == 'fantasy':
        return redirect('character')
