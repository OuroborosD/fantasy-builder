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
from murim.models import Atribute, CharacterProficience, CharacterRealm, CharacterSkills, Realms, SkillRank, Skills


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
        # 'realm_limit':{
        #             'physic':sum([realm.fk_realm.bonus_physic, st]),
        #             'spiritual':sum([realm.fk_realm.bonus_spiritual, realm.fk_realm.bonus_spiritual]),
        #             },
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
    def get(self, request, slug_book, slug_character, pk_realm, pk):
        atribute = Atribute.objects.get(pk=pk)
        form = AtributosForm(instance= atribute)
        realm = Realms.objects.get(pk = self.kwargs['pk_realm'])
        print(f'	linha 143-------arquivo: {realm}  ------- valor:	')
        context = {
            'form': form,
            'realm':realm,
        }
        return render(request, 'murim/atributes/add.html', context)

    def post(self, request, slug_book, slug_character, pk_realm,pk):
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



class Skill2(View):
    def get(self, request, slug_book, slug_character):
        form = SkillForm()
        context = {
            'form': form,
        }
        return render(request, 'murim/skill/add_skill.html', context)

    def post(self, request, slug_book, slug_character):
        skillrank = SkillRank.objects.all
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            # BOOK
            # para salvar many-to-many feild, que no caso é outra tabela
            # crie o objeto sabe ele, e depois adicione o atributo com o metodo .add()
            
            # fief.name=form.cleaned_data['name']
            # fief.size=form.cleaned_data['size']
            # fief.description=form.cleaned_data['description']
            # fief.save()

            # for l in form.cleaned_data["atributes"]:
            #     fief.localization.add(localization.get(name=l))
            return redirect('skill-add',slug_book=slug_book, slug_character=slug_character)
        rank_skill = form["rank"].value()
      
        print(f'	linha 271-------arquivo: {rank_skill}------- valor:')
        
        try:
            rank = SkillRank.objects.get(pk=rank_skill)
            bonus= rank.multiplier
            time = rank.time
        except:
            rank = 0
        context = {
            'form': SkillForm(request.POST,bonus = {'bonus_5' : bonus, 'time':time}),
            'rank':rank,
        }
        return render(request, 'murim/skill/add_skill.html', context)



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

class EditSkill(View):
    
    def get(self,request, slug_book, slug_character, pk):
        skill = CharacterSkills.objects.get(pk=pk)
        form = CharacterSkillForm(instance=skill)
        context = {
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/skill/edit.html',context)

    def post(self,request,slug_book, slug_character, pk):
        skill = CharacterSkills.objects.get(pk=pk)
        form = CharacterSkillForm(request.POST)
        if form.is_valid():
            skill.fk_skill =form.cleaned_data['fk_skill']
            skill.mastery = form.cleaned_data['mastery']
            skill.page = form.cleaned_data['page']
            skill.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book=slug_book, slug_character=slug_character)

        context = {
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/skill/edit.html',context)

def deleteSkill(request, slug_book,slug_character,pk):
    item = CharacterSkills.objects.get(pk = pk)
    item.delete()
    return redirect('character-murim', slug_book= slug_book, slug_character=slug_character)

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
    


class EditProficience(View):
    
    def get(self,request, slug_book, slug_character, pk):
        proficience = CharacterProficience.objects.get(pk=pk)
        form = CharacterProficienceForm(instance=proficience)
        context = {
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/proficience/edit.html',context)

    def post(self,request,slug_book, slug_character, pk):
        proficience = CharacterProficience.objects.get(pk=pk)
        form = CharacterProficienceForm(request.POST)
        if form.is_valid():
            proficience.fk_proficience =form.cleaned_data['fk_proficience']
            proficience.weapon_id = form.cleaned_data['weapon_id']
            proficience.level = form.cleaned_data['level']
            proficience.page = form.cleaned_data['page']
            proficience.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book=slug_book, slug_character=slug_character)

        context = {
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/proficience/edit.html',context)

def deleteProficience(request, slug_book,slug_character,pk):
    item = CharacterProficience.objects.get(pk = pk)
    item.delete()
    return redirect('character-murim', slug_book= slug_book, slug_character=slug_character)


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
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/item/edit.html',context)

    def post(self,request,slug_book, slug_character, pk):
        character = Characters.objects.get(slug=slug_character)
        item = Inventory.objects.get(pk = pk)
        form = InventaryForm(request.POST)
        if form.is_valid():
            item.fk_item_type =form.cleaned_data['fk_item_type']
            item.name = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            item.page = form.cleaned_data['page']
            item.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-murim', slug_book=slug_book, slug_character=character.slug)

        context = {
        'form':form,
        'slug_book':slug_book,
        'slug_character':slug_character,
        'pk':pk,
        }
        return render(request, 'murim/item/edit.html',context)


def deleteItem(request, slug_book,slug_character,pk):
    item = Inventory.objects.get(pk = pk)
    item.delete()
    return redirect('character-murim', slug_book= slug_book, slug_character=slug_character)

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