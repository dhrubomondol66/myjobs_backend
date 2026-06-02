from rest_framework import serializers
from .models import CompensationData
from companies.models import Company


class CompensationSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )
    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )
    
    class Meta:
        model = CompensationData

        fields = [
            'id',
            'user',
            'company',
            'company_name',
            'job_title',
            'department',
            'base_salary',
            'fringe_benefits_value',
            'other_allowances',
            'annual_bonus_structure',
            'market_fairness_rating',
            'is_anonymous',
            'year',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
        ]

    def validate_base_salary(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Base salary must be greater than 0"
            )

        return value