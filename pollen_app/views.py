from django.http import Http404, HttpResponse
from django.template import loader
from pollen_app.models import Nepenthes, Transaction
from pollen_app.forms import addPlantForm
from django.db.models import Q, Count
from django.views.generic import ListView

# Create your views here.
from user.models import CustomUser


def nepenthes_detail_page(request, nepenthes_name):
    try:
        nepenthes = Nepenthes.objects.get(name=nepenthes_name)
    except Nepenthes.DoesNotExist:
        raise Http404("Nepenthes does not exist")
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
                nepenthes = form.save(commit=False)
                nepenthes.owner = request.user
                nepenthes.save()
                message += "Nepenthes {} was successfully saved!".format(nepenthes.name)
                color += "green"
            else:
                for error_field in form.errors.keys():
                    message += "The field {} is required<br>".format(error_field)
                color += "red"
        else:
            message += "Please Login or Register first"
            color += "red"

        context = {
            "color": color,
            "message": message,
        }
        return HttpResponse(template.render(context, request))

    if request.method == "GET":
        template = loader.get_template('nepenthes/add_nepenthes.html')
        return HttpResponse(template.render(context, request))


def transaction_offer(request):
    # TODO email is missing
    context = {}
    template = loader.get_template('nepenthes/transaction_offers.html')
    if request.user.is_authenticated:
        offers = Transaction.objects.raw("""
            SELECT pollen_app_transaction.id,username,t1.name as USER_PLANT_NAME,t1.image,t2.name as AUTHOR_PLANT_NAME,user_plant_id as UPLANTID,author_plant_id as APLANTID,accepted
            FROM pollen_app_transaction
            JOIN user_customuser  on pollen_app_transaction.user_id = user_customuser.id
            JOIN pollen_app_nepenthes t1 on pollen_app_transaction.user_plant_id=t1.id
            JOIN pollen_app_nepenthes t2 on pollen_app_transaction.author_plant_id=t2.id
            WHERE pollen_app_transaction.author_id = {}
            ORDER BY created DESC
            ;""".format(request.user.id))  # TODO maybe not safe?

        context = {
            "data": offers,
        }

    return HttpResponse(template.render(context, request))


def transaction_requests(request):
    context = {}
    template = loader.get_template('nepenthes/transaction_requests.html')
    if request.user.is_authenticated:
        offers = Transaction.objects.raw("""
            SELECT author_plant_id,user_plant_id,pollen_app_transaction.id,username,t1.name as USER_PLANT_NAME,t2.image,t2.name as AUTHOR_PLANT_NAME,email,accepted
            FROM pollen_app_transaction
            JOIN user_customuser  on pollen_app_transaction.author_id = user_customuser.id
            JOIN pollen_app_nepenthes t1 on pollen_app_transaction.user_plant_id=t1.id
            JOIN pollen_app_nepenthes t2 on pollen_app_transaction.author_plant_id=t2.id
            WHERE pollen_app_transaction.user_id = {}
            ORDER BY created DESC
            ;""".format(request.user.id))  # TODO maybe not safe?

        context = {
            "data": offers,
        }

    return HttpResponse(template.render(context, request))


def transaction_overview(request, author_plant_id, user_plant_id):
    context = {}
    template = loader.get_template('nepenthes/transaction_overview.html')
    if request.user.is_authenticated:
        user_id = request.user.id
        transaction = Transaction.objects.filter(author_plant_id=author_plant_id, user_plant_id=user_plant_id).filter(
            Q(author_id=user_id) | Q(user_id=user_id))
        # check if transaction exists and the caller is allowed to see the transaction
        print(transaction.count())
        if transaction.count() != 1:
            raise Http404("Not Allowed :(")
        nepenthes_author = Nepenthes.objects.filter(id=author_plant_id).only("image","name").first()
        nepenthes_user = Nepenthes.objects.filter(id=user_plant_id).only("image","name").first()
        context = {
            "nepenthes_author": nepenthes_author,
            "nepenthes_user": nepenthes_user
        }

    return HttpResponse(template.render(context, request))


# TODO API calls put/delete/vue view
def edit_nepenthes(request):
    context = {}
    template = loader.get_template('nepenthes/edit_nepenthes.html')
    return HttpResponse(template.render(context, request))


def nepenthes_statistics(request):
    most_requested = Transaction.objects.raw("""
        SELECT 1 as id, count(author_plant_id) as total, pollen_app_nepenthes.image,pollen_app_nepenthes.name
        FROM pollen_app_transaction
        JOIN pollen_app_nepenthes  on pollen_app_transaction.author_plant_id = pollen_app_nepenthes.id
        GROUP by author_plant_id
        ORDER BY total DESC
        LIMIT 10
        ;""")
    most_offered = Transaction.objects.raw("""
        SELECT pollen_app_transaction.id,count(user_plant_id) as total, pollen_app_nepenthes.image,pollen_app_nepenthes.name
        FROM pollen_app_transaction
        JOIN pollen_app_nepenthes  on pollen_app_transaction.user_plant_id = pollen_app_nepenthes.id
        GROUP by user_plant_id
        ORDER BY total DESC
        LIMIT 10
        ;""")
    context = {
        "most_requested": most_requested,
        "most_offered": most_offered,
    }

    template = loader.get_template('nepenthes/nepenthes_statistics.html')
    return HttpResponse(template.render(context, request))





