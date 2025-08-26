from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, "home.html")

def login_view(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = forms.LoginForm()

    context = {
        'form': form,
    }
    return render(request, "registration/login.html", context)
