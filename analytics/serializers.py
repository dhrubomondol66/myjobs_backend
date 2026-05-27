from rest_framework import serializers, filters, generics
from .models import SalaryAnalytics
from companies.models import Company
from django.db.models import Avg


def validate_rating(value):
    if value < 1 or value > 5:
        raise serializers.ValidationError("Rating must be between 1 and 5")
    return value


class SalaryAnalyticsSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )

    market_fairness_rating = serializers.IntegerField(
        validators=[validate_rating]
    )

    class Meta:
        model = SalaryAnalytics
        fields = [
            'id',
            'company',
            'user',
            'job_title',
            'department',
            'base_salary',
            'fringe_benefits_value',
            'other_allowances',
            'bonus_amount',
            'market_fairness_rating',
            'is_anonymous',
            'year',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)

class SalaryAnalyticsListView(generics.ListAPIView):
    serializer_class = SalaryAnalyticsSerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['job_title', 'company__name', 'department']
    ordering_fields = ['base_salary', 'market_fairness_rating', 'year']

    def get_queryset(self):
        queryset = SalaryAnalytics.objects.all()

        company = self.request.query_params.get("company")
        year = self.request.query_params.get("year")
        job_title = self.request.query_params.get("job_title")
        department = self.request.query_params.get("department")
        min_salary = self.request.query_params.get("min_salary")
        max_salary = self.request.query_params.get("max_salary")

        if company:
            queryset = queryset.filter(company_id=company)

        if year:
            queryset = queryset.filter(year=year)

        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)

        if department:
            queryset = queryset.filter(department=department)

        if min_salary:
            queryset = queryset.filter(base_salary__gte=min_salary)

        if max_salary:
            queryset = queryset.filter(base_salary__lte=max_salary)

        return queryset


class SalaryStatsView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = SalaryAnalytics.objects.all()

        # Apply same filters as ListAPIView
        company = request.query_params.get("company")
        year = request.query_params.get("year")
        job_title = request.query_params.get("job_title")
        department = request.query_params.get("department")
        min_salary = request.query_params.get("min_salary")
        max_salary = request.query_params.get("max_salary")

        if company:
            queryset = queryset.filter(company_id=company)

        if year:
            queryset = queryset.filter(year=year)

        if job_title:
            queryset = queryset.filter(job_title__icontains=job_title)

        if department:
            queryset = queryset.filter(department=department)

        if min_salary:
            queryset = queryset.filter(base_salary__gte=min_salary)

        if max_salary:
            queryset = queryset.filter(base_salary__lte=max_salary)

        stats = queryset.aggregate(
            count=Count('id'),
            average_salary=Avg('base_salary'),
            min_salary=Min('base_salary'),
            max_salary=Max('base_salary'),
            average_market_rating=Avg('market_fairness_rating'),
            count_anonymous=Count('id', filter=Q(is_anonymous=True)),
        )

        return Response(stats)