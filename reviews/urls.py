from django.urls import path
from .views import (
    CompanyReviewCreateView,
    CompanyReviewListView,
    CompanyReviewDetailView,
    CompanyReviewUpdateView,
    CompanyReviewDeleteView,
)

urlpatterns = [
    path("", CompanyReviewListView.as_view()),
    path("create/", CompanyReviewCreateView.as_view()),
    path("<int:pk>/", CompanyReviewDetailView.as_view()),
    # path("<int:pk>/update/", CompanyReviewUpdateView.as_view()),
    # path("<int:pk>/delete/", CompanyReviewDeleteView.as_view()),
]