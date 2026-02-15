from .models import Expense, Category, Income, Profile
from django.contrib.auth.models import User
from rest_framework import serializers


# ============================
# PROFILE SERIALIZER
# ============================
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic']


# ============================
# USER REGISTRATION SERIALIZER
# ============================
class RegisterSerializer(serializers.ModelSerializer):
    # Password should never be readable in API responses
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name']

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
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'profile_pic']

    def get_profile_pic(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_pic:
            return obj.profile.profile_pic.url
        return None


# ============================
# EXPENSE SERIALIZER
# ============================
class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'category', 'category_name', 'description', 'date']
        read_only_fields = ['user']  # Ensures users can't create expenses for others

    def get_category_name(self, obj):
        try:
            return obj.category.name if obj.category else "No Category"
        except Exception:
            return "No Category"


# ============================
# CATEGORY SERIALIZER
# ============================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'type']
        read_only_fields = ['user']  # Link to user automatically in view



# ============================
# INCOME SERIALIZER
# ============================
class IncomeSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Income
        fields = ['id', 'user', 'amount', 'category', 'category_name', 'description', 'date']
        read_only_fields = ['user']  # Prevent users from assigning income to others

    def get_category_name(self, obj):
        return obj.category.name if obj.category else "No Category"


