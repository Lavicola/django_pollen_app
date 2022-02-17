from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from rest_framework.response import Response
from verify_email import send_verification_email
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from user.forms import UserRegistrationForm,UserLoginForm


def register(request):
    context = {}
    template = loader.get_template('accounts/register.html')
    if (request.method == "GET"):
        template = loader.get_template('accounts/register.html')
    if (request.method == "POST"):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)

    return HttpResponse(template.render(context, request))

def login(request):
    context = {}
    if (request.method == "GET"):
        template = loader.get_template('accounts/login.html')
        return HttpResponse(template.render(context, request))

    if(request.method == "POST"):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            auth_login(request,user)
            return redirect('/nepenthes/overview')

    return Response(status=405)

def logout(request):
    if (request.method == "GET"):
        auth_logout(request)
        return redirect('/nepenthes/overview')


    return Response(status=405)
