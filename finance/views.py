from django.shortcuts import render, redirect, get_object_or_404
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
    template_name = "category/index.html"
    context_object_name = "categories"
    extra_context = {
        "title": "Categories",
        "form": forms.CategoryForm,
    }


@login_required(login_url='login')
def category_action_cell(request, pk):
    category = get_object_or_404(Category, pk=pk)
    context = {
        'category': category,
    }
    return render(request, 'category/partials/action_cell.html', context)


@login_required(login_url='login')
def create_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)

        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, "category/partials/table_rows.html", context)


@login_required(login_url='login')
def update_category_form(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = forms.CategoryForm(instance=category)
    context = {
        'form': form,
        'form_url': '/categories/' + str(pk) + '/update',
    }
    return render(request, "category/partials/form.html", context)


@login_required(login_url='login')
def update_category(request, pk):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=pk)
        name = request.POST.get("name")
        if name:
            form = forms.CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()

        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, "category/partials/table_rows.html", context)


@login_required(login_url='login')
def delete_category_form(request, pk):
    category = get_object_or_404(Category, pk=pk)
    context = {
        'category': category,
    }
    return render(request, "category/partials/delete_row.html", context)


@login_required(login_url='login')
def delete_category(request, pk):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=pk)
        category.delete()

        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, "category/partials/table_rows.html", context)


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expense/list.html'
    context_object_name = "expenses"
    extra_context = {
        "title": "Expense List",
    }

    def get_queryset(self):
        return Expense.objects.select_related('category','budget')


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expense/detail.html'
    context_object_name = "expense"
    extra_context = {
        "title": "Expense Detail",
    }

    def get_queryset(self):
        return Expense.objects.select_related('category','budget', 'user')


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = forms.ExpenseForm
    template_name = 'expense/create.html'
    success_url = '/expenses'
    extra_context = {
        "title": "Expense Create",
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = forms.ExpenseForm
    template_name = 'expense/update.html'
    extra_context = {
        "title": "Expense Update",
    }

    def get_success_url(self):
        return reverse_lazy("expense-detail", kwargs={"pk": self.object.pk})


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    context_object_name = "expense"
    template_name = "expense/delete.html"
    success_url = '/expenses'
    extra_context = {
        "title": "Expense Delete",
    }
