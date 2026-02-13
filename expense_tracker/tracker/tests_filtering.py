from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Expense, Category
import datetime
from django.utils import timezone

class DateFilterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('expense-list-create')
        self.category = Category.objects.create(name='Food', type='expense', user=self.user)
        
        # Create expenses with different dates
        today = timezone.now()
        yesterday = today - datetime.timedelta(days=1)
        last_month = today - datetime.timedelta(days=30)
        
        Expense.objects.create(user=self.user, category=self.category, amount=10, date=today)
        Expense.objects.create(user=self.user, category=self.category, amount=20, date=yesterday)
        Expense.objects.create(user=self.user, category=self.category, amount=30, date=last_month)

    def test_filter_by_date_range(self):
        # Filter for expenses since yesterday (should include today and yesterday, exclude last month)
        start_date = (timezone.now() - datetime.timedelta(days=2)).date()
        response = self.client.get(f"{self.url}?date__gte={start_date}")
        
        # If filtering works, we expect 2 results. If it ignores the filter, we get 3.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: If date__gte isn't supported, it will likely return all 3.
        # We want to fail if it returns 3.
        self.assertEqual(len(response.data['results']), 2) 
