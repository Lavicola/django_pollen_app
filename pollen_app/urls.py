from django.urls import path,include
from pollen_app import views

app_name = "pollen_app"
urlpatterns = [
    path("overview", views.nepenthes_overview_page),
    path("add", views.nepenthes_add_page),
    path("edit", views.edit_nepenthes), #TODO list all plants of user via api
    path("transaction_offers", views.transaction_offer),
    path("transaction_requests", views.transaction_requests),
    path("transaction_overview/<int:author_plant_id>/<int:user_plant_id>", views.transaction_overview),


]
