from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
)
from .models import Company
from .serializers import CompanySerializer

class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class CompanyDeleteView(generics.DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]