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
]
