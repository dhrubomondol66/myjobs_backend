from django.urls import path
from .views import (
    CompensationCreateView,
    CompensationListView,
    CompensationDetailView,
    CompensationUpdateView,
    CompensationDeleteView,
)

urlpatterns = [
    path("", CompensationListView.as_view()),
    path("create/", CompensationCreateView.as_view()),
    path("<int:pk>/", CompensationDetailView.as_view()),
    path("<int:pk>/update/", CompensationUpdateView.as_view()),
    path("<int:pk>/delete/", CompensationDeleteView.as_view()),
]