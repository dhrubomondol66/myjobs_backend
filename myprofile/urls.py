from django.urls import path
from .views import (
    UserProfileListView,
    UserProfileDetailView,
    UserProfileUpdateView,
)

urlpatterns = [
    path("me/", UserProfileDetailView.as_view()),
    path("update/", UserProfileUpdateView.as_view()),
]