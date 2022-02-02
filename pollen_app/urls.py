from django.urls import path,include
from django.views.generic import TemplateView
from pollen_app import views

app_name = "pollen_app"
urlpatterns = [
    #path('nepenthes/<str:device_name>/', views.device_overview, name='device'),
    path("overview", views.nepenthes_overview_page),
    path("add", views.nepenthes_add_page),

]
