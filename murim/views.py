from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from character.froms import CharacterForm
# Create your views here.

from character.models import Characters, GoldEntries, Inventory, TotalGold
from helper.models import Books, ItemType, Periode
from murim.forms import AtributosForm, CharacterProficienceForm, CharacterRealmForm, CharacterSkillForm, GoldForm, InventaryForm, SkillForm
from murim.models import Atribute, CharacterProficience, CharacterRealm, CharacterSkills, Realms, Skills


class CharacterList(ListView):
    model = Characters
    context_object_name = 'characters'
    template_name = 'murim/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterList, self).get_context_data(**kwargs)
        print(f'	linha 13-------arquivo: {self.kwargs}------- valor:')
        print(
            f'	linha 13-------arquivo: {self.kwargs["slug_book"]}------- valor:')
        context['slug_book'] = self.kwargs['slug_book']
        return context


class CharacterAdd(CreateView):
    model = Characters
    form_class = CharacterForm
    context_object_name = 'form'
    template_name = 'murim/character/add.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('character-list', kwargs={'slug_book': self.kwargs['slug_book']})

    def form_valid(self, form):
        self.object = form.save(False)
        self.object
        print(self.object)
        # make change at the object
        book = Books.objects.get(slug=self.kwargs['slug_book'])
        self.object.fk_book = book
        print(f'	linha 37-------arquivo: {self.object.fk_book}------- valor:	')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


def character(request, slug_book, slug_character):
    character = Characters.objects.get(slug=slug_character)
    atribute = Atribute.objects.filter(fk_character= character).order_by('-page').first()

    gold = TotalGold.objects.filter(fk_character= character).order_by('updated_page').last()
    realm = CharacterRealm.objects.filter(fk_character = character).order_by('page').last()
    itens = Inventory.objects.filter(fk_character = character)[0:10]
    skill = CharacterSkills.objects.raw(
        f"""
        SELECT * FROM( 
        SELECT DISTINCT ON (fk_skill_id) * from murim_characterskills WHERE fk_character_id= {character.pk}
        ORDER BY fk_skill_id , id  DESC
        )AS subquery ORDER BY page DESC
        """
)

    try:
       first_skill= list(skill)[0]
    except IndexError:
       first_skill = 0
    
    proficience = CharacterProficience.objects.raw(
        f"""
        SELECT * FROM( 
        SELECT DISTINCT ON (weapon_id_id) * from murim_characterproficience WHERE fk_character_id = {character.pk}
        ORDER BY weapon_id_id , id  DESC
        )AS subquery ORDER BY page DESC
        """
)

    try:
       first_proficience= list(proficience)[0]
    except IndexError:
       first_proficience = 0

    context = {
        'character': character,
        'slug_book': slug_book,
        'atribute':atribute,
        'skills':skill,
        'first_skill': first_skill,
        'realm':realm,
        'proficiences':proficience,
        'first_proficience':first_proficience,
        'gold':gold,
        'itens':itens

    }
    return render(request, 'murim/character/character.html', context)


class characterEdit(View):
    def get(self, request, slug_book, slug_character):
        character = Characters.objects.get(slug=slug_character)
        form = CharacterForm(instance=character)
        context = {
            'form': form
        }
        return render(request, 'murim/character/add.html', context)

    def post(self, request, slug_book, slug_character):
        character = Characters.objects.get(slug=slug_character)
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.changed_data)
            #output
            #['name', 'alias', 'alive', 'birth_year', 'season', 'periode']
            #BOOK
            #verifica se aparece a imagem em dados mudados
            if 'img' in form.changed_data:
                print('imagem foi mudada')
                character.img = form.cleaned_data['img']
            else:    
                print('imagem não foi mudada')
            character.name = form.cleaned_data['name']
            character.alias = form.cleaned_data['alias']
            character.birth_year = form.cleaned_data['birth_year']
            character.alive = form.cleaned_data['alive']
            character.season = form.cleaned_data['season']
            character.periode = form.cleaned_data['periode']
            character.description = form.cleaned_data['description']
            character.save()
            return redirect('character-murim', slug_book= slug_book, slug_character = character.slug)
        context = {
            'form': form
        }
        return render(request, 'murim/character/add.html', context)


