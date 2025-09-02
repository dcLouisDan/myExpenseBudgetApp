import datetime
from tabnanny import check

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Budget(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date')
        if self.total_amount < 0:
            raise ValidationError('Total amount must be greater than 0')

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_name'),
            models.CheckConstraint(check=models.Q(total_amount__gte=0), name='amount_non_negative'),
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    description = models.TextField()
    date = models.DateField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.date > datetime.date.today():
            raise ValidationError('Date must be before or equal to today')
        if self.amount < 0:
            raise ValidationError('Amount must be greater than 0')

    class Meta:
        ordering = ['-created_at']
