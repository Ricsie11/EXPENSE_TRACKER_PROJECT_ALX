from rest_framework import serializers
from .models import Expense, Category, Income
from django.contrib.auth.models import User


# ============================
# USER REGISTRATION SERIALIZER
# ============================
class RegisterSerializer(serializers.ModelSerializer):
    # Password should never be readable in API responses
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Custom validation to ensure both username and email are unique
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email has been taken."})

        return attrs

    # Create user using Django’s built-in helper to hash the password automatically
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ============================
# SIMPLE USER DATA SERIALIZER
# ============================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ============================
# EXPENSE SERIALIZER
# ============================
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'category', 'description', 'date']
        read_only_fields = ['user']  # Ensures users can't create expenses for others


# ============================
# CATEGORY SERIALIZER
# ============================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']
        read_only_fields = ['user']  # Only the owner (user) can manage their categories


# ============================
# INCOME SERIALIZER
# ============================
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'category', 'description', 'date']
        read_only_fields = ['user']  # Prevent users from assigning income to others
