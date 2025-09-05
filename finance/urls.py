from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("login", views.login_view, name="login"),

    # Budget
    path("budgets", views.BudgetListView.as_view(), name="budget-list"),
    path("budgets/<int:pk>", views.BudgetDetailView.as_view(), name="budget-detail"),
    path("budgets/create", views.BudgetCreateView.as_view(), name="budget-create"),
    path("budgets/<int:pk>/update", views.BudgetUpdateView.as_view(), name="budget-update"),
    path("budgets/<int:pk>/delete", views.BudgetDeleteView.as_view(), name="budget-delete"),

    # Category
    path("categories", views.CategoryListView.as_view(), name="category-list"),
    path("categories/create", views.create_category, name="category-create"),
    path("categories/<int:pk>/action-cell", views.category_action_cell, name="category-action-cell"),
    path("categories/<int:pk>/update-form", views.update_category_form, name="category-update-form"),
    path("categories/<int:pk>/update", views.update_category, name="category-update"),
    path("categories/<int:pk>/delete-form", views.delete_category_form, name="category-delete-form"),
    path("categories/<int:pk>/delete", views.delete_category, name="category-delete"),

    # Expense
    path("expenses", views.ExpenseListView.as_view(), name="expense-list"),
    path("expenses/<int:pk>", views.ExpenseDetailView.as_view(), name="expense-detail"),
    path("expenses/create", views.ExpenseCreateView.as_view(), name="expense-create"),
    path("expenses/<int:pk>/update", views.ExpenseUpdateView.as_view(), name="expense-update"),
    path("expenses/<int:pk>/delete", views.ExpenseDeleteView.as_view(), name="expense-delete"),

]
