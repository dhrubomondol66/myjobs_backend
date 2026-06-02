from django.urls import path
from .views import (
    SalaryAnalyticsListView,
    AnalyticsSummaryView,
    SalaryStatsView,
)

urlpatterns = [
    path("summary/", AnalyticsSummaryView.as_view()),
    path("salary/", SalaryAnalyticsListView.as_view()),
    path("salary/stats/", SalaryStatsView.as_view()),
]