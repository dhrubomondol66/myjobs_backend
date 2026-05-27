from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CompanyReview
from .serializers import CompanyReviewSerializer, CompanyReviewListSerializer

class CompanyReviewCreateView(generics.CreateAPIView):
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyReviewListView(generics.ListAPIView):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewListSerializer

class CompanyReviewDetailView(generics.RetrieveAPIView):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewListSerializer

class CompanyReviewUpdateView(generics.UpdateAPIView):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]

class CompanyReviewDeleteView(generics.DestroyAPIView):
    queryset = CompanyReview.objects.all()
    serializer_class = CompanyReviewSerializer
    permission_classes = [IsAuthenticated]
