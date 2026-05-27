from rest_framework import serializers
from .models import CompanyReview
from companies.models import Company

class CompanyReviewSerializer(serializers.ModelSerializer):
    # company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    class Meta:
        model = CompanyReview
        fields = [
            'id',
            'user',
            'company',
            'is_anonymous',
            'brand_value',
            'work_environment',
            'career_growth',
            'salary_range_perception',
            'fringe_benefits',
            'job_security',
            'employee_respect',
            'overall_recommendation',
            'created_at',
        ]
        read_only_fields = [
            'user',
            'created_at',
        ]

class CompanyReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = [
            'id',
            'user',
            'company',
            'is_anonymous',
            'brand_value',
            'work_environment',
            'career_growth',
            'salary_range_perception',
            'fringe_benefits',
            'job_security',
            'employee_respect',
            'overall_recommendation',
            'created_at',
        ]
        read_only_fields = [
            'user',
            'created_at',
        ]   