
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from utils.rank import Rank

from .models import CharacterRealm, CharacterSkills, Characters, GoldEntries, Inventory, Skills, Status, Proficience, CharacterProficience, TotalGold
#-------------------Forms
from .froms import CharacterForm, CharacterRealmForm, GoldForm, InventaryForm, ProficienceForm, ProfileForm, StatusForm, SkillForm, CharacterSkillForm

from helper.models import WeaponsType
# Create your views here.



# BOOK colocar view


class CharacterList(ListView):
    model = Characters  # aqui coloca a classe que está vindo
    template_name = 'character/home.html'
    # tem o retorno do contexto implicito, ele vai como o nome do model em caixa baixo 'characters' e apartir dele pode usar
    # loops para mostrar as informações


def characterDetailView(request, slug):
    character = Characters.objects.get(slug=slug)
    # pega o registro com a ultima pagina alterada.
    status = Status.objects.filter(
        fk_character=character).order_by('page').last()
    
    # proficiencia = Proficience.objects.filter(
    #     fk_character=character).order_by('weapon', '-pk').distinct('weapon')
    
    # proficiencia_page = proficiencia.all().order_by('weapon', 'page').values().last()

    # skill = CharacterSkills.objects.filter(
    #     character_id=character).order_by('-page')[0:10]
    
    # skill = CharacterSkills.objects.filter(character_id=character).order_by('skill_id','-page').distinct('skill_id')
    # s_skill = sorted(skill, key=operator.attrgetter('page'), reverse=True)
    
    skill = CharacterSkills.objects.raw(
        f"""
        SELECT * FROM( 
	    SELECT DISTINCT ON (skill_id_id) * from character_characterskills WHERE character_id_id = {character.pk}
        ORDER BY skill_id_id , id  DESC
        )AS subquery ORDER BY page DESC
        """
    )

    proficience = CharacterProficience.objects.raw(
        f"""
        SELECT * FROM( 
	SELECT DISTINCT ON (weapon_id_id) * from character_characterproficience WHERE character_id_id = {character.pk}
        ORDER BY weapon_id_id , id  DESC
    )AS subquery ORDER BY page DESC
        """
    )

    items = Inventory.objects.filter(fk_character=character).order_by('-page')[0:10]


    realm = CharacterRealm.objects.filter(fk_character=character.pk).order_by('page').last()

    gold = TotalGold.objects.get(fk_character = character)

    update_page_skill  = 0
    update_page_proficience  = 0
    try:
        # update_page = CharacterSkills.objects.filter(character_id=character).order_by('page').values().last()
        update_page_skill = skill[0].page #pega o ultimo registro, sem precisar fazer novas querrys 
      
    except:
        update_page  = 0
        
    try:
        update_page_proficience = proficience[0].page #pega o ultimo registro, sem precisar fazer novas querrys 
    except:
       
        update_page_proficience  = 0
    

    
    context = {
        's': status,
        'c': character,
        'proficiences':proficience,
        'realm':realm,
        'skills': skill,
        'proficience_page':update_page_proficience,
        'skill_page':update_page_skill,
        'items':items,
        'gold':gold
    }



    return render(request, 'character/character-murim.html', context)


class characterPage(DetailView):
    model = Characters
    template_name = 'character/character-murim.html'
    context_object_name = 'character'  # muda o nome padrão do contexto


# class AddCharacter(CreateView):
#     model = Characters
#     template_name = 'character/character/add.html'
#     fields = ['name', 'alias', 'birth_year', 'season', 'periode']

# def store_file(file):
#     with open('images/image.png','wb+') as dest: # images/images é o caminho que
#         for chunk in file.chunks():
#             dest.write(chunk)


class AddCharacter(View):
    def get(self,request):
        form = CharacterForm()
        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)

    def post(self,request):
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(f'	linha -------arquivo:   ------- valor:	')
            print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            print(form.instance.slug)
            return redirect('character-page', slug=form.instance.slug)

        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)




class EditCharacter(UpdateView):
    model = Characters
    template_name = 'character/character/add.html'
    fields = ['img','name', 'alias', 'birth_year', 'season', 'periode','description']


class DeleteCharacter(DeleteView):
    model = Characters
    template_name = 'character/character_del.html'
    success_url = reverse_lazy('character')


