from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignupAPIView,
    ExpenseListCreateView, ExpenseDetailView,
    IncomeListCreateView, IncomeDetailView,
    CategoryListCreateView, CategoryDetailView,
    SummaryView, CategorySummaryView
)
from . import views


#Write your urls here
urlpatterns = [
    #Signup & Login Endpoints
    path("signup/", SignupAPIView.as_view(), name='sign-up'),
    path("login/", TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token-refresh'),

    #Expense Endpoints
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    #Income Endpoints
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('incomes/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),

    #Category Endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'), 

    #Summary Endpoint
    path('summary/', SummaryView.as_view(), name='summary'),

    #Summary by category Endpoint
    path('category/summary/', CategorySummaryView.as_view(), name='category-summary'),
]