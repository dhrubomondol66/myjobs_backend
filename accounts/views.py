from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
import logging

from .models import User
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

logger = logging.getLogger(__name__)

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
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Forgot password validation failed: {serializer.errors}")
                return Response(
                    {
                        "error": "Validation failed",
                        "details": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response({
                "message": "Password reset link sent successfully to your email."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Forgot password error: {str(e)}")
            return Response(
                {
                    "error": "Failed to process password reset request",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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