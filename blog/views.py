from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement
 
# Create your views here.

def post_list(request):
    Animals=Animal.objects.all()
    Equipements=Equipement.objects.all()
    
    return render(request, 'blog/post_list.html',{"Animals":Animals,"Equipements":Equipements})


def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'blog/animal_list.html', {'animals': animals})
 
def animal_detail(request, id_animal):
    mangeoire = get_object_or_404(Equipement, id_equip='Mangeoire')
    roue = get_object_or_404(Equipement, id_equip='Roue')
    litière = get_object_or_404(Equipement, id_equip='Litière')
    nid = get_object_or_404(Equipement, id_equip='Nid')
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
    
    
    if request.method == "POST":
            form = MoveForm(request.POST, instance=animal)
            if form.is_valid():
                destination=form.data["lieu"]
                
                if destination == "Roue":
                    if roue.disponibilite=="occupé":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':"La roue est déjà occupée !"}))
                    elif animal.etat != "repus":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':f"{animal} ne veux pas faire d'exercice ! "}))
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        animal.etat='fatigué'
                        form.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        return redirect('animal_detail', id_animal=id_animal)
                
                elif destination=="Mangeoire":
                    if mangeoire.disponibilite=="occupé":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':"Le mangeoire est déjà occupé !"}))
                    elif animal.etat != "affamé":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':f"{animal} n'a pas faim ! "}))
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        animal.etat='repus'
                        form.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        return redirect('animal_detail', id_animal=id_animal)
                
                elif destination=="Nid":
                    if nid.disponibilite=="occupé":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':"Le nid est déjà occupé !"}))
                    elif animal.etat != "fatigué":
                        return(render(request,"blog/animal_detail.html",{'animal': animal, 'message':f"{animal} n'est pas fatigué ! "}))
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        animal.etat='endormi'
                        form.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        return redirect('animal_detail', id_animal=id_animal)
                
                else:
                    if ancien_lieu.id_equip=="Nid":
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        animal.etat='affamé'
                        form.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                        nouveau_lieu.save()
                        return redirect('animal_detail', id_animal=id_animal)
                    else:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()
                        
                        form.save()
                        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                        nouveau_lieu.save()
                        return redirect('animal_detail', id_animal=id_animal)

               
    else:
        form = MoveForm() 
    return render(request,
                  'blog/animal_detail.html',
                  {'animal':animal,'lieu':animal.lieu,  'form': form})