##################################         ######################################

class AtributeAd(View):
    def get(self, request, slug_book, slug_character, pk_realm):
        form = AtributosForm()
        realm = Realms.objects.get(pk = self.kwargs['pk_realm'])
        print(f'	linha 143-------arquivo: {realm}  ------- valor:	')
        context = {
            'form': form,
            'realm':realm,
        }
        return render(request, 'murim/atributes/add.html', context)

    def post(self, request, slug_book, slug_character, pk_realm):
        character = Characters.objects.get(slug=slug_character)
        realm = Realms.objects.get(pk = self.kwargs['pk_realm'])
        form = AtributosForm(request.POST)
        print(f'	linha 154-------arquivo: {form.errors}------- valor:	')
        if form.is_valid():
            print(f'	linha 155-------arquivo: entrou no valido-------')
            aux = form.save(commit=False)
            aux.KY = (form.cleaned_data['CTL']*10)
            aux.fk_character = character
            aux.save()
            return redirect('character-murim', slug_book= slug_book, slug_character = character.slug)
        print(f'	linha 160-------arquivo: não foi valido------- valor:{form.is_valid()}	')
        print(f'	linha 143-------arquivo: {form.errors}  ------- valor:	')
        context = {
            'form': form,
            'realm':realm,
        }
        return render(request, 'murim/atributes/add.html', context)

class AtributeAdd(CreateView):
    model = Atribute
    context_object_name = 'form'
    form_class = AtributosForm
    template_name = 'murim/atributes/add.html'

    def get_queryset(self, **kwargs):
        print(f'	linha 164-------arquivo:   ------- valor:	')
        print(f'	linha 164-------arquivo:   ------- valor:	')
        character = Characters.objects.get(slug=self.kwargs['slug_character'])
        realm = Realms.objects.get(pk = self.kwargs['pk_realm'])
        return {
            'realm':realm,
            'character':character,
        }
    def get_context_data(self, **kwargs, ):
        context = super(AtributeAdd, self).get_context_data(**kwargs)
        print(f'	linha 149-------arquivo:   ------- valor:	')

        context['slug_book'] = self.kwargs['slug_book']
        context['slug_character'] = self.kwargs['slug_character']

        return context



    def get_success_url(self, **kwargs):
        return reverse_lazy('character-murim', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_character':self.kwargs['slug_character']})



    def form_valid(self, form):
        self.object = form.save(commit=False)
        # make change at the object
        character = Characters.objects.get(slug=self.kwargs['slug_character'])
       
        self.object.fk_character = character
        print(f'	linha 37-------arquivo: {self.object.fk_character}------- valor:	')
        #self.object.save()

        return HttpResponseRedirect(self.get_success_url())



##################################   SKILL      ######################################
class Skill(CreateView):
    models = Skills
    form_class = SkillForm
    context_object_name = 'form'
    template_name = 'generic_form.html'
    def get_context_data(self, **kwargs):
            context = super(Skill, self).get_context_data(**kwargs)
            print(f'	linha 13-------arquivo: {self.kwargs}------- valor:')
            print(
                f'	linha 13-------arquivo: {self.kwargs["slug_book"]}------- valor:')
            context['slug_book'] = self.kwargs['slug_book']
            context['slug_character'] = self.kwargs['slug_character']
            return context

    def get_success_url(self, **kwargs):
            return reverse_lazy('character-murim', 
                                kwargs={
                'slug_book': self.kwargs['slug_book'], 
                'slug_character':self.kwargs['slug_character']})


class CharacterSkillAdd(CreateView):
    model = CharacterSkills
    context_object_name = 'form'
    form_class = CharacterSkillForm
    template_name = 'murim/skill/add.html'

    def get_context_data(self, **kwargs):
        context = super(CharacterSkillAdd, self).get_context_data(**kwargs)
        print(f'	linha 13-------arquivo: {self.kwargs}------- valor:')
        print(
            f'	linha 13-------arquivo: {self.kwargs["slug_book"]}------- valor:')
        context['slug_book'] = self.kwargs['slug_book']
        context['slug_character'] = self.kwargs['slug_character']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('character-murim', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_character':self.kwargs['slug_character']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # make change at the object
        character = Characters.objects.get(slug=self.kwargs['slug_character'])
        self.object.fk_character = character
        print(f'	linha 37-------arquivo: {self.object.fk_character}------- valor:	')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


##################################   REALM      ######################################


class RealmAdd(CreateView):
    model = CharacterRealm
    context_object_name = 'form'
    form_class = CharacterRealmForm
    template_name = 'generic_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('character-murim', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_character':self.kwargs['slug_character']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # make change at the object
        character = Characters.objects.get(slug=self.kwargs['slug_character'])
        self.object.fk_character = character
        print(f'	linha 37-------arquivo: {self.object.fk_character}------- valor:	')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    



##################################   Proficience      ######################################


class ProficienceAdd(CreateView):
    model = CharacterProficience
    context_object_name = 'form'
    form_class = CharacterProficienceForm
    template_name = 'generic_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('character-murim', kwargs={'slug_book': self.kwargs['slug_book'], 'slug_character':self.kwargs['slug_character']})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # make change at the object
        character = Characters.objects.get(slug=self.kwargs['slug_character'])
        self.object.fk_character = character
        print(f'	linha 37-------arquivo: {self.object.fk_character}------- valor:	')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    



# ############################ INVENTORY ###################################33


class AddItem(View):
    
    def get(self,request, slug_book,slug_character):
        
        form = InventaryForm()
        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)

    def post(self,request,slug_book,slug_character):
        character = Characters.objects.get(slug=slug_character)
        form = InventaryForm(request.POST)
        if form.is_valid():
            aux_form = form.save( commit=False)
            aux_form.fk_character = character
            aux_form.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book = slug_book, slug_character=character.slug)

        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)


