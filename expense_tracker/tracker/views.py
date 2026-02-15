from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ExpenseSerializer, 
    CategorySerializer, 
    IncomeSerializer, 
    RegisterSerializer,
    UserSerializer
)
from .models import Income, Expense
from .filters import ExpenseFilter, IncomeFilter


# ==========================================================
# 🔐 AUTHENTICATION & USER REGISTRATION VIEWS
# ==========================================================


def home(request):
    return HttpResponse("Expense Tracker API is running")

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    """
    Handle user registration.
    Returns JWT access & refresh tokens upon successful registration.
    """

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)

            # Return validation errors if serializer fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch any unexpected errors (e.g., DB or serialization issues)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return Response({'profile_pic': profile.profile_pic.url}, status=status.HTTP_200_OK)
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================
# 💸 EXPENSE VIEWS
# ==========================================================

class ExpenseListCreateView(ListCreateAPIView):
    """
    Allows users to:
    - List all their expenses
    - Create new expense records
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter

    def perform_create(self, serializer):
        # Automatically link expense to the logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Return only the authenticated user's expenses
        return Expense.objects.filter(user=self.request.user)


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows users to:
    - Retrieve details of a single expense
    - Update or delete their own expense
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict access to user's own expenses
        return Expense.objects.filter(user=self.request.user)


# ==========================================================
# 💰 INCOME VIEWS
# ==========================================================

class IncomeListCreateView(ListCreateAPIView):
    """
    Allows users to:
    - List all their income records
    - Create new income entries
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows users to:
    - Retrieve, update, or delete a specific income record
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


# ==========================================================
# 🏷️ CATEGORY VIEWS
# ==========================================================

class CategoryListCreateView(ListCreateAPIView):
    """
    Allows users to:
    - List all their categories
    - Create new category entries
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows users to:
    - Retrieve, update, or delete a specific category
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


# ==========================================================
# 📊 SUMMARY & REPORT VIEWS
# ==========================================================

class SummaryView(APIView):
    """
    Returns a summary of a user's financial overview:
    - Total income
    - Total expense
    - Net balance
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.localdate()

        def get_totals(start_date=None, end_date=None):
            expenses = Expense.objects.filter(user=user)
            incomes = Income.objects.filter(user=user)

            if start_date:
                expenses = expenses.filter(date__date__gte=start_date)
                incomes = incomes.filter(date__date__gte=start_date)
            
            if end_date:
                expenses = expenses.filter(date__date__lte=end_date)
                incomes = incomes.filter(date__date__lte=end_date)

            total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
            total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
            
            return {
                "income": total_income,
                "expense": total_expense,
                "balance": total_income - total_expense
            }

        # Calculate dates
        start_week = today - timedelta(days=today.weekday()) # Monday of this week
        start_month = today.replace(day=1)
        start_year = today.replace(month=1, day=1)

        return Response({
            "today": get_totals(start_date=today, end_date=today),
            "week": get_totals(start_date=start_week),
            "month": get_totals(start_date=start_month),
            "year": get_totals(start_date=start_year),
            "total": get_totals() # All time
        })


class CategorySummaryView(APIView):
    """
    Returns a breakdown of total income and expenses by category.
    Useful for visualizing spending patterns.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.localdate()

        def get_category_totals(start_date=None, end_date=None):
            expenses = Expense.objects.filter(user=user)
            incomes = Income.objects.filter(user=user)

            if start_date:
                expenses = expenses.filter(date__date__gte=start_date)
                incomes = incomes.filter(date__date__gte=start_date)
            
            if end_date:
                expenses = expenses.filter(date__date__lte=end_date)
                incomes = incomes.filter(date__date__lte=end_date)

            expense_summary = expenses.values('category__name').annotate(total=Sum('amount'))
            income_summary = incomes.values('category__name').annotate(total=Sum('amount'))
            
            return {
                "incomes": income_summary,
                "expenses": expense_summary
            }

        # Calculate dates
        start_week = today - timedelta(days=today.weekday())
        start_month = today.replace(day=1)
        start_year = today.replace(month=1, day=1)

        return Response({
            "today": get_category_totals(start_date=today, end_date=today),
            "week": get_category_totals(start_date=start_week),
            "month": get_category_totals(start_date=start_month),
            "year": get_category_totals(start_date=start_year),
            "total": get_category_totals()
        })



