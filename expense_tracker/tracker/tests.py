from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Expense, Income, Category
import datetime

class AuthTestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('sign-up')
        self.login_url = reverse('token-obtain-pair')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class ExpenseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('expense-list-create')
        self.category = Category.objects.create(name='Food', type='expense', user=self.user)
        self.expense_data = {
            'category': self.category.id,
            'amount': 50.00,
            'description': 'Lunch',
            'date': datetime.date.today()
        }

    def test_create_expense(self):
        response = self.client.post(self.url, self.expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.get().amount, 50.00)

    def test_list_expenses(self):
        Expense.objects.create(user=self.user, category=self.category, amount=50.00, description='Lunch', date=datetime.date.today())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class SummaryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.summary_url = reverse('summary')

        # Add some data
        self.cat_expense = Category.objects.create(name='Food', type='expense', user=self.user)
        self.cat_income = Category.objects.create(name='Salary', type='income', user=self.user)
        
        Expense.objects.create(user=self.user, category=self.cat_expense, amount=100, date=datetime.date.today())
        Income.objects.create(user=self.user, category=self.cat_income, amount=500, date=datetime.date.today())

    def test_summary_calculation(self):
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check total (all time)
        self.assertEqual(response.data['total']['income'], 500)
        self.assertEqual(response.data['total']['expense'], 100)
        self.assertEqual(response.data['total']['balance'], 400)

        # Check today (since we just created them today)
        self.assertEqual(response.data['today']['income'], 500)
        self.assertEqual(response.data['today']['expense'], 100)
