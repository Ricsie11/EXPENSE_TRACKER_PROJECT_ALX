from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# ============================
# CATEGORY MODEL
# ============================
class Category(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # Link each category to a user (so users can have their own categories)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        # Display the name and whether it’s income or expense
        return f"{self.name} ({self.type})"


# ============================
# EXPENSE MODEL
# ============================
class Expense(models.Model):
    class Meta:
        ordering = ['-date']  # Newest expenses appear first

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Amount (NGN)'
    )
    # Keeps the expense data even if the related category is deleted
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='expenses'
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Handle case where category might be deleted (avoids AttributeError)
        category_name = self.category.name if self.category else "No Category"
        return f"{self.user.username} - {self.amount} ({category_name})"


# ============================
# INCOME MODEL
# ============================
class Income(models.Model):
    class Meta:
        ordering = ['-date']  # Newest incomes appear first

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='incomes'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Keeps the income data even if the related category is deleted
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='incomes'
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Handle case where category might be deleted
        category_name = self.category.name if self.category else "No Category"
        return f"{self.user.username} - {self.amount} ({category_name})"



# ============================
# USER PROFILE MODEL
# ============================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.FileField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signals to automatically create/update Profile when User is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
