from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import SalaryAnalytics
from .serializers import SalaryAnalyticsSerializer, SalaryStatsView
from rest_framework.response import Response


from django.db.models import Count, Avg, Min, Max
from django.contrib.auth import get_user_model
from companies.models import Company
from reviews.models import CompanyReview

class AnalyticsSummaryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_reviews = CompanyReview.objects.count()
        companies_listed = Company.objects.count()
        salary_data_points = SalaryAnalytics.objects.count()
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
            SalaryAnalytics.objects.values('job_title')
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
            SalaryAnalytics.objects.values('company__industry')
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
        queryset = SalaryAnalytics.objects.all()

        company = self.request.query_params.get("company")
        year = self.request.query_params.get("year")

        if company:
            queryset = queryset.filter(company_id=company)

        if year:
            queryset = queryset.filter(year=year)

        return queryset


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