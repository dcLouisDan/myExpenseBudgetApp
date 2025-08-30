from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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
    extra_context = {
        "title": "Budget List",
    }


class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = "budget/detail.html"
    context_object_name = "budget"
    extra_context = {
        "title": "Budget Detail",
    }


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = "budget/create.html"
    form_class = forms.BudgetForm
    success_url = '/budgets'
    extra_context = {
        "title": "Budget Create",
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = "budget/update.html"
    form_class = forms.BudgetForm
    extra_context = {
        "title": "Budget Update",
    }

    def get_success_url(self):
        return reverse_lazy("budget-detail", kwargs={"pk": self.object.pk})



class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    context_object_name = "budget"
    template_name = "budget/delete.html"
    success_url = '/budgets'
    extra_context = {
        'title': 'Budget Delete',
    }


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
