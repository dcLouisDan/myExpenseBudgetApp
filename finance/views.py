from django.shortcuts import render
from . import forms
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, "home.html")

def login(request):
    form = forms.LoginForm()

    context = {
        'form': form,
    }
    return render(request, "registration/login.html", context)
