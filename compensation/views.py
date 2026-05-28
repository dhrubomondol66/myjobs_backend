from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import CompensationData
from .serializers import CompensationSerializer


class CompensationCreateView(generics.CreateAPIView):
    serializer_class = CompensationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompensationListView(generics.ListAPIView):
    queryset = CompensationData.objects.all().order_by('-created_at')
    serializer_class = CompensationSerializer


class CompensationDetailView(generics.RetrieveAPIView):
    queryset = CompensationData.objects.all()
    serializer_class = CompensationSerializer


class CompensationUpdateView(generics.UpdateAPIView):
    serializer_class = CompensationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompensationData.objects.filter(
            user=self.request.user
        )


class CompensationDeleteView(generics.DestroyAPIView):
    serializer_class = CompensationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompensationData.objects.filter(
            user=self.request.user
        )