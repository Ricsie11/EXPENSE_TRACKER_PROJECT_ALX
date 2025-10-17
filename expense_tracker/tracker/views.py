from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializer, CategorySerializer, IncomeSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Income, Expense
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class SignupAPIView(APIView):
    #...Used try/except should incase the user gets an error while registering
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#Expense ListCreateView
class ExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amount', 'category', 'date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Saves any expense instance created by a user

    def get_queryset(self):  #....Gets all expense of the authenticated user
        return self.request.user.expenses.all()

#Expense DetailView
class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  #....Gets all expense of the authenticated user
        return self.request.user.expenses.all()
    
#Income ListCreateView
class IncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amount', 'category', 'date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Saves any Income instance created by a user

    def get_queryset(self):  #....Gets all income of the authenticated user
        return self.request.user.incomes.all()

#Income DetailView
class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  #....Gets all income of the authenticated user
        return self.request.user.incomes.all()
    

#Category ListCreateView
class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Saves any category instance created by a user

    def get_queryset(self):  #....Gets all category of the authenticated user
        return self.request.user.categories.all()

#Category DetailView
class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  #....Gets all category of the authenticated user
        return self.request.user.categories.all()
    

#..A summary view to get a users total spendings or savings.
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        #..Utilising Django's ORM to calc total income and expense
        total_income = Income.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income - total_expense

        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })
    
#..A Category summary view to get users total expense or income
class CategorySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        #..Get each category name from Expense and group them for total calculation
        expense_summary = Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount'))
        income_summary = Income.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount'))

        return Response({
            "incomes": income_summary,
            "expenses": expense_summary
        })
