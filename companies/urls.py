from django.urls import path
from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
)

urlpatterns = [
    path("", CompanyListView.as_view()),
    path("create/", CompanyCreateView.as_view()),
    path("<int:pk>/", CompanyDetailView.as_view()),
    path("<int:pk>/update/", CompanyUpdateView.as_view()),
    path("<int:pk>/delete/", CompanyDeleteView.as_view()),
]