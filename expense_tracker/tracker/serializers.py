from rest_framework import serializers
from .models import Expense, Category, Income
from django.contrib.auth.models import User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        #Stops people from using the same username twice.
    def validate_username(self, value):
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("Username already exists.")
            return value
        
        #Stops people from using the same email twice.
    def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This Email has been taken.")
            return value
        
    def create(self, validated_data):  #Uses Django’s built-in user creator so the password is hashed.
            return User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"]
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['user', 'amount', 'category', 'description', 'date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['user', 'amount', 'category', 'description', 'date']