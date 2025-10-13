from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Expense, Category, Income
from .serializers import ExpenseSerializer, CategorySerializer, IncomeSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class SignupAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)