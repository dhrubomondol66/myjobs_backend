from rest_framework import serializers
import os
import requests
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
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
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
        reset_link = (
            f"{frontend_url}/reset-password/{uid}/{token}/"
        )
        
        # Send email using EmailJS
        emailjs_service_id = os.getenv('EMAILJS_SERVICE_ID')
        emailjs_template_id = os.getenv('EMAILJS_TEMPLATE_ID')
        emailjs_public_key = os.getenv('EMAILJS_PUBLIC_KEY')
        sender_email = os.getenv('EMAILJS_SENDER_EMAIL')
        
        # Correct EmailJS API format
        emailjs_payload = {
            'service_id': emailjs_service_id,
            'template_id': emailjs_template_id,
            'user_id': emailjs_public_key,
            'template_params': {
                'to_email': email,
                'from_email': sender_email,
                'user_name': user.username,
                'reset_link': reset_link,
            }
        }
        
        try:
            response = requests.post(
                'https://api.emailjs.com/api/v1.0/email/send',
                json=emailjs_payload,
                timeout=10
            )
            
            if response.status_code != 200:
                error_msg = f"EmailJS API returned {response.status_code}: {response.text}"
                raise serializers.ValidationError(error_msg)
                
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(
                f"Failed to send password reset email: {str(e)}"
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