from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView

from apps.reviews.api.serializers import ReviewSerializer
from apps.reviews.models import Review


class CreateReviewAPIView(CreateAPIView):
    serializer_class = ReviewSerializer


class UpdateReviewAPIView(UpdateAPIView):
    http_method_names = ["options", "patch"]
    serializer_class = ReviewSerializer

    def get_object(self):
        return True


class DestroyReviewAPIView(DestroyAPIView):
    lookup_field = "book_id"
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
