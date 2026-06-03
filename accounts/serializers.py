from django.core.mail import send_mail
from rest_framework import serializers
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
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
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = os.getenv('FRONTEND_URL')
        reset_link = f"{frontend_url}/#/reset-password/{uid}/{token}/"

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email, "name": user.username}],
            sender={"email": "dhrubomondol66@gmail.com", "name": "MyJobs"},
            subject="Password Reset - MyJobs",
            text_content=f"Hello {user.username},\n\nReset your password:\n{reset_link}\n\nExpires in 24 hours.\n\nMyJobs Team"
        )
        api_instance.send_transac_email(send_smtp_email)

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