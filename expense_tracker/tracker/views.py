from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ExpenseSerializer, 
    CategorySerializer, 
    IncomeSerializer, 
    RegisterSerializer
)
from .models import Income, Expense


# ==========================================================
# 🔐 AUTHENTICATION & USER REGISTRATION VIEWS
# ==========================================================

class SignupAPIView(APIView):
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
    filterset_fields = ['amount', 'category', 'date']

    def perform_create(self, serializer):
        # Automatically link expense to the logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Return only the authenticated user's expenses
        return self.request.user.expenses.all()


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
        return self.request.user.expenses.all()


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
    filterset_fields = ['amount', 'category', 'date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.incomes.all()


class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows users to:
    - Retrieve, update, or delete a specific income record
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.incomes.all()


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
        return self.request.user.categories.all()


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    """
    Allows users to:
    - Retrieve, update, or delete a specific category
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.categories.all()


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

        total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })


class CategorySummaryView(APIView):
    """
    Returns a breakdown of total income and expenses by category.
    Useful for visualizing spending patterns.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Aggregate total expenses per category
        expense_summary = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))
        income_summary = Income.objects.filter(user=user).values('category__name').annotate(total=Sum('amount'))

        return Response({
            "incomes": income_summary,
            "expenses": expense_summary
        })




