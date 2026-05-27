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
# path("create/", SalaryAnalyticsCreateView.as_view()),  # removed due to missing view
# path("<int:pk>/", SalaryAnalyticsDetailView.as_view()),  # removed
# path("<int:pk>/update/", SalaryAnalyticsUpdateView.as_view()),  # removed
# path("<int:pk>/delete/", SalaryAnalyticsDeleteView.as_view()),  # removed
]