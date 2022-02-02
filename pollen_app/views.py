from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import loader
from pollen_app.models import Nepenthes
from pollen_app.forms import addPlantForm

# Create your views here.

def nepenthes_detail_page(request, nepenthes_name):
    try:
        nepenthes = Nepenthes.objects.get(name=nepenthes_name)
    except Nepenthes.DoesNotExist:
        raise Http404("Nepentthes does not exist")
    context = {
        "nepenthes": nepenthes,
    }
    template = loader.get_template('nepenthes/nepenthes_detail_page.html')
    return HttpResponse(template.render(context, request))


def nepenthes_overview_page(request):
    nepenthes = Nepenthes.objects.all()
    context = {
        "nepenthes": nepenthes,
    }
    template = loader.get_template('nepenthes/nepenthes_overview_page.html')
    return HttpResponse(template.render(context, request))



def nepenthes_add_page(request):
    context = {}
    template = loader.get_template('nepenthes/add_nepenthes.html')

    if request.method == "POST" and request.user.is_authenticated:
        # add plant to database if valid
        form = addPlantForm(request.POST,request.FILES)
        if  form.is_valid():
            print("validated!")
            name = form.cleaned_data['nepenthes']
            flower_status = form.cleaned_data['flower_status']
            sex = form.cleaned_data['sex']
            image = form.cleaned_data['image']
            nepenthes  = Nepenthes(name=name,sex=sex,flower=flower_status,image=image,owner_id=request.user.id)
            nepenthes.save()

        return HttpResponse(template.render(context, request))
    return render(request,"nepenthes/add_nepenthes.html",{"form":addPlantForm})
    template = loader.get_template('nepenthes/add_nepenthes.html')
    return HttpResponse(template.render(context, request))


