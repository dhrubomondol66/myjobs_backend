from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CompanyReview
from .serializers import (
    CompanyReviewSerializer,
    CompanyReviewListSerializer
)
from accounts.service import add_credits

class CompanyReviewCreateView(generics.CreateAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        user = request.user
        user.credits += 10
        user.save()

        headers = self.get_success_headers(serializer.data)

        return Response({
            "review": serializer.data,
            "credits_added": 10,
            "total_credits": user.credits
        }, status=status.HTTP_201_CREATED, headers=headers)


class CompanyReviewListView(generics.ListAPIView):
    queryset = CompanyReview.objects.all().order_by('-created_at')
    serializer_class = CompanyReviewListSerializer


class CompanyReviewDetailView(generics.RetrieveAPIView):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewListSerializer


class CompanyReviewUpdateView(generics.UpdateAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompanyReview.objects.filter(user=self.request.user)


class CompanyReviewDeleteView(generics.DestroyAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompanyReview.objects.filter(user=self.request.user)