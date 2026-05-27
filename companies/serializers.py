from rest_framework import serializers
from django.db.models import Avg
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = (
            "user",
            "is_verified",
            "created_at",
            "updated_at",
        )

    def get_rating(self, obj):
        from compensation.models import CompensationData
        agg = CompensationData.objects.filter(company=obj).aggregate(avg_rating=Avg('market_fairness_rating'))
        return round(agg['avg_rating'], 2) if agg['avg_rating'] is not None else None