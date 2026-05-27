from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'full_name',
            'current_work_status',
            'current_designation',
            'current_industry',
            'current_company',
            'current_salary',
            'city',
            'is_verified',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'user',
            'is_verified',
            'created_at',
            'updated_at',
        ]