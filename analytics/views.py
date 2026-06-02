from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from compensation.models import CompensationData
from .serializers import SalaryAnalyticsSerializer
from rest_framework.response import Response


from django.db.models.functions import Coalesce
from django.db.models import DecimalField, Value, Avg, Min, Max, Count, Q
from django.contrib.auth import get_user_model
from companies.models import Company
from reviews.models import CompanyReview

class AnalyticsSummaryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_reviews = CompanyReview.objects.count()
        companies_listed = Company.objects.count()
        salary_data_points = CompensationData.objects.count()
        active_users = get_user_model().objects.filter(is_active=True).count()

        top_companies_qs = (
            Company.objects.annotate(review_count=Count('companyreview'))
            .order_by('-review_count')[:5]
        )
        top_companies = [
            {
                "name": comp.name,
                "industry": comp.industry,
                "reviews": comp.review_count,
                "type": comp.type,
            }
            for comp in top_companies_qs
        ]

        salary_benchmarks_qs = (
            CompensationData.objects.values('job_title')
            .annotate(min_salary=Min('base_salary'), max_salary=Max('base_salary'))
            .order_by('job_title')[:5]
        )
        salary_benchmarks = [
            {
                "job_title": sb['job_title'],
                "min_salary": sb['min_salary'],
                "max_salary": sb['max_salary'],
            }
            for sb in salary_benchmarks_qs
        ]

        avg_salary_by_industry_qs = (
            CompensationData.objects.values('company__industry')
            .annotate(avg_salary=Avg('base_salary'))
            .order_by('-avg_salary')
        )
        avg_salary_by_industry = [
            {
                "industry": item['company__industry'],
                "average_salary": item['avg_salary'],
            }
            for item in avg_salary_by_industry_qs
            if item['company__industry']
        ]

        data = {
            "total_reviews": total_reviews,
            "companies_listed": companies_listed,
            "salary_data_points": salary_data_points,
            "active_users": active_users,
            "top_rated_companies": top_companies,
            "salary_benchmarks": salary_benchmarks,
            "average_salary_by_industry": avg_salary_by_industry,
        }
        return Response(data)

class SalaryAnalyticsListView(generics.ListAPIView):
    serializer_class = SalaryAnalyticsSerializer
    permission_classes = [IsAuthenticated]  # 🔥 IMPORTANT FIX

    def get_queryset(self):
        queryset = CompensationData.objects.all()

        company = self.request.query_params.get("company")
        year = self.request.query_params.get("year")

        if company:
            queryset = queryset.filter(company_id=company)

        if year:
            queryset = queryset.filter(year=year)

        return queryset

class SalaryStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = CompensationData.objects.all()

        stats = queryset.aggregate(
            count=Count('id'),

            average_salary=Coalesce(
                Avg('base_salary'),
                Value(0),
                output_field=DecimalField()
            ),

            min_salary=Coalesce(
                Min('base_salary'),
                Value(0),
                output_field=DecimalField()
            ),

            max_salary=Coalesce(
                Max('base_salary'),
                Value(0),
                output_field=DecimalField()
            ),

            average_market_rating=Coalesce(
                Avg('market_fairness_rating'),
                Value(0)
            ),

            count_anonymous=Count('id', filter=Q(is_anonymous=True)),
        )

        return Response(stats)


# class SalaryAnalyticsDetailView(generics.RetrieveAPIView):
#     queryset = SalaryAnalytics.objects.all()
#     serializer_class = SalaryAnalyticsSerializer
#     permission_classes = [IsAuthenticated]


# class SalaryAnalyticsUpdateView(generics.UpdateAPIView):
#     queryset = SalaryAnalytics.objects.all()
#     serializer_class = SalaryAnalyticsSerializer
#     permission_classes = [IsAuthenticated]


# class SalaryAnalyticsDeleteView(generics.DestroyAPIView):
#     queryset = SalaryAnalytics.objects.all()
#     serializer_class = SalaryAnalyticsSerializer
#     permission_classes = [IsAuthenticated]