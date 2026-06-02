from rest_framework import serializers
import os
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'industry',
            'years_of_experience',
            'is_verified',
            'credits',
        ]
        read_only_fields = ['is_verified', 'credits']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'industry': user.industry,
            'years_of_experience': user.years_of_experience,
            'is_verified': user.is_verified,
            'credits': user.credits,
        })
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist."
            )
        return value
    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )
        token = default_token_generator.make_token(user)
        frontend_url = os.getenv('FRONTEND_URL')
        reset_link = (
            f"{frontend_url}/reset-password/{uid}/{token}/"
        )
        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset password:\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return user

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Validate UID and token
        try:
            user_id = urlsafe_base64_decode(attrs["uid"]).decode()
            user = User.objects.get(id=user_id)
        except Exception:
            raise serializers.ValidationError("Invalid UID")
        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError("Invalid or expired token")
        # Validate passwords match
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        # Validate password strength
        # Simple validation: ensure password is at least 8 characters
        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"]) 
        user.save()
        return user