#################### realm #############################


def addRealm(request, slug):
    character = Characters.objects.get(slug=slug)
    if request.method == 'POST':
        form = CharacterRealmForm(request.POST)
        if form.is_valid():
            form_aux = form.save(commit=False)
            form_aux.fk_character = character
            form_aux.save()

            # não é boa pratica redirecionar na mesma pagina
            return redirect('character-page', slug=slug)

    else:
        form = CharacterRealmForm()
    context = {
        'form':form
    }

    return render(request, 'character/skill/add.html', context)





#################### skill#############################


def skillAdd(request, slug):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():

            form.save()
            # não é boa pratica redirecionar na mesma pagina
            return redirect('character-page', slug=slug)

    else:
        form = SkillForm()
    context = {
        'form':form
    }

    return render(request, 'character/skill/add.html', context)




def skillCharacter(request, slug):
    character = Characters.objects.get(slug=slug)
    if request.method == 'POST':
        form = CharacterSkillForm(request.POST)
        if form.is_valid():
            print(f'	linha 144-------arquivo: entrou no if   ------- valor:	')
            form_aux = form.save(commit=False)
            form_aux.character_id = character
            form_aux.save()
            # não é boa pratica redirecionar na mesma pagina
            return redirect('character-page', slug=slug)
        else:
            print(f'	linha 151-------arquivo: NÂO entrou no if   ------- valor:	')

    else:
        form = CharacterSkillForm()
    context = {
        'form': form,
        'slug': slug,
    }

    return render(request, 'character/skill/character.html', context)




def editSkillCharacter(request, slug, pk):
    character = Characters.objects.get(slug=slug)
    existing_skill = CharacterSkills.objects.get(pk=pk)
    if request.method == 'POST':
        form = CharacterSkillForm(request.POST)
        if form.is_valid():
            print(f'	linha 144-------arquivo: entrou no if   ------- valor:	')
            form_aux = form.save(commit=False)
            form_aux.character_id = character
            form_aux.save()
            # não é boa pratica redirecionar na mesma pagina
            return redirect('character-page', slug=slug)
        else:
            print(f'	linha 151-------arquivo: NÂO entrou no if   ------- valor:	')

    else:
        form = CharacterSkillForm(instance=existing_skill)
    context = {
        'form': form,
        'slug':slug
    }

    return render(request, 'character/skill/character.html', context)


############################ status###########################

def statusAdd(request, slug):
    character = Characters.objects.get(slug=slug)
    if request.method == 'POST':
        #salva os dados do formulario, e imprede que sejam apagados caso de erro
        form = StatusForm(request.POST)
        if form.is_valid():
            teste = form.save(commit=False)
            teste.fk_character = character
            teste.save()
            # Status.objects.create(
            #     fk_character =character,
            #     STR=form.cleaned_data['STR'],
            #     AGI=form.cleaned_data['AGI'],
            #     DEX=form.cleaned_data['DEX'],
            #     RES=form.cleaned_data['RES'],
            #     CON=form.cleaned_data['CON'],
            #     KY=form.cleaned_data['KY'],
            #     CTL=form.cleaned_data['CTL'],
            #     PER=form.cleaned_data['PER'],
            #     page=form.cleaned_data['page'],
            #     )
            return redirect('character-page', slug=slug)

    else:
        form = StatusForm()

        # não é boa pratica redirecionar na mesma pagina
       

    context = {
        'form':form
    }

    return render(request, 'character/status/add.html', context)


def statusEdit(request, slug,pk):
    character = Characters.objects.get(slug=slug)
    status = Status.objects.get(pk=pk)

    if request.method == 'POST':
        #salva os dados do formulario, e imprede que sejam apagados caso de erro
        form = StatusForm(request.POST)
        if form.is_valid():
            status.STR=form.cleaned_data['STR']
            status.AGI=form.cleaned_data['AGI']
            status.DEX=form.cleaned_data['DEX']
            status.RES=form.cleaned_data['RES']
            status.CON=form.cleaned_data['CON']
            status.KY=form.cleaned_data['KY']
            status.CTL=form.cleaned_data['CTL']
            status.PER=form.cleaned_data['PER']
            status.page=form.cleaned_data['page']
            status.save()
            return redirect('character-page', slug=slug)

    else:
        form = StatusForm()
        form.initial['STR'] = status.STR
        form.initial['AGI'] =status.AGI
        form.initial['DEX'] = status.DEX
        form.initial['RES']= status.RES
        form.initial['CON']= status.CON
        form.initial['KY']= status.KY
        form.initial['CTL']= status.CTL
        form.initial['PER']= status.PER
        form.initial['page']= status.page


        # não é boa pratica redirecionar na mesma pagina
       

    context = {
        'form':form
    }

    return render(request, 'character/status/add.html', context)


