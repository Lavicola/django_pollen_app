from django.http import Http404, HttpResponse
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
    if (request.user.is_authenticated):
        user_nepenthes = Nepenthes.objects.filter(owner_id=request.user.id)
    else:
        user_nepenthes = []
    context = {
        "nepenthes": nepenthes,
        "user_nepenthes": user_nepenthes,
    }
    template = loader.get_template('nepenthes/nepenthes_overview_page.html')
    return HttpResponse(template.render(context, request))


def nepenthes_add_page(request):
    context = {}
    template = loader.get_template('nepenthes/add_nepenthes.html')  # TODO POST needs a success/failure Message

    if request.method == "POST":
        message = ""
        color = ""
        if request.user.is_authenticated:
            form = addPlantForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['name']
                flower_status = form.cleaned_data['flower_status']
                sex = form.cleaned_data['sex']
                image = form.cleaned_data['image']
                nepenthes = Nepenthes(name=name, sex=sex, flower=flower_status, image=image, owner_id=request.user.id)
                nepenthes.save()
                message += "Nepenthes {} was successfully saved!".format(nepenthes.name)
                color += "green"
            else:
                for error_field in form.errors.keys():
                    message+= "The field {} is required<br>".format(error_field)
                color += "red"
            context ={
                "color": color,
                "message": message,
            }
        else:
            message += "Please Login or Register first"
            color +="red"

        context ={
            "color": color,
            "message": message,
        }
        return HttpResponse(template.render(context, request))

    if request.method == "GET":
        template = loader.get_template('nepenthes/add_nepenthes.html')
        return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))
    template = loader.get_template('nepenthes/add_nepenthes.html')
    return HttpResponse(template.render(context, request))
