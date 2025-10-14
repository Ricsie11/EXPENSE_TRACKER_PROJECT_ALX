from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SignupAPIView,
    ExpenseListCreateView, ExpenseDetailView,
    IncomeListCreateView, IncomeDetailView,
    CategoryListCreateView, CategoryDetailView,
    SummaryView, CategorySummaryView
)

#Write your urls here
urlpatterns = [
    #Signup & Login Endpoints
    path("signup/", SignupAPIView.as_view(), name='sign-up'),
    path("login/", TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token-refresh'),

    #Expense Endpoints
    path('expense/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expense/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    #Income Endpoints
    path('income/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('income/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),

    #Category Endpoints
    path('category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'), 

    #Summary Endpoint
    path('summary/', SummaryView.as_view(), name='summary'),

    #Summary by category Endpoint
    path('category/summary/', CategorySummaryView.as_view(), name='category-summary')
]