from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Expense(models.Model):
    class Meta:
        ordering = ['-date']
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount (NGN)')
    # This keeps expense data even if a category is removed.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='expenses')
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.category.name})"


class Income(models.Model):
    class Meta:
        ordering = ['-date']
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # This keeps income data even if a category is removed.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='incomes') 
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.user.username} - {self.amount}"

