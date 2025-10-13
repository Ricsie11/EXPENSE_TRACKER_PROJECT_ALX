from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView

#Write your urls here
urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name='sign-up'),
    path("login/", TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token-refresh'),
]