from rest_framework import serializers
from .models import CompanyReview
from companies.models import Company


class CompanyReviewSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Company.objects.all()
    )

    class Meta:
        model = CompanyReview

        fields = [
            'id',
            'user',
            'company',
            'is_anonymous',
            'company_type',
            'brand_value',
            'work_environment',
            'career_growth',
            'work_life_balance',
            'management_quality',
            'salary_benefits',
            'recommendation',
            'overall_experience',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
        ]


class CompanyReviewListSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source='company.name',
        read_only=True
    )

    class Meta:
        model = CompanyReview

        fields = [
            'id',
            'company_name',
            'is_anonymous',
            'company_type',
            'brand_value',
            'work_environment',
            'career_growth',
            'work_life_balance',
            'management_quality',
            'salary_benefits',
            'recommendation',
            'overall_experience',
            'created_at',
        ]