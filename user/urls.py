import django.contrib.auth.views
from django.urls import path,include
from django.views.generic import TemplateView
from user import views


urlpatterns = [
    path("register", views.register,name="register"),
    path("login", views.login ,name="login"),
    path("logout", views.logout, name="logout"),
    path('', include('django.contrib.auth.urls')),

]