class EditItem(View):
    
    def get(self,request, slug_book, slug_character, pk):
        item = Inventory.objects.get(pk=pk)
        form = InventaryForm(instance=item)
        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)

    def post(self,request,slug_book, slug_character, pk):
        character = Characters.objects.get(slug=slug_character)
        item = Inventory.objects.get(pk = pk)
        form = InventaryForm(request.POST)
        if form.is_valid():
            print(f'	linha 363-------arquivo: {form.cleaned_data["name"]}------- valor:')
            item.fk_item_type =form.cleaned_data['fk_item_type']
            item.name = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            item.page = form.cleaned_data['page']
            item.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book=slug_book, slug_character=character.slug)

        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)



class AddCoin(View):
    
    def get(self,request,slug_book,slug_character):
        form = GoldForm()
        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)

    def post(self,request,slug_book,slug_character):
        character = Characters.objects.get(slug=slug_character)
        form = GoldForm(request.POST)
        if form.is_valid():
            value = float(form.cleaned_data["coin"]) * float(form.cleaned_data["value"])
            print(f'linha 485-------arquivo: {value}------- valor:	')
            GoldEntries.objects.create(
                fk_character = character,
                value = value,
                description = form.cleaned_data["description"],
                page = form.cleaned_data["page"],
            )
            try:
                sum  = TotalGold.objects.get(fk_character = character)
                sum.value += value
                sum.updated_page = form.cleaned_data["page"]
                sum.save()
            except:
                TotalGold.objects.create(
                    fk_character = character,
                    value = value,
                    updated_page = form.cleaned_data["page"],
                )
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book=slug_book, slug_character=character.slug)

        context = {
        'form':form
        }
        return render(request, 'generic_form.html',context)