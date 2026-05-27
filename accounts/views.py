from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = CustomTokenObtainPairSerializer

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Password reset link sent successfully."
        })

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Password reset successful."
        })