###############################profifience###########################



def proficienceAdd(request, slug):
    character = Characters.objects.get(slug=slug)
    proficience =  Proficience.objects.all()
    weapon =  WeaponsType.objects.all()

    if request.method == 'POST':
        form = ProficienceForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print(form.cleaned_data)
            CharacterProficience.objects.create(
                character_id=character,
                proficience_id=proficience.get(pk=form.cleaned_data['proficience']),
                weapon_id = weapon.get(pk=form.cleaned_data['weapon']),
                page = form.cleaned_data['page'],
                level = form.cleaned_data['level'],
            )

        # não é boa pratica redirecionar na mesma pagina
            return redirect('character-page', slug=slug)
    else:
        form = ProficienceForm()

    context = {
        'form':form
    }

    return render(request, 'character/proficience/add.html', context)



# class EditProficience(UpdateView):
#     model = CharacterProficience
#     context_object_name = 'proficience'
#     template_name = 'character/proficience/edit.html'
#     fields = ['weapon', 'proficience_id', 'level', 'page']
#     #success_url = '/characters/details/cassandra-mirrage-spear-1/'
#     success_url = '/'



def editProficience(request,slug, pk):
    charPro = CharacterProficience.objects.get(pk=pk)
    proficience =  Proficience.objects.all()
    weapon =  WeaponsType.objects.all()
    
    if request.method == 'POST':
        form = ProficienceForm(request.POST)
        if form.is_valid():
            charPro.proficience_id=proficience.get(pk=form.cleaned_data['proficience'])
            charPro.weapon_id = weapon.get(pk=form.cleaned_data['weapon'])
            charPro.page = form.cleaned_data['page']
            charPro.level = form.cleaned_data['level']
            charPro.save()
            return redirect('character-page', slug)
        

        
    else:#caso get, gera esse daqui
        form = ProficienceForm()
        form.initial['page'] = charPro.page
        form.initial['level'] =charPro.level
        form.initial['weapon'] = [f'{charPro.weapon_id.pk}']
        form.initial['proficience']= [f'{charPro.proficience_id.pk}']


    context = {
        'form':form#caso o form for POST, mas invalido, ele passa passa direto para o post, enviando os dados, assim não precisando reescerver
    }
    return render(request, 'character/proficience/add.html',context)



############################ INVENTORY ###################################33


class AddItem(View):
    
    def get(self,request, slug):
        
        form = InventaryForm()
        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)

    def post(self,request,slug):
        character = Characters.objects.get(slug=slug)
        form = InventaryForm(request.POST)
        if form.is_valid():
            aux_form = form.save( commit=False)
            aux_form.fk_character = character
            aux_form.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-page', slug=character.slug)

        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)


class EditItem(View):
    
    def get(self,request, slug, pk):
        item = Inventory.objects.get(pk=pk)
        form = InventaryForm(instance=item)
        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)

    def post(self,request,slug, pk):
        character = Characters.objects.get(slug=slug)
        form = InventaryForm(request.POST)
        if form.is_valid():
            aux_form = form.save( commit=False)
            aux_form.fk_character = character
            aux_form.save()
            # print(form.instance)#instance serve para pegar o valor do model no caso CHARACTERS
            # print(form.instance.slug)
            return redirect('character-page', slug=character.slug)

        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)



class AddCoin(View):
    
    def get(self,request, slug):
        form = GoldForm()
        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)

    def post(self,request,slug):
        character = Characters.objects.get(slug=slug)
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
            return redirect('character-page', slug=character.slug)

        context = {
        'form':form
        }
        return render(request, 'character/character/add.html',context)