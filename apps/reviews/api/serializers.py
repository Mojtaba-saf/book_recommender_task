from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from apps.reviews.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["book", "rating"]
        extra_kwargs = {
            "rating": {"max_value": 5, "min_value": 1},
            "book": {"write_only": True},
        }

    def create(self, validated_data):
        review, created = Review.objects.get_or_create(
            book=validated_data["book"],
            user=self.context["request"].user,
            defaults={"rating": validated_data["rating"]},
        )
        if not created:
            raise ValidationError(detail={"detail": "rating already exists."})
        return review

    def update(self, instance, validated_data):
        review: Review = get_object_or_404(
            Review.objects.all(),
            book=validated_data["book"],
            user=self.context["request"].user,
        )
        updated_reviews = Review.objects.filter(id=review.id).update(
            rating=validated_data["rating"]
        )
        if updated_reviews == 0:
            raise Http404
        review.refresh_from_db()
        return review
