from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Budget, Expense
from datetime import date

# Create your tests here.

class BudgetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            email="",
            password="password"
        )

    def test_end_date_cannot_be_before_start_date(self):
        budget=Budget.objects.create(
            name='Budget',
            start_date=date(2019, 12, 12),
            end_date=date(2018, 12, 12),
            total_amount=0,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            budget.full_clean()

    def test_total_amount_cannot_be_negative(self):
        budget=Budget.objects.create(
            name='Budget',
            start_date=date.today(),
            end_date=date.today(),
            total_amount=-10,
            user = self.user
        )
        with self.assertRaises(ValidationError):
            budget.full_clean()