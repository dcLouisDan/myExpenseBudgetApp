from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from . import forms
from .models import Expense, Category, Budget


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


@login_required(login_url='login')
def index(request):
    return render(request, "home.html")


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = "budget/list.html"
    context_object_name = "budgets"


class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    fields = [
        'name',
        'total_amount',
        'start_date',
        'end_date',
    ]
    success_url = '/'


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
