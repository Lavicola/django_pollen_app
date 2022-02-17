from django.urls import path,include
from pollen_app import views

app_name = "pollen_app"
urlpatterns = [
    path("overview", views.nepenthes_overview_page),
    path("add", views.nepenthes_add_page),